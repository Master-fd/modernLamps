#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'Administrator'

'''
每个订单的goodsid表操作
'''

from django.forms.models import model_to_dict
from django.core.paginator import Paginator

from website import models

class OrderGoodsInfo(object):


    #获取goodsid
    @classmethod
    def getOrderGoodsData(cls, account, condition={}):
        try:
            if account:
                condition['account'] = account;
            results = models.OrderTable.objects.filter(**condition).order_by('-id');
            if results:
                data = [];
                for obj in results:   #模型转字典
                    dict = model_to_dict(obj);
                    data.append(dict);
                return data;  #返回数组
            else:
                return None;
        except Exception, e:
            return None;




