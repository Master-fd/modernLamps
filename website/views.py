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


#返回没有结果界面
def noresults(request):
    isLogin, account = UserInfo.checkIsLogin(request);
    return Responses.returnDrawPage(isLogin, 'common/noresult.html', 'goodsList', None);

#搜索接口
def search(request):
    isLogin, account = UserInfo.checkIsLogin(request);
    goodsName = request.GET.get('keyword', None);
    goodsList = GoodsInfo.searchGoods(1, 20, goodsName);
    data = {
        'subClass' : 'undefine',
        'goodsList' : goodsList
    }
    if goodsList:
        return Responses.returnDrawPage(isLogin, 'goods/goodsBrowse.html', 'data', data);
    else:
        return Responses.returnDrawPage(isLogin, 'common/noresult.html', 'data', None);

#返回首页页面
def home(request):
    isLogin, account = UserInfo.checkIsLogin(request);
    goods = GoodsInfo.getGoodsData(1, 20, None);
    try:
        goodsList = {
            'banner1' : goods[0],
            # 'banner2' : goods[1],
            # 'banner3' : goods[2],
            # 'banner4' : goods[3],
            # 'hotGoods1' : goods[4],
            # 'hotGoods2' : goods[5],
            # 'hotGoods3' : goods[6],
            # 'hotGoods4' : goods[7],
            # 'hotGoods5' : goods[8],
            # 'hotGoods6' : goods[9],
            # 'first1' : goods[10],
            # 'first2' : goods[11],
            # 'first3' : goods[12],
            # 'first4' : goods[13],
            # 'first5' : goods[14],
            # 'first6' : goods[15]
        };
    except Exception, e:
        return Responses.returnDrawPage(isLogin, 'home/home.html', 'goodsList', None);
    else:
        return Responses.returnDrawPage(isLogin, 'home/home.html', 'goodsList', goodsList);

#渲染所有商品页面,需要设置分类
def goodsBrowse(request, subClass):
    isLogin, account = UserInfo.checkIsLogin(request);
    if subClass != 'undefine':
        condition = {
            'subClass' : subClass
        }
        goodsList = GoodsInfo.getGoodsData(1, 20, condition);
    else:
        goodsList = GoodsInfo.getGoodsData(1, 20, None);
    print subClass, goodsList;

    data = {
        'subClass' : subClass,
        'goodsList' : goodsList
    }
    return Responses.returnDrawPage(isLogin, 'goods/goodsBrowse.html', 'data', data);


#渲染一个商品
def goodsInfo(request, goodsId):
    isLogin, account = UserInfo.checkIsLogin(request);
    condition = {
        'goodsId': goodsId
    };

    goodsList = GoodsInfo.getGoodsData(1, 20, condition);
    return Responses.returnDrawPage(isLogin, 'goods/goodsInfo.html', 'goods', goodsList[0]);

#管理员上传页面
def managerUploader(request):
    isLogin, account = UserInfo.checkIsLogin(request);
    return Responses.returnDrawPage(isLogin, 'managerBackgroup/uploadGoods.html', 'upload', None);
#管理员所有商品
def managerAllGoods(request):
    isLogin, account = UserInfo.checkIsLogin(request);
    #分页获取所有商品
    goodsList = GoodsInfo.getGoodsData(1, 20, None);
    return Responses.returnDrawPage(isLogin, 'managerBackgroup/allGoods.html', 'goodsList', goodsList);
#管理员所有订单
def managerAllOrder(request):
    isLogin, account = UserInfo.checkIsLogin(request);
    return Responses.returnDrawPage(isLogin, 'managerBackgroup/allOrder.html', 'ordersList', None);

#返回用户后台首页 order
def userBackgroupOrder(request):
    #获取order信息
    isLogin, account = UserInfo.checkIsLogin(request);
    condition = {
        'account' : account
    }

    orderList = OrderInfo.getOrderData(1, 20, account, condition);
    return Responses.returnCheckLoginDrawPage(isLogin, 'myBackgroup/myOrder.html', 'orderList', orderList);
#用户后台 收藏
def userBackgroupCollect(request):
    #获取order信息
    isLogin, account = UserInfo.checkIsLogin(request);
    condition = {
        'account' : account
    }
    collectList = CollectInfo.getCollectData(1, 20, account, condition);
    return Responses.returnCheckLoginDrawPage(isLogin, 'myBackgroup/myCollect.html', 'collectList', collectList);
#用户后台 地址
def userBackgroupAddress(request):
    #获取order信息
    isLogin, account = UserInfo.checkIsLogin(request);
    condition = {
        'account' : account
    }
    addressList = AddressInfo.getAddressData(1, 20, account, condition);
    return Responses.returnCheckLoginDrawPage(isLogin, 'myBackgroup/myAddress.html', 'addressList', addressList);
#用户后台 我的资料
def userBackgroupUserInfo(request):
    #获取order信息
    isLogin, account = UserInfo.checkIsLogin(request);
    userInfo = UserInfo.getUserInfoData(account);
    userInfo=userInfo[0];
    return Responses.returnCheckLoginDrawPage(isLogin, 'myBackgroup/myPersonal.html', 'userInfo', userInfo);

#ajax请求类操作
def userInfoRequestPortManager(request): #check ok
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
