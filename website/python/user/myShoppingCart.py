#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'Administrator'

from django.http import HttpRequest
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
import random

from website import models
from website.python.common.response import Responses
from website.python.user.userInfo import UserInfo
from modernLamps import settings

'''
根据用户请求，ShoppingCart表增删改查
'''

class ShoppingCartInfo(object):

    #管理请求端口,分发任务
    @classmethod
    def shoppingCartRequestPortManager(cls, request=HttpRequest()):
        #检测是否登录
        isLogin, account = UserInfo.checkIsLogin(request);
        if isLogin == True:
            if request.method == 'POST':
                operation = request.POST.get('operation', None);
                if operation == 'add':
                    return cls.addShoppingCart(request, account);
                elif operation == 'delete':
                    return cls.deleteShoppingCart(request, account);
                elif operation == 'modify':
                    return cls.modifyShoppingCart(request, account);
                elif operation == 'checkBox':
                    #修改商品是否选中
                    return cls.modifyCheckBox(request, account);
                elif operation == 'checkBoxAll':
                    return cls.modifyCheckBoxAll(request, account);
                else:
                    return Responses.responseJsonArray('fail', 'operation有误');
            elif request.method == 'GET':
                operation = request.GET.get('operation', None);
                if operation == 'get':
                    return cls.getShoppingCart(request, account);
                elif operation == 'checkStock':
                    return cls.checkStock(request, account);
                else:
                    return Responses.responseJsonArray('fail', 'operation有误');
            else:
                return Responses.responseJsonArray('fail', '请使用get或post请求');
        else:
            return Responses.responseJsonArray('fail', '未登录');

    #检查库存
    @classmethod
    def checkStock(cls, request=HttpRequest(), account='0'):
        try:
            goodsList = models.ShoppingCartTable.objects.filter(account=account, isSelect=True);
            if goodsList:
                for obj in goodsList:
                    goods = models.GoodsTable.objects.get(goodsId=obj.goodsId);
                    if obj.count > goods.inventoryCount:
                        return Responses.responseJsonArray('fail', '存在库存不足');  #库存不足
                return Responses.responseJsonArray('success', '库存充足');  #库存足
            else:
                return Responses.responseJsonArray('fail', '存在库存不足');  #库存不足
        except Exception, e:
                return Responses.responseJsonArray('fail', '数据异常');

    #修改商品是否选中
    @classmethod
    def modifyCheckBox(cls, request=HttpRequest(), account='0'):

        goodsId = request.POST.get('goodsId', None);
        try:
            goodsList = models.ShoppingCartTable.objects.filter(goodsId=goodsId, account=account);
            goods = goodsList[0];
            if goods:
                if goods.isSelect:   #本身是选中的则是不选中
                    models.ShoppingCartTable.objects.filter(goodsId=goodsId, account=account).update(isSelect=False);
                else:
                    models.ShoppingCartTable.objects.filter(goodsId=goodsId, account=account).update(isSelect=True);
            else:
                return Responses.responseJsonArray('fail', '商品已失效');

            results = models.ShoppingCartTable.objects.filter(account=account);
            allSelect = True;
            totalPrice = 0;  #总额
            if results:
                for obj in results:
                    if not obj.isSelect:
                        allSelect = False;
                    if obj.isSelect:
                        totalPrice += float(obj.sumPrice);

            data = [{'totalPrice' : totalPrice}];
            if allSelect:
                return Responses.responseJsonArray('success', '全选', data);
            else:
                return Responses.responseJsonArray('fail', '未全选', data);
        except Exception, e:
            return Responses.responseJsonArray('fail', '数据异常');

    #全选
    @classmethod
    def modifyCheckBoxAll(cls, request=HttpRequest(), account='0'):
        try:
            results = models.ShoppingCartTable.objects.filter(account=account);
            allSelect = True;
            totalPrice = 0;  #总额
            if results:
                for obj in results:
                    totalPrice += float(obj.sumPrice);  #这里计算所有的总额
                    if not obj.isSelect:
                        allSelect = False;

            data = [{'totalPrice' : totalPrice}];
            if allSelect:
                #全不选所有
                models.ShoppingCartTable.objects.filter(account=account).update(isSelect=False);
                return Responses.responseJsonArray('fail', '未全选', [{'totalPrice' : 0 }]);
            else:
                models.ShoppingCartTable.objects.filter(account=account).update(isSelect=True);
                return Responses.responseJsonArray('success', '全选', data);
        except Exception, e:
            return Responses.responseJsonArray('fail', '数据异常');

    #添加shoppingCart
    @classmethod
    def addShoppingCart(cls, request=HttpRequest(), account='0'):

        try:
            count = int(request.POST.get('count', '1'));
            goodsId = request.POST.get('goodsId', None);
            isSelect = True;
        except Exception, e:
            goodsId = request.POST.get('goodsId', None);
            isSelect = True;
            count = 1;

        if count <= 1:
            count = 1;

        try:
            #检查购物车里面是否有
            results = models.ShoppingCartTable.objects.filter(goodsId=goodsId, account=account);
            if results:
                count = results[0].count + count;  #增加

            #检查商品是否失效
            goodsResult = models.GoodsTable.objects.get(goodsId=goodsId);
            if goodsResult:
                sumPrice = float(goodsResult.price) * count;  #计算总价
            else:
                return Responses.responseJsonArray('fail', '商品已失效');

            data = {
                    'count' : count,
                    'sumPrice' : str(sumPrice),
                    'account' : account,
                    'goodsId' : goodsId,
                    'isSelect' : isSelect
                }

            if results:
                #更新
                models.ShoppingCartTable.objects.filter(goodsId=goodsId, account=account).update(**data);
                return Responses.responseJsonArray('success', '更新成功');
            else:
                #增加
                result = models.ShoppingCartTable.objects.create(**data);
                if result:
                    data = [];
                    data.append(model_to_dict(result));
                    return Responses.responseJsonArray('success', '添加成功', data);
                else:
                    return Responses.responseJsonArray('fail', '添加失败');

        except Exception, e:
            return Responses.responseJsonArray('fail', '数据异常');


    @classmethod
    def deleteShoppingCart(cls, request=HttpRequest(), account='0'):
        goodsId = request.POST.get('goodsId', None);
        try:
            models.ShoppingCartTable.objects.filter(goodsId=goodsId, account=account).delete();
            results = models.ShoppingCartTable.objects.filter(account=account, isSelect=True);
            totalPrice = 0;
            if results:
                for obj in results:
                    totalPrice += float(obj.sumPrice);
            data = [{'totalPrice' : totalPrice}];
            return Responses.responseJsonArray('success', '删除成功', data);
        except Exception, e:
            return Responses.responseJsonArray('fail', '删除失败');

    @classmethod
    def modifyShoppingCart(cls, request=HttpRequest(), account='0'):

        try:
            goodsId = request.POST.get('goodsId', None);
            isSelect = request.POST.get('isSelect', None);
            count = int(request.POST.get('count', '1'));
            if count <= 1:
                count = 1
        except Exception, e:
            isSelect = True;
            count=1

        try:

            #检查商品是否失效，库存
            goodsResult = models.GoodsTable.objects.get(goodsId=goodsId);
            if goodsResult:
                if goodsResult.inventoryCount >= count:
                    sumPrice = float(goodsResult.price) * count;  #计算总价
                else:
                    return Responses.responseJsonArray('fail', '库存不足');
            else:
                return Responses.responseJsonArray('fail', '商品已失效');

            dic = {}
            if count:
                dic['count'] = count;
            if sumPrice:
                dic['sumPrice'] = str(sumPrice);
            if isSelect:
                dic['isSelect'] = isSelect;

            condition = {
                'goodsId':goodsId,
                'account':account
            };
            #更新
            models.ShoppingCartTable.objects.filter(**condition).update(**dic);
            #更新完毕，返回数据
            results = models.ShoppingCartTable.objects.filter(account=account);
            totalPrice = 0;
            for goods in results:
                if goods.isSelect:
                    totalPrice += float(goods.sumPrice);
            dic['totalPrice'] = totalPrice;
            return Responses.responseJsonArray('success', '更新成功', [dic]);

        except Exception, e:
            return Responses.responseJsonArray('fail', '更新失败');

    @classmethod
    def getShoppingCart(cls, request=HttpRequest(), account='0'):

        try:
            page = int(request.GET.get('page', '1'));
            pageSize = int(request.GET.get('pageSize', '20'));
            isSelect = bool(request.GET.get('isSelect', True));
        except ValueError, e:
            page = 1;
            pageSize = 20;
            isSelect = False;

        if page <= 1:
            page = 1;
        if pageSize <= 1:
            pageSize = 1;

        condition = {
            'isSelect' : isSelect,
            'account' : account
        }
        data = cls.getShoppingCartData(page, pageSize, condition);
        if data:
            return Responses.responseJsonArray('success', '请求成功', data);
        else:
            return Responses.responseJsonArray('fail', '没有数据');

    #获取购物车数据
    @classmethod
    def getShoppingCartData(cls, page, pageSize, condition={}):
        try:
            results = models.ShoppingCartTable.objects.filter(**condition).order_by("-id");
            if results.count():
                paginator = Paginator(results, pageSize);  #分页
                try:
                    results = paginator.page(page);
                except Exception ,e:
                    results = paginator.page(paginator.num_pages);
                data = [];
                for obj in results:   #模型转字典
                    dict = model_to_dict(obj);
                    data.append(dict);
                return data;
            else:
                return None;
        except:
            return None;