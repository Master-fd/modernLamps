#coding: utf8

__author__ = 'fenton-fd.zhu'

from django.conf.urls import url, include
from website import views

urlpatterns = [
    url(r'^noresults/$', views.noresults),   #无结果页面
    url(r'^$', views.home),
    url(r'^home/$', views.home),  #首页
    url(r'^allGoods/(?P<subClass>\w+)/$', views.goodsBrowse),   #所有商品list页面,分类
    url(r'^goodsInfo/(?P<goodsId>\d+)/$', views.goodsInfo),   #商品详情
    url(r'^search/$', views.search),   #返回搜索结果
    url(r'^shoppingCart/$', views.shoppingCart),   #购物车页面
    url(r'^order/checkout/$', views.orderCheckout),   #结算页面

    url(r'^userBackgroup/$', views.userBackgroupOrder),  #用户后台页面order
    url(r'^userBackgroup/order/$', views.userBackgroupOrder),  #用户后台页面order
    url(r'^userBackgroup/collect/$', views.userBackgroupCollect),  #用户后台页面collect
    url(r'^userBackgroup/address/$', views.userBackgroupAddress),  #用户后台页面address
    url(r'^userBackgroup/userInfo/$', views.userBackgroupUserInfo),  #用户后台页面personal

    url(r'^managerBackgroup/$', views.managerAllOrder),  #后台页面order
    url(r'^managerBackgroup/allOrder/$', views.managerAllOrder),  #后台页面order
    url(r'^managerBackgroup/uploader/$', views.managerUploader),  #上传
    url(r'^managerBackgroup/goods/$', views.managerAllGoods),  #所有商品


    url(r'^userInfoRequest/$', views.userInfoRequestPortManager),   #用户信息请求类处理端口，例如Login，检查是否login等
    url(r'^addressRequest/$', views.addressRequestPortManager),   #用户地址请求类处理端口
    url(r'^goodsInfoRequest/$', views.goodsInfoRequestPortManager),   #goods请求类处理端口
    url(r'^collectRequest/$', views.collectRequestPortManager),      #用户收藏请求类处理端口
    url(r'^shoppingCartRequest/$', views.shoppingCartRequestPortManager),      #用户购物车请求类处理端口
    url(r'^orderRequest/$', views.orderRequestPortManager),      #用户订单请求类处理端口

    url(r'^bottom/(?P<page>\w+)/$', views.bottomStaticPage)   #底部静态页面
]

