#coding: utf8
from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render_to_response
from website.python.user.userInfo import UserInfo
from website.python.user.myShoppingCart import ShoppingCartInfo
from website.python.user.myAddress import AddressInfo
from website.python.user.myCollect import CollectInfo
from website.python.goods.goodsInfo import GoodsInfo
from website.python.order.order import OrderInfo


'''
请求接口函数
'''



#页面返回页面
def home(request):
    return render_to_response('goods/goodsInfo.html');



#渲染一个商品
def goodsInfo(request, goodsId):
    return GoodsInfo.goodsInfo(goodsId);

#返回用户后台首页
def userBackgroup(request):
    return render_to_response('myBackgroup/myCollect.html');


#ajax请求类操作
def userInfoRequestPortManager(request):
    return UserInfo.userInfoRequestPortManager(request);

def goodsInfoRequestPortManager(request):
    return GoodsInfo.goodsRequestPortManager(request);

def orderRequestPortManager(request):
    return OrderInfo.orderRequestPortManager(request);

def addressRequestPortManager(request):
    return AddressInfo.addressRequestPortManager(request);

def collectRequestPortManager(request):
    return CollectInfo.collectRequestPortManager(request);

def shoppingCartRequestPortManager(request):
    return ShoppingCartInfo.shoppingCartRequestPortManager(request);
