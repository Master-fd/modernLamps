#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'Administrator'

from django.http import HttpRequest
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.db import transaction, IntegrityError     #事务操作
from django.db.transaction import TransactionManagementError
import random
import json

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
                if operation == None:  #有可能传递过来的是json
                    try:
                        result = json.loads(request.body);
                        operation = result['operation'];
                    except Exception, e:
                        return Responses.responseJsonArray('fail', 'operation无法获取');

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
                if not models.UserOrderTable.objects.filter(orderId=orderId):
                    break;
        except Exception, e:
            return Responses.responseJsonArray('fail', '产生订单号失败');

        jsonResult = json.loads(request.body);   #获取json数据
        phoneNumber = '';
        address = '';
        contact = '';
        print jsonResult
        #获取地址
        try:
            addressId = jsonResult.get('addressId', None);
            result = models.AddressTable.objects.filter(account=account, addressId=addressId);
            if result:
                addr = result[0];
                phoneNumber = addr.phoneNumber;
                address = addr.address;
                contact = addr.contact;
        except Exception, e:
            return Responses.responseJsonArray('fail', '没有填写地址');

        #封装数据
        data = {
                    'orderId' : orderId,
                    'account' : account,
                    'status' : 'new',
                    'phoneNumber' : phoneNumber,
                    'address' : address,
                    'contact' : contact,
                    'totalPrice' : jsonResult.get('totalPrice', None)
                };

        try:
            #一个订单有多个goods
            goodsList = jsonResult.get('goodsList', None);
            buyNow = jsonResult.get('buyNow', None);

            #开启一个事务，增加订单，库存减少，购物车删除
            if not goodsList:
                return Responses.responseJsonArray('fail', '没有商品');
            with transaction.atomic():
                for goods in goodsList:
                    #查找goods看看是否失效
                    result = models.GoodsTable.objects.get(goodsId=goods['goodsId']);
                    if result and result.inventoryCount >= goods['count']:
                        goods = {'account' : account,
                                'orderId' : orderId,
                                'goodsId' : goods['goodsId'],
                                'count' : goods['count'],
                                'sumPrice' : goods['sumPrice']};
                        models.OrderTable.objects.create(**goods);  #添加数据到order goods表
                        inventoryCount = result.inventoryCount-goods['count'];
                        saleCount = result.saleCount+goods['count'];
                        condition = {
                            'inventoryCount' : inventoryCount,
                            'saleCount' : saleCount
                        }
                        models.GoodsTable.objects.filter(goodsId=goods['goodsId']).update(**condition);
                    else:
                        #订单无效, 抛出事务异常
                        raise TransactionManagementError;
                if not buyNow:
                    models.ShoppingCartTable.objects.filter(account=account).delete();  #清空购物车
                #增加订单
                models.UserOrderTable.objects.create(**data);
                return Responses.responseJsonArray('success', '添加成功');
        except Exception, e:
            return Responses.responseJsonArray('fail', '添加失败');

    @classmethod
    def deleteOrder(cls, request=HttpRequest(), account='0'):
        orderId = request.POST.get('orderId', None);
        try:
            #查看是否为超级用户
            result = models.UsersTable.objects.get(account=account);
            if result.superUser == True:
                #管理员
                result = models.UserOrderTable.objects.filter(orderId=orderId).update(managerDelete=True);
            else:  #普通用户
                result = models.UserOrderTable.objects.filter(orderId=orderId).update(userDelete=True);

            result = models.UserOrderTable.objects.get(orderId=orderId);
            if result.userDelete and result.managerDelete:  #如果用户和管理员都删除了，才真正的删除
                models.UserOrderTable.objects.get(orderId=orderId).delete();

            return Responses.responseJsonArray('success', '删除成功');
        except Exception, e:
            return Responses.responseJsonArray('fail', '删除失败');

    @classmethod
    def modifyOrder(cls, request=HttpRequest(), account='0'):
        orderId = request.POST.get('orderId', None);
        if not orderId:
            return Responses.responseJsonArray('fail', '没有orderId');
        status = request.POST.get('status', None);
        company = request.POST.get('company', None);
        expressId = request.POST.get('expressId', None);
        condition = {};
        if status:
            condition['status'] = status;
        if status:
            condition['company'] = company;
        if status:
            condition['expressId'] = expressId;
        try:
            if status:
                #开启事务
                with transaction.atomic():
                    models.UserOrderTable.objects.filter(orderId=orderId).update(**condition)
                    return Responses.responseJsonArray('success', '修改成功', [condition]);
            else:
                return Responses.responseJsonArray('fail', '没有对应订单');
        except Exception, e:
            return Responses.responseJsonArray('fail', '修改失败');

    @classmethod
    def getOrder(cls, request=HttpRequest(), account='0'):

        try:
            page = int(request.GET.get('page', '1'));
            pageSize = int(request.GET.get('pageSize', '20'));
        except ValueError, e:
            page = 1;
            pageSize = 20;

        if page <= 1:
            page = 1;
        if pageSize <= 1:
            pageSize = 1;

        condition = {};
        if request.GET.get('orderId', None):
            condition['orderId'] = request.GET.get('orderId', None);
        if request.GET.get('status', None):
            condition['status'] = request.GET.get('status', None);

        data, pageResult = cls.getOrderData(page, pageSize, account, condition);
        if data:
            return Responses.responseJsonArray('success', '请求成功', data);
        else:
            return Responses.responseJsonArray('fail', '没有数据');

    @classmethod
    def getOrderData(cls, page, pageSize, account, condition={}):
        try:
             #查看是否为超级用户
            result = models.UsersTable.objects.get(account=account);
            if result.superUser == True:
                #管理员
                condition['managerDelete'] = False;
            else:
                condition['userDelete'] = False;
            results = models.UserOrderTable.objects.filter(**condition).order_by("-id");

            if results:
                paginator = Paginator(results, pageSize);  #分页
                try:
                    results = paginator.page(page);
                except Exception ,e:
                    results = paginator.page(paginator.num_pages);
                data = [];
                for obj in results:   #模型转字典
                    dict = model_to_dict(obj);
                    dict['createDate'] = obj.createDate;
                    dict['createDate'] = obj.updateDate;   #model_to_dict无法转换时间，需要手动转
                    # dict['status'] = obj.get_status_display;   #获取状态显示,这种只能直接渲染模板，无法使用json，dumps
                    data.append(dict);
                return data, results;  #返回数组
            else:
                return None, None;
        except:
            return None, None;
