#coding: utf8

__author__ = 'fenton-fd.zhu'

from django.conf.urls import url, include
from website import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^home/$', views.home),  #首页
    url(r'^allGoods/$', views.allGoods),   #所有商品list页面

    # url(r'^shoppingCart/$', views.shoppingCart),   #购物车页面

    url(r'^userBackgroup/$', views.userBackgroupOrder),  #用户后台页面order
    url(r'^userBackgroup/order/$', views.userBackgroupOrder),  #用户后台页面order
    url(r'^userBackgroup/collect/$', views.userBackgroupCollect),  #用户后台页面collect
    url(r'^userBackgroup/address/$', views.userBackgroupAddress),  #用户后台页面address
    url(r'^userBackgroup/userInfo/$', views.userBackgroupUserInfo),  #用户后台页面personal

    url(r'^userInfoRequest/$', views.userInfoRequestPortManager),   #用户信息请求类处理端口，例如Login，检查是否login等
    url(r'^addressRequest/$', views.addressRequestPortManager),   #用户地址请求类处理端口，
]

