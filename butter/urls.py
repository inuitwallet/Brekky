from django.conf.urls import url
from django.http.request import QueryDict

from . import views

urlpatterns = [
    url(
        r'^$',
        views.index,
        name='index',
    ),
    url(
        r'^selling-page-2/(?P<tx_id>\d+?)/$',
        views.selling_page_2,
        name='selling_page_2',
    ),
]
