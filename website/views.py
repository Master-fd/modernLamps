#conding utf8
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


def home(request):
    return render_to_response('home.html');

def userInfoRequestPortManager(request):
    return UserInfo.userInfoRequestPortManager(request);

def goodsInfoRequestPortManager(request):
    return GoodsInfo.userInfoRequestPortManager(request);

#渲染一个商品
def goodsInfo(request, goodsId):
    return GoodsInfo.goodsInfo(goodsId);

def orderRequestPortManager(request):
    return OrderInfo.userInfoRequestPortManager(request);

def addressRequestPortManager(request):
    return AddressInfo.userInfoRequestPortManager(request);

def collectRequestPortManager(request):
    return CollectInfo.userInfoRequestPortManager(request);

def shoppingCartRequestPortManager(request):
    return ShoppingCartInfo.userInfoRequestPortManager(request);
