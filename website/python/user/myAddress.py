#coding:utf8
# __author__ = 'fenton-fd.zhu'

from django.http import HttpRequest
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.db import transaction
import random

from website import models
from website.python.common.response import Responses
from website.python.user.userInfo import UserInfo
from modernLamps import settings

'''
根据用户请求，address数据增删改查
'''

class AddressInfo(object):

    #管理请求端口,分发任务
    @classmethod
    def addressRequestPortManager(cls, request=HttpRequest()):
        #检测是否登录
        isLogin, account = UserInfo.checkIsLogin(request);
        if isLogin == True:
            if request.method == 'POST':
                operation = request.POST.get('operation', None);
                if operation == 'add':
                    return cls.addAddress(request, account);
                elif operation == 'modify':
                    return cls.modifyAddress(request, account);
                elif operation == 'delete':
                    return cls.deleteAddress(request, account);
                else:
                    return Responses.responseJsonArray('fail', 'operation有误');
            elif request.method == 'GET':
                operation = request.GET.get('operation', None);
                if operation == 'get':
                    return cls.getAddress(request, account);
                else:
                    return Responses.responseJsonArray('fail', 'operation有误');
            else:
                return Responses.responseJsonArray('fail', '请使用get或post请求');
        else:
            return Responses.responseJsonArray('fail', '未登录');

    #添加地址
    @classmethod
    def addAddress(cls, request=HttpRequest(), account='0'):
        addressId = '00000';
        while True:
            addressId = str(random.randint(10000, 60000));
            if not models.AddressTable.objects.get(addressId=addressId):
                break;
        data = {
                    'addressId' : addressId,
                    'account' : account,
                    'contact' : request.POST.get('contact', None),
                    'phoneNumber' : request.POST.get('phoneNumber', None),
                    'address' : request.POST.get('address', None),
                    'defaults' : False
                }
        try:
            count = models.AddressTable.objects.all().count();
            if count==0:
                data['defaults'] = True;
            result = models.AddressTable.objects.create(**data);
            if result:
                data = [{model_to_dict(result)}];
                return Responses.responseJsonArray('success', '添加成功', data);
        except Exception, e:
            return Responses.responseJsonArray('fail', '添加失败,请重试');

    @classmethod
    def deleteAddress(cls, request=HttpRequest(), account='0'):
        addressId = request.POST.get('addressId', None);
        try:
            result = models.AddressTable.objects.filter(addressId=addressId, account=account).delete();
            if result:
                return Responses.responseJsonArray('success', '删除成功');
            else:
                return Responses.responseJsonArray('fail', '删除失败');
        except Exception, e:
            return Responses.responseJsonArray('fail', '删除失败');

    @classmethod
    def modifyAddress(cls, request=HttpRequest(), account='0'):
        addressId = request.POST.get('addressId', None),
        if not addressId:
            return Responses.responseJsonArray('fail', '没有addressId');

        data = {
                    'addressId' : request.POST.get('addressId', None),
                    'account' : account,
                    'contact' : request.POST.get('contact', None),
                    'phoneNumber' : request.POST.get('phoneNumber', None),
                    'address' : request.POST.get('address', None),
                    'defaults' : request.POST.get('defaults', None)
                }
        try:
            with transaction.atomic():
                if data['defaults'] == True:
                    models.AddressTable.objects.all().update(defaults=False);
                models.AddressTable.objects.filter(addressId=addressId, account=account).update(**data);
                return Responses.responseJsonArray('success', '修改成功');
        except Exception, e:
            return Responses.responseJsonArray('fail', '修改失败');

    @classmethod
    def getAddress(cls, request=HttpRequest(), account='0'):

        try:
            condition = {
                'addressId' : request.GET.get('addressId', None),
                'defaults' : request.GET.get('defaults', None),
                'account' : request.GET.get('addressId', None)
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
            results = models.AddressTable.objects.filter(**condition).order_by("id");
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