#coding:utf8
# __author__ = 'fenton-fd.zhu'

from django.http import HttpRequest
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
import random

from website import models
from website.python.common.response import Responses
from website.python.user.userInfo import UserInfo
from modernLamps import settings

'''
根据用户请求，collect数据增删改查
'''

class CollectInfo(object):

    #管理请求端口,分发任务
    @classmethod
    def collectRequestPortManager(cls, request=HttpRequest()):
        #检测是否登录
        isLogin, account = UserInfo.checkIsLogin(request);
        if isLogin == True:
            if request.method == 'POST':
                operation = request.POST.get('operation', None);
                if operation == 'add':
                    return cls.addCollect(request, account);
                elif operation == 'modify':
                    return cls.modifyCollect(request, account);
                elif operation == 'delete':
                    return cls.deleteCollect(request, account);
                else:
                    return Responses.responseJsonArray('fail', 'operation有误');
            elif request.method == 'GET':
                operation = request.GET.get('operation', None);
                if operation == 'get':
                    return cls.getCollect(request, account);
                else:
                    return Responses.responseJsonArray('fail', 'operation有误');
            else:
                return Responses.responseJsonArray('fail', '请使用get或post请求');
        else:
            return Responses.responseJsonArray('fail', '未登录');

    #添加地址
    @classmethod
    def addCollect(cls, request=HttpRequest(), account='0'):
        collectId = '00000';
        while True:
            CollectId = str(random.randint(10000, 60000));
            if not models.GoodsTable.objects.get(collectId=collectId):
                break;
        data = {
                    'collectId' : collectId,
                    'account' : account,
                    'goodsId' : request.POST.get('goodsId', None),
                }
        try:
            count = models.CollectTable.objects.all().count();
            if count==0:
                data['defaults'] = True;
            result = models.AddressTable.objects.create(**data);
            if result:
                data = [model_to_dict(result)];
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
            if data['defaults'] == True:
                result = models.AddressTable.objects.all().update(defaults=False);
            if result:
                result = models.AddressTable.objects.filter(addressId=addressId, account=account).update(**data);
                if result:
                    return Responses.responseJsonArray('success', '修改成功');
                else:
                    return Responses.responseJsonArray('fail', '修改失败');
            else:
                return Responses.responseJsonArray('fail', '修改失败');
        except Exception, e:
            return Responses.responseJsonArray('fail', '修改失败');

    @classmethod
    def getAddress(cls, request=HttpRequest(), account='0'):
        condition = {
            'addressId' : request.GET.get('addressId', None),
            'defaults' : request.GET.get('defaults', None),
            'account' : request.GET.get('addressId', None)
        };

        try:
            results = models.AddressTable.objects.filter(**condition);
            if results:
                data=[];
                for obj in results:
                    dic = model_to_dict(obj);
                    data.append(dic);
                return Responses.responseJsonArray('success', '获取成功', data);
            else:
                return Responses.responseJsonArray('fail', '没有地址');
        except Exception, e:
            return Responses.responseJsonArray('fail', '没有地址');