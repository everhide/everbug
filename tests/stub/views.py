from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from tests.stub.models import AltEntity, Entity


CONTEXT = {'yes': True}
TEMPLATE = 'index.html'


def context(request, *args, **kwargs):
    return TemplateResponse(request, TEMPLATE, CONTEXT)


def context_render(request):
    return render(request, TEMPLATE, CONTEXT)


def context_empty(request):
    return TemplateResponse(request, TEMPLATE, {})


class ContextEmpty(TemplateView):
    template_name = TEMPLATE


class Context(TemplateView):
    template_name = TEMPLATE

    def get_context_data(self, **kwargs):
        return CONTEXT


def query_single(request):
    list(Entity.objects.all())
    return render(request, TEMPLATE)


def query_multiply(request):
    list(Entity.objects.all())
    list(AltEntity.objects.all())
    return render(request, TEMPLATE)


def query_no(request):
    return render(request, TEMPLATE)
