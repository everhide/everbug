from django.conf.urls import url

from tests.stub.views import (
    Context,
    ContextEmpty,
    context,
    context_empty,
    context_render,
    query_multiply,
    query_no,
    query_single
)


urlpatterns = [
    url(r'^context/$', context),
    url(r'^context_empty/$', context_empty),
    url(r'^context_render/$', context_render),
    url(r'^context_cbv/$', Context.as_view()),
    url(r'^context_cbv_empty/$', ContextEmpty.as_view()),
    url(r'^query_no/$', query_no),
    url(r'^query_single/$', query_single),
    url(r'^query_multiply/$', query_multiply),
]
