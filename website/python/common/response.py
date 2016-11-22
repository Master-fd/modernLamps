#coding:utf8
# __author__ = 'fenton-fd.zhu'

'''
请求响应数据
'''
from django.shortcuts import HttpResponse, HttpResponseRedirect, render_to_response
from django.http import Http404
import json
from modernLamps import settings
from datetime import datetime


class Responses(object):
    #以json的方式响应,数据data是数组
    @classmethod
    def responseJsonArray(cls, status="success", message="请求成功", data=[]):
        dict = {
            'status' : status,
            'message' : message,
            'data' : data
        };
        return HttpResponse(json.dumps(dict, cls=DateEncoder));

    #以json的方式响应,数据data是字典
    @classmethod
    def responseJsonDict(cls, status="success", message="请求成功", data={}):
        dict = {
            'status' : status,
            'message' : message,
            'data' : data
        };
        return HttpResponse(json.dumps(dict, cls=DateEncoder));

    #渲染返回页面,同时返回login
    @classmethod
    def returnDrawPage(cls, isLogin, page, dictName, data):
        dataDict = {
            'isLogin' : json.dumps(isLogin),
            dictName : data
        };
        return render_to_response(page, dataDict);


    #渲染返回后台类页面，需要先check用户是否login
    @classmethod
    def returnCheckLoginDrawPage(cls, isLogin, page, dictName, data):
        if isLogin:
            return cls.returnDrawPage(isLogin, page, dictName, data);
        else:
            #未login，从定向到home页
            return HttpResponseRedirect(settings.BASE_URL);

#json默认只能dump一些基本的类，例如数组之类的，对于日期和自定义的类是无法dump的，需要我们自己写
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.__str__();

        return json.JSONEncoder.default(self, obj);
