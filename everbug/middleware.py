from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import MiddlewareNotUsed
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from everbug.utils.context import wrap_context
from everbug.utils.manager import ProfileManager
from everbug.utils.queries import wrap_queries
from everbug.utils.serilalize import serial


class Header:
    REQUEST = 'HTTP_REQUEST_ID'
    TRACE = 'HTTP_TRACE_ID'
    HAS_TRACE = 'HTTP_HAS_TRACE'


class Field:
    CONTEXT = 'context'
    QUERIES = 'queries'
    PROFILES = 'profiles'


class Tracer(MiddlewareMixin):

    def __init__(self, get_response=None):
        if not getattr(settings, 'DEBUG', False):
            raise MiddlewareNotUsed
        super().__init__()
        self.get_response = get_response
        self.request_id = 0
        self.manager = ProfileManager()
        self.data = {}

    def process_request(self, request):
        if Header.TRACE in request.META:
            trace_id = request.META.get(Header.TRACE, 0)
            cached_data = cache.get(trace_id, {})
            json_response = {
                'data': cached_data,
                'status': 200 if cached_data else 404,
                'json_dumps_params': {'default': serial}
            }
            return JsonResponse(**json_response)
        elif Header.REQUEST in request.META:
            self.manager.clear()
            self.data = {}
            self.request_id = request.META.get(Header.REQUEST, 0)

    def process_template_response(self, request, response):
        if self.request_id and not request.path.startswith('/admin/'):
            if getattr(response, 'context_data', None):
                self.data[Field.CONTEXT] = wrap_context(response.context_data)
        return response

    def process_response(self, request, response):
        if Header.REQUEST in request.META and self.request_id:
            self.data[Field.QUERIES] = wrap_queries()
            if self.manager.count > 0:
                self.data[Field.PROFILES] = self.manager.profiles()
            self.data = {k: v for k, v in self.data.items() if v}
            if self.data:
                cache.set(self.request_id, self.data)
                response[Header.HAS_TRACE] = self.request_id
            else:
                response[Header.HAS_TRACE] = 0
        return response
