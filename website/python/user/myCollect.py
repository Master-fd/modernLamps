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

    #添加collect
    @classmethod
    def addCollect(cls, request=HttpRequest(), account='0'):
        collectId = '00000';
        try:
            while True:
                collectId = str(random.randint(10000, 60000));
                if not models.CollectTable.objects.get(collectId=collectId):
                    break;
        except Exception, e:
            return Responses.responseJsonArray('fail', '添加失败,请重试');

        goodsId = request.POST.get('goodsId', None);
        data = {
                    'collectId' : collectId,
                    'account' : account,
                    'goodsId' : goodsId
                }
        try:
            result = models.CollectTable.objects.get(goodsId=goodsId);
            if result:
                return Responses.responseJsonArray('fail', '已存在');
            result = models.CollectTable.objects.create(**data);
            if result:
                data = [{model_to_dict(result)}];
                return Responses.responseJsonArray('success', '添加成功', data);
            else:
                return Responses.responseJsonArray('fail', '添加失败,请重试');
        except Exception, e:
            return Responses.responseJsonArray('fail', '添加失败,请重试');

    @classmethod
    def deleteCollect(cls, request=HttpRequest(), account='0'):
        collectId = request.POST.get('collectId', None);
        try:
            result = models.CollectTable.objects.filter(collectId=collectId, account=account).delete();
            if result:
                return Responses.responseJsonArray('success', '删除成功');
            else:
                return Responses.responseJsonArray('fail', '删除失败');
        except Exception, e:
            return Responses.responseJsonArray('fail', '删除失败');

    @classmethod
    def getCollect(cls, request=HttpRequest(), account='0'):

        try:
            condition = {
            'collectId' : request.GET.get('collectId', None),
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
            results = models.CollectTable.objects.filter(**condition).order_by("id");
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