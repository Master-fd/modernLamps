#coding utf8

__author__ = 'fenton-fd.zhu'

from django.conf.urls import url, include
from website import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^index/$', views.index),
]

