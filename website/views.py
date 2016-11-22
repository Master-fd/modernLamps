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
from website.python.order.orderGoodsInfo import OrderGoodsInfo
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
    goodsList = GoodsInfo.searchGoods(1, 50, goodsName);
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
    goods, pageResult = GoodsInfo.getGoodsData(1, 20, None);
    try:
        goodsList = {
            'banner1' : goods[0],
            # 'banner2' : goods[1],
            # 'banner3' : goods[2],
            # 'banner4' : goods[3],
            'hotGoods1' : goods[0],
            # 'hotGoods2' : goods[5],
            # 'hotGoods3' : goods[6],
            # 'hotGoods4' : goods[7],
            # 'hotGoods5' : goods[8],
            # 'hotGoods6' : goods[9],
            'first1' : goods[0],
            'first2' : goods[0],
            'first3' : goods[0],
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
    #获取页码
    try:
        page = int(request.GET.get('page', '1'));
    except Exception, e:
        page = 1;

    if subClass != 'undefine':
        condition = {
            'subClass' : subClass
        }
        goodsList, pageResult = GoodsInfo.getGoodsData(page, 12, condition);
    else:
        goodsList, pageResult = GoodsInfo.getGoodsData(page, 12, None);  #获取所有

    #限定只能看到多少页，例如总的有20页，只限定看2--5页
    new_page_range = [];
    if pageResult:
        for page_number in pageResult.paginator.page_range:
            if abs(page_number-pageResult.number) <= 3:
                new_page_range.append(page_number);

    data = {
        'subClass' : subClass,
        'goodsList' : goodsList,
        'pageResult' : pageResult,
        'new_page_range' : new_page_range
    }
    return Responses.returnDrawPage(isLogin, 'goods/goodsBrowse.html', 'data', data);


#渲染一个商品
def goodsInfo(request, goodsId):
    isLogin, account = UserInfo.checkIsLogin(request);
    condition = {
        'goodsId': goodsId
    };
    goodsList, pageResult = GoodsInfo.getGoodsData(1, 20, condition);

    minImageUrls = [];
    descImageUrls = [];
    if goodsList:
        for (key, value) in goodsList[0].items():
            if key[0:11] == 'minImageUrl' and value != '':
                minImageUrls.append(value);
            if key[0:12] == 'descImageUrl' and value != '':
                descImageUrls.append(value);
    else:
        return Responses.returnDrawPage(isLogin, 'common/noresult.html', 'data', None);

    goods = goodsList[0];
    goods['minImageUrls'] = minImageUrls;
    goods['descImageUrls'] = descImageUrls;

    return Responses.returnDrawPage(isLogin, 'goods/goodsInfo.html', 'goods', goods);

#购物车页面
def shoppingCart(request):
    isLogin, account = UserInfo.checkIsLogin(request);

    goodsList = [];
    totalPrice = 0;
    allSelect = 1;
    try:
        #先从购物车表获取goodsid,再获取商品
        condition = {
            'account' : account,
        }
        data = ShoppingCartInfo.getShoppingCartData(1, 2000, condition);
        if data:
            for obj in data:
                objList, pageResult = GoodsInfo.getGoodsData(1, 2000, {'goodsId' : obj['goodsId']});
                goods = objList[0];
                #从新计算价格,以最新的为准
                obj['sumPrice'] = str(float(goods['price'])*obj['count']);
                if obj['count'] > goods['inventoryCount']:
                    goods['isOverflow'] = 1;  #库存不足
                else:
                    goods['isOverflow'] = 0;
                goods['count'] = obj['count'];  #增加属性
                goods['sumPrice'] = obj['sumPrice'];
                goods['isSelect'] = obj['isSelect'];

                if not obj['isSelect']:
                    allSelect = 0;
                goodsList.append(goods);
                if obj['isSelect']:
                    totalPrice += float(goods['sumPrice']);
    except Exception, e:
        Responses.returnCheckLoginDrawPage(isLogin, 'goods/shoppingCart.html', 'data', None);


    order = {
        'goodsList' : goodsList,
        'totalPrice' : totalPrice,
        'allSelect' : allSelect,
    };

    return Responses.returnCheckLoginDrawPage(isLogin, 'goods/shoppingCart.html', 'order', order);
#结算页面
def orderCheckout(request):
    isLogin, account = UserInfo.checkIsLogin(request);
    try:
        goodsId = request.GET.get('goodsId', None);
        count = int(request.GET.get('count', '1'));
    except Exception, e:
        goodsId = request.GET.get('goodsId', None);
        count = 1;

    goodsList = [];
    addressList = [];
    freightCost = 0;
    totalPrice = 0;
    rowspan = 1;  #运费表格占用多少行
    try:
        #获取地址
        condition = {
            'account' : account
        };
        addressList = AddressInfo.getAddressData(1, 2000, account, condition);
    except Exception, e:
        addressList = [];

    if goodsId:
        #有商品id,说明是立即购买
        try:
            goodsList, pageResult = GoodsInfo.getGoodsData(1, 2000, {'goodsId' : goodsId});
            goods = goodsList[0];
            if count < 1:
                count = 1;
            if count > goods['inventoryCount']:
                return Responses.responseJsonArray('fail', '库存不足');
            freightCost = float(goods['freightCost']);
            totalPrice = float(goods['price'])*count;
            goods['count'] = count;  #增加一个数量
            goods['sumPrice'] = totalPrice;  #增加一个小计
        except Exception, e:
            return Responses.returnCheckLoginDrawPage(isLogin, 'goods/orderCheckout.html', 'order', None);
    else:
        #没有则渲染购物车里面的
        try:
            #先从购物车表获取goodsid,再获取商品
            condition = {
                'account' : account,
                'isSelect' : True
            }
            data = ShoppingCartInfo.getShoppingCartData(1, 2000, condition);
            if data:
                for obj in data:
                    objList, pageResult = GoodsInfo.getGoodsData(1, 2000, {'goodsId' : obj['goodsId']});
                    goods = objList[0];
                    #从新计算价格,以最新的为准
                    obj['sumPrice'] = str(float(goods['price'])*obj['count']);
                    freightCost += float(goods['freightCost']);
                    goods['count'] = obj['count'];  #增加属性
                    goods['sumPrice'] = obj['sumPrice'];
                    goodsList.append(goods);
                    totalPrice += float(goods['sumPrice']);
            rowspan = len(data);  #占有表格的行数
        except Exception, e:
            return Responses.returnCheckLoginDrawPage(isLogin, 'goods/orderCheckout.html', 'order', None);

    order = {
        'goodsList' : goodsList,
        'addressList' : addressList,
        'freightCost' : freightCost,
        'totalPrice' : totalPrice,
        'rowspan' : rowspan
    };

    return Responses.returnCheckLoginDrawPage(isLogin, 'goods/orderCheckout.html', 'order', order);

#管理员上传页面
def managerUploader(request):
    isLogin, account = UserInfo.checkIsLogin(request);
    data = {
        'superUser' : UserInfo.checkIsSuperUser(request)
    }
    return Responses.returnCheckLoginDrawPage(isLogin, 'managerBackgroup/uploadGoods.html', 'data', data);
#管理员所有商品
def managerAllGoods(request):
    isLogin, account = UserInfo.checkIsLogin(request);

    #获取页码
    try:
        page = int(request.GET.get('page', '1'));
    except Exception, e:
        page = 1;
    #分页获取所有商品
    goodsList, pageResult = GoodsInfo.getGoodsData(page, 12, None);
    #限定只能看到多少页，例如总的有20页，只限定看2--5页
    new_page_range = [];
    if pageResult:
        for page_number in pageResult.paginator.page_range:
            if abs(page_number-pageResult.number) <= 3:
                new_page_range.append(page_number);
    data = {
        'goodsList' : goodsList,
        'pageResult' : pageResult,
        'new_page_range' : new_page_range,
        'superUser' : UserInfo.checkIsSuperUser(request)
    }
    return Responses.returnCheckLoginDrawPage(isLogin, 'managerBackgroup/allGoods.html', 'data', data);
#管理员所有订单
def managerAllOrder(request):
    isLogin, account = UserInfo.checkIsLogin(request);
    #获取页码
    try:
        page = int(request.GET.get('page', '1'));
    except Exception, e:
        page = 1;

    #获取订单
    allOrder, pageResult = OrderInfo.getOrderData(page, 12, account);
    #限定只能看到多少页，例如总的有20页，只限定看2--5页
    new_page_range = [];
    if pageResult:
        for page_number in pageResult.paginator.page_range:
            if abs(page_number-pageResult.number) <= 3:
                new_page_range.append(page_number);

    orderList = [];
    if allOrder:  #所有订单
        for order in allOrder:
            #获取该笔订单的所有商品
            orderGoods = OrderGoodsInfo.getOrderGoodsData(account, {'orderId' : order['orderId']});
            goodsList = [];   #一个订单的所有商品
            if orderGoods:
                for obj in orderGoods:
                    list, pageGoodsResult = GoodsInfo.getGoodsData(1, 2000, {'goodsId' : obj['goodsId']});
                    goods = list[0];
                    goods['count'] = obj['count'];
                    goodsList.append(goods);

            #拼接成一个完整的订单
            order['goodsList'] = goodsList;
            order['goodsCount'] = len(goodsList);        #商品数量

            #添加到订单列表
            orderList.append(order);

    data = {
        'orderList' : orderList,
        'pageResult' : pageResult,
        'new_page_range' : new_page_range,
        'superUser' : UserInfo.checkIsSuperUser(request)
    }
    return Responses.returnCheckLoginDrawPage(isLogin, 'managerBackgroup/allOrder.html', 'data', data);

#返回用户后台首页 order
def userBackgroupOrder(request):
    #获取order信息
    isLogin, account = UserInfo.checkIsLogin(request);
    isSuperUser = UserInfo.checkIsSuperUser(request);

    #获取页码
    try:
        page = int(request.GET.get('page', '1'));
    except Exception, e:
        page = 1;

    #获取该用户的所有order
    allOrder, pageResult = OrderInfo.getOrderData(page, 12, account, {'account' : account});
    #限定只能看到多少页，例如总的有20页，只限定看2--5页
    new_page_range = [];
    if pageResult:
        for page_number in pageResult.paginator.page_range:
            if abs(page_number-pageResult.number) <= 3:
                new_page_range.append(page_number);

    orderList = [];
    if allOrder:  #所有订单
        for order in allOrder:
            #获取该笔订单的所有商品
            orderGoods = OrderGoodsInfo.getOrderGoodsData(account, {'orderId' : order['orderId']});
            goodsList = [];   #一个订单的所有商品
            if orderGoods:
                for obj in orderGoods:
                    list, pageGoodsResult = GoodsInfo.getGoodsData(1, 2000, {'goodsId' : obj['goodsId']});
                    goods = list[0];
                    goods['count'] = obj['count'];
                    goodsList.append(goods);

            #拼接成一个完整的订单
            order['goodsList'] = goodsList;
            order['goodsCount'] = len(goodsList);        #商品数量
            #添加到订单列表
            orderList.append(order);

    data = {
        'orderList' : orderList,
        'pageResult' : pageResult,
        'new_page_range' : new_page_range,
        'superUser' : isSuperUser
    }

    return Responses.returnCheckLoginDrawPage(isLogin, 'myBackgroup/myOrder.html', 'data', data);

#用户后台 收藏
def userBackgroupCollect(request):

    isLogin, account = UserInfo.checkIsLogin(request);
    isSuperUser = UserInfo.checkIsSuperUser(request);
    #获取页码
    try:
        page = int(request.GET.get('page', '1'));
    except Exception, e:
        page = 1;

    #获取该用户collect
    collectList, pageResult = CollectInfo.getCollectData(page, 12, account, {'account' : account});
    #限定只能看到多少页，例如总的有20页，只限定看2--5页
    new_page_range = [];
    if pageResult:
        for page_number in pageResult.paginator.page_range:
            if abs(page_number-pageResult.number) <= 3:
                new_page_range.append(page_number);

    goodsList = [];
    if collectList:
        for collect in  collectList:
            goods, pageGoodsResult = GoodsInfo.getGoodsData(1, 2000, {'goodsId' : collect['goodsId']});
            goodsList.append(goods[0]);

    data = {
        'collectList' : goodsList,
        'pageResult' : pageResult,
        'new_page_range' : new_page_range,
        'superUser' : isSuperUser
    }
    return Responses.returnCheckLoginDrawPage(isLogin, 'myBackgroup/myCollect.html', 'data', data);
#用户后台 地址
def userBackgroupAddress(request):
    #获取order信息
    isLogin, account = UserInfo.checkIsLogin(request);
    #获取地址
    addressList = AddressInfo.getAddressData(1, 2000, account, {'account' : account});
    data = {
        'addressList' : addressList,
        'superUser' : UserInfo.checkIsSuperUser(request)
    }

    return Responses.returnCheckLoginDrawPage(isLogin, 'myBackgroup/myAddress.html', 'data', data);
#用户后台 我的资料
def userBackgroupUserInfo(request):
    #获取order信息
    isLogin, account = UserInfo.checkIsLogin(request);
    userInfo = UserInfo.getUserInfoData(account);
    data = [];
    if userInfo:
        userInfo=userInfo[0];
        data = {
            'userInfo' : userInfo,
            'superUser' : UserInfo.checkIsSuperUser(request)
        }
    return Responses.returnCheckLoginDrawPage(isLogin, 'myBackgroup/myPersonal.html', 'data', data);

#bottom静态页面
def bottomStaticPage(request, page):
    isLogin, account = UserInfo.checkIsLogin(request);
    if page == 'about':
        return Responses.returnDrawPage(isLogin, 'static/about.html', 'about', None);
    elif page == 'bigSale':
        return Responses.returnDrawPage(isLogin, 'static/bigSale.html', 'bigsale', None);
    elif page == 'privacy':
        return Responses.returnDrawPage(isLogin, 'static/privacy.html', 'privacy', None);
    elif page == 'saleBack':
        return Responses.returnDrawPage(isLogin, 'static/saleBack.html', 'saleback', None);
    else:
        return HttpResponseRedirect('noresults/');

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
