#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'Administrator'

from django.http import HttpRequest
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.db import transaction, IntegrityError     #事务操作
from django.db.transaction import TransactionManagementError
import random

from website import models
from website.python.common.response import Responses
from website.python.user.userInfo import UserInfo
from modernLamps import settings

'''
根据用户请求，order数据增删改查
'''

class OrderInfo(object):

    #管理请求端口,分发任务
    @classmethod
    def orderRequestPortManager(cls, request=HttpRequest()):
        #检测是否登录
        isLogin, account = UserInfo.checkIsLogin(request);
        if isLogin == True:
            if request.method == 'POST':
                operation = request.POST.get('operation', None);
                if operation == 'add':
                    return cls.addOrder(request, account);
                elif operation == 'modify':
                    return cls.modifyOrder(request, account);
                elif operation == 'delete':
                    return cls.deleteOrder(request, account);
                else:
                    return Responses.responseJsonArray('fail', 'operation有误');
            elif request.method == 'GET':
                operation = request.GET.get('operation', None);
                if operation == 'get':
                    return cls.getOrder(request, account);
                else:
                    return Responses.responseJsonArray('fail', 'operation有误');
            else:
                return Responses.responseJsonArray('fail', '请使用get或post请求');
        else:
            return Responses.responseJsonArray('fail', '未登录');


    @classmethod
    def addOrder(cls, request=HttpRequest(), account='0'):
        #产生订单号
        orderId = '00000';
        try:
            while True:
                orderId = str(random.randint(10000, 60000));
                if not models.UserOrderTable.objects.get(orderId=orderId) and models.ManagerOrderTable.objects.get(orderId=orderId):
                    break;
        except Exception, e:
            return Responses.responseJsonArray('fail', '添加失败,请重试');

        #封装数据
        data = {
                    'orderId' : orderId,
                    'account' : account,
                    'status' : 'new',
                    'phoneNumber' : request.POST.get('phoneNumber', None),
                    'order' : request.POST.get('order', None),
                    'contact' : request.POST.get('contact', None),
                }


        try:
            #一个订单有多个goods
            goodsIds = request.POST.get('goodsIds', None);
            counts = request.POST.get('counts', None),
            if len(goodsIds) != len(counts):
                return Responses.responseJsonArray('fail', '添加失败,请重试');

            #开启一个事务，增加订单，库存减少，购物车删除
            with transaction.atomic():
                totalPrice = 0;
                for (goodsId, count) in zip(goodsIds, counts):
                    #查找goods看看是否失效
                    result = models.GoodsTable.objects.get(goodsId=goodsId);
                    if result and result.inventoryCount >= count:
                        sumPrice = float(result.price) * count;
                        totalPrice += sumPrice;
                        goods = {'account' : account,
                                'orderId' : orderId,
                                'goodsId' : goodsId,
                                'count' : count,
                                'sumPrice' : sumPrice};
                        models.OrderTable.objects.create(**goods);  #添加数据
                    else:
                        #订单无效, 抛出事务异常
                        raise TransactionManagementError;
                #清空购物车
                models.ShoppingCartTable.objects.filter(account=account).delete();
                #增加订单
                data['totalPrice'] = str(totalPrice);
                models.UserOrderTable.objects.create(**data);
                models.ManagerOrderTable.objects.create(**data);
                return Responses.responseJsonArray('success', '添加成功');
        except Exception, e:
            return Responses.responseJsonArray('fail', '添加失败');

    @classmethod
    def deleteOrder(cls, request=HttpRequest(), account='0'):
        orderId = request.POST.get('orderId', None);
        try:
            #查看是否为超级用户
            result = models.UsersTable.get(account=account);
            if result.superUser == True:
                #管理员
                result = models.ManagerOrderTable.objects.get(orderId=orderId).delete();
            else:  #普通用户
                result = models.UserOrderTable.objects.get(orderId=orderId).delete();
            if result:
                return Responses.responseJsonArray('success', '删除成功');
            else:
                return Responses.responseJsonArray('fail', '删除失败');
        except Exception, e:
            return Responses.responseJsonArray('fail', '删除失败');

    @classmethod
    def modifyOrder(cls, request=HttpRequest(), account='0'):
        orderId = request.POST.get('orderId', None),
        if not orderId:
            return Responses.responseJsonArray('fail', '没有orderId');

        data = {'status' : request.POST.get('status', None)};

        try:
            #开启事务
            with transaction.atomic():
                models.UserOrderTable.objects.filter(orderId=orderId, account=account).update(**data)
                models.ManagerOrderTable.objects.filter(addressId=orderId, account=account).update(**data);
                return Responses.responseJsonArray('success', '修改成功');
        except Exception, e:
            return Responses.responseJsonArray('fail', '修改失败');

    @classmethod
    def getOrder(cls, request=HttpRequest(), account='0'):

        try:
            condition = {
                'orderId' : request.GET.get('orderId', None),
                'status' : request.GET.get('status', None)
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
             #查看是否为超级用户
            result = models.UsersTable.get(account=account);
            if result.superUser == True:
                #管理员
                results = models.ManagerOrderTable.objects.filter(**condition).order_by("id");
            else:
                results = models.UserOrderTable.objects.filter(**condition).order_by("id");
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
