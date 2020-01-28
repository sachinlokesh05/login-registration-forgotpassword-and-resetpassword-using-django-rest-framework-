# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django_short_url import views as surl_views


app_name = 'django_short_url'


urlpatterns = [
    url(r'^(?P<surl>\w+)', surl_views.short_url_redirect, name='short_url_redirect'),
]
