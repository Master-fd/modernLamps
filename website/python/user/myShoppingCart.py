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
                else:
                    return Responses.responseJsonArray('fail', 'operation有误');
            elif request.method == 'GET':
                operation = request.GET.get('operation', None);
                if operation == 'get':
                    return cls.getShoppingCart(request, account);
                else:
                    return Responses.responseJsonArray('fail', 'operation有误');
            else:
                return Responses.responseJsonArray('fail', '请使用get或post请求');
        else:
            return Responses.responseJsonArray('fail', '未登录');

    #添加shoppingCart
    @classmethod
    def addShoppingCart(cls, request=HttpRequest(), account='0'):

        count = int(request.POST.get('count', '1'));
        goodsId = request.POST.get('goodsId', None);
        isSelect = True;

        if count <= 1:
            count = 1
        try:
            #检查购物车里面是否有
            result = models.ShoppingCartTable.objects.get(goodsId=goodsId, account=account);
            if result:
                count = result.count + count;  #增加

            #检查商品是否失效，库存
            goodsResult = models.GoodsTable.objects.get(goodsId=goodsId);
            if goodsResult:
                if goodsResult.inventoryCount >= count:
                    sumPrice = float(goodsResult.price) * count;  #计算总价
                else:
                    return Responses.responseJsonArray('fail', '库存不足');
            else:
                return Responses.responseJsonArray('fail', '商品已失效');

            data = {
                    'count' : count,
                    'sumPrice' : sumPrice,
                    'account' : account,
                    'goodsId' : goodsId,
                    'isSelect' : isSelect
                }

            if result:
                #更新
                result = models.ShoppingCartTable.objects.filter(goodsId=goodsId, account=account).update(**data);
                if result:
                    data = [{model_to_dict(result)}];
                    return Responses.responseJsonArray('success', '更新成功', data);
                else:
                    return Responses.responseJsonArray('fail', '更新失败,请重试');
            else:
                #增加
                result = models.ShoppingCartTable.objects.create(**data);
                if result:
                    data = [{model_to_dict(result)}];
                    return Responses.responseJsonArray('success', '添加成功', data);
                else:
                    return Responses.responseJsonArray('fail', '添加失败,请重试');

        except Exception, e:
            return Responses.responseJsonArray('fail', '添加失败,请重试');


    @classmethod
    def deleteShoppingCart(cls, request=HttpRequest(), account='0'):
        goodsId = request.POST.get('goodsId', None);
        try:
            result = models.ShoppingCartTable.objects.filter(goodsId=goodsId, account=account).delete();
            if result:
                return Responses.responseJsonArray('success', '删除成功');
            else:
                return Responses.responseJsonArray('fail', '删除失败');
        except Exception, e:
            return Responses.responseJsonArray('fail', '删除失败');

    @classmethod
    def modifyShoppingCart(cls, request=HttpRequest(), account='0'):

        count = int(request.POST.get('count', '1'));
        goodsId = request.POST.get('goodsId', None);
        isSelect = True;
        if count <= 1:
            count = 1

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

            data = {
                    'count' : count,
                    'account' : account,
                    'goodsId' : goodsId,
                    'sumPrice' : sumPrice,
                    'isSelect' : isSelect
                }

            #检查是否在购物车中
            result = models.ShoppingCartTable.objects.get(goodsId=goodsId, account=account);
            if result:
                #更新
                result = models.ShoppingCartTable.objects.filter(goodsId=goodsId, account=account).update(**data);
            else:
                #添加
                result = models.ShoppingCartTable.objects.create(**data);

            if result:
                data = [{model_to_dict(result)}];
                return Responses.responseJsonArray('success', '更新成功', data);
            else:
                return Responses.responseJsonArray('fail', '更新失败,请重试');

        except Exception, e:
            return Responses.responseJsonArray('fail', '更新失败');

    @classmethod
    def getShoppingCart(cls, request=HttpRequest(), account='0'):

        try:
            condition = {
            'goodsId' : request.GET.get('goodsId', None),
            'account' : request.GET.get('account', None)
        };
            page = int(request.GET.get('page', '1'));
            pageSize = int(request.GET.get('pageSize', '20'));
        except ValueError, e:
            page = 1;
            pageSize = 20;

        if page <= 1:
            page = 1;
        if pageSize <= 1:
            pageSize = 1;

        try:
            results = models.ShoppingCartTable.objects.filter(**condition).order_by("id");
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
                return Responses.responseJsonArray('success', '请求成功', data);
            else:
                return Responses.responseJsonArray('fail', '没有数据');
        except:
            return Responses.responseJsonArray('fail', '请求异常');