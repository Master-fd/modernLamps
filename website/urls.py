#coding: utf8

__author__ = 'fenton-fd.zhu'

from django.conf.urls import url, include
from website import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^home/$', views.home),  #首页
    # url(r'^shoppingCart/$', views.shoppingCart),   #购物车页面
    url(r'^userBackgroup/$', views.userBackgroup),  #用户后台页面


    url(r'^userInfoRequest/$', views.userInfoRequestPortManager),   #用户信息请求类处理端口，例如Login，检查是否login等

]

