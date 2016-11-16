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
from website.python.common.response import Responses


'''
请求接口函数
'''



#返回首页页面
def home(request):
    # isLogin, account = UserInfo.checkIsLogin();
    # goods = GoodsInfo.getGoodsData(1, 20, None);
    # goodsList = {
    #     'banner1' : goods[0],
    #     'banner2' : goods[1],
    #     'banner3' : goods[2],
    #     'banner4' : goods[3],
    #     'hotGoods1' : goods[4],
    #     'hotGoods2' : goods[5],
    #     'hotGoods3' : goods[6],
    #     'hotGoods4' : goods[7],
    #     'hotGoods5' : goods[8],
    #     'hotGoods6' : goods[9],
    #     'first1' : goods[10],
    #     'first2' : goods[11],
    #     'first3' : goods[12],
    #     'first4' : goods[13],
    #     'first5' : goods[14],
    #     'first6' : goods[15],
    #
    # }
    isLogin = False;
    return Responses.returnDrawPage(isLogin, 'home/home.html', 'goodsList', None);

#渲染一个商品
def goodsInfo(request, goodsId):
    isLogin, account = UserInfo.checkIsLogin();
    condition = {
        'goodsId', goodsId
    }
    goods = GoodsInfo.getGoodsData(1, 20, condition);
    return Responses.returnDrawPage(isLogin, 'goods/goodsInfo.html', 'goods', **goods);


#返回用户后台首页
def userBackgroup(request):
    #获取order信息
    isLogin, account = UserInfo.checkIsLogin();
    condition = {
        'account' : account
    }
    orderList = OrderInfo.getOrderData(1, 20, account, condition);
    return Responses.returnCheckLoginDrawPage(isLogin, 'myBackgroup/myCollect.html', 'orderList', orderList);


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
