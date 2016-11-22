#coding:utf8
# __author__ = 'fenton-fd.zhu'

from django.http import HttpRequest
from django.shortcuts import render_to_response
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
import random
import os

from website import models
from website.python.common.response import Responses
from website.python.tools.uploader import Uploader
from modernLamps import settings

'''
根据用户请求，goods数据增删改查
'''

class GoodsInfo(object):

    #管理请求端口,分发任务
    @classmethod
    def goodsRequestPortManager(cls, request=HttpRequest()):
        if request.method == 'POST':
            operation = request.POST.get('operation', None);
            if operation == 'add':
                return cls.addGoods(request);
            elif operation == 'modify':
                return cls.modifyGoods(request);
            elif operation == 'delete':
                return cls.deleteGoods(request);
            else:
                return Responses.responseJsonArray('fail', 'operation有误');
        elif request.method == 'GET':
            operation = request.GET.get('operation', None);
            if operation == 'get':
                return cls.getGoods(request);
            else:
                return Responses.responseJsonArray('fail', 'operation有误');
        else:
            return Responses.responseJsonArray('fail', '请使用get或post请求');


    #分页查找商品,返回json
    @classmethod
    def getGoods(cls, request=HttpRequest()):
        try:
            goodsName = request.GET.get('goodsName', None);
            goodsId = request.GET.get('goodsId', None);
            subClass = request.GET.get('subClass', None);
            page = int(request.GET.get('page', '1'));
            pageSize = int(request.GET.get('pageSize', '20'));
        except ValueError, e:
            page = 1;
            pageSize = 20;

        if page <= 1:
            page = 1;
        if pageSize <= 20:
            pageSize


        condition = {};
        if goodsName:
            condition['goodsName'] = goodsName;
        if goodsId:
            condition['goodsId'] = goodsId;
        if subClass:
            condition['subClass'] = subClass;
        data, pageResult = cls.getGoodsData(page, pageSize, condition);
        if data:
            return Responses.responseJsonArray('success', '请求成功', data);
        else:
            return Responses.responseJsonArray('fail', '没有数据');

    #搜索商品, 正则匹配
    @classmethod
    def searchGoods(cls, page, pageSize, goodsName):
        try:
            data = [];
            results = models.GoodsTable.objects.filter(goodsName__icontains=goodsName);
            paginator = Paginator(results, pageSize);  #分页
            if results:
                try:
                    results = paginator.page(page);
                except Exception ,e:
                    results = paginator.page(paginator.num_pages);
                for obj in results:
                    obj = model_to_dict(obj);
                    data.append(obj);
                return data;
            else:
                return None;
        except Exception, e:
            return None;

    #分页查找商品
    @classmethod
    def getGoodsData(cls, page=1, pageSize=20, condition={}):
        data = [];
        try:
            if condition:
                results = models.GoodsTable.objects.filter(**condition).order_by('-id');
            else:
                results = models.GoodsTable.objects.all().order_by('-id');
            if results:
                paginator = Paginator(results, pageSize);  #分页
                try:
                    results = paginator.page(page);
                except Exception ,e:
                    results = paginator.page(paginator.num_pages);

                for obj in results:   #模型转字典
                    goods = model_to_dict(obj);
                    goods['subClass'] = obj.get_subClass_display;
                    data.append(goods);
                return data, results;
            else:
                return None, None;
        except:
            return None, None;
    #删除商品
    @classmethod
    def deleteGoods(cls, request=HttpRequest()):
        try:
            goodsId = request.POST.get('goodsId', None);
        except Exception, e:
            return Responses.responseJsonArray('fail', '参数有误');

        try:
            models.GoodsTable.objects.filter(goodsId=goodsId).delete();
            return Responses.responseJsonArray('success', '删除成功');
        except Exception, e:
            return Responses.responseJsonArray('fail', '删除失败');

    #增加
    @classmethod
    def addGoods(cls, request=HttpRequest()):

        goodsId = '00000';
        try:   #产生goodsId
            while True:
                goodsId = str(random.randint(10000, 60000));
                if not models.GoodsTable.objects.filter(goodsId=goodsId).count():
                    break;
        except Exception, e:
            return Responses.responseJsonArray('fail', '添加失败,请重试');

        subClass = request.POST.get('subClass', "undefine");  #获取分类
        goodsName = request.POST.get('goodsName', None);
        if not goodsName:
            return Responses.responseJsonArray('fail', '商品名不能为空');
        price = request.POST.get('price', None);
        if not price:
            return Responses.responseJsonArray('fail', '价格不能为空');
        try:
            inventoryCount = int(request.POST.get('inventoryCount', '0'));
        except Exception, e:
            return Responses.responseJsonArray('fail', '库存非法');

        dirRoot = os.path.join(os.path.join(settings.MEDIA_GOODS_ROOT, subClass), goodsId);  #每次上传一个商品，用一个文件夹来保存，命名为media/goodsImage/分类/goodsId
        myUploder = Uploader(dirRoot);   #新建下载器

        data = {
                    'goodsId' : goodsId,
                    'goodsName' : goodsName,
                    'goodsDescUrl' : settings.BASE_URL + 'goodsInfo/' + goodsId,
                    'price' : price,
                    'description' : request.POST.get('description', None),
                    'freightCost' : request.POST.get('freightCost', '0'),
                    'saleCount' : 0,
                    'inventoryCount' : inventoryCount,
                    'subClass' : subClass,
                    'minImageUrl1' : myUploder.uploadFile(request.FILES.get('minImageUrl1', None)),
                    'minImageUrl2' : myUploder.uploadFile(request.FILES.get('minImageUrl2', None)),
                    'minImageUrl3' : myUploder.uploadFile(request.FILES.get('minImageUrl3', None)),
                    'descImageUrl1' : myUploder.uploadFile(request.FILES.get('descImageUrl1', None)),
                    'descImageUrl2' : myUploder.uploadFile(request.FILES.get('descImageUrl2', None)),
                    'descImageUrl3' : myUploder.uploadFile(request.FILES.get('descImageUrl3', None)),
                    'descImageUrl4' : myUploder.uploadFile(request.FILES.get('descImageUrl4', None)),
                    'descImageUrl5' : myUploder.uploadFile(request.FILES.get('descImageUrl5', None)),
                    'descImageUrl6' : myUploder.uploadFile(request.FILES.get('descImageUrl6', None)),
                    'descImageUrl7' : myUploder.uploadFile(request.FILES.get('descImageUrl7', None)),
                    'descImageUrl8' : myUploder.uploadFile(request.FILES.get('descImageUrl8', None)),
                    'descImageUrl9' : myUploder.uploadFile(request.FILES.get('descImageUrl9', None)),
                    'descImageUrl10' : myUploder.uploadFile(request.FILES.get('descImageUrl10', None)),
                    'aboutImageUrl' : myUploder.uploadFile(request.FILES.get('aboutImageUrl', None)),
                    'remarkImageUrl' :  myUploder.uploadFile(request.FILES.get('remarkImageUrl', None)),
                };

        try:
            result = models.GoodsTable.objects.create(**data);
            if result:
                return Responses.responseJsonArray('success', '上传成功');
            else:
                Responses.responseJsonArray('fail', '上传失败,请重试');
        except Exception, e:
            return Responses.responseJsonArray('faill', '上传失败,请重试');

