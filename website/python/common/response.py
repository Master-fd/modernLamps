#coding:utf8
# __author__ = 'fenton-fd.zhu'

'''
请求响应数据
'''
from django.shortcuts import HttpResponse, HttpResponseRedirect, render_to_response
from django.http import Http404
import json

class Responses(object):
    #以json的方式响应,数据data是数组
    @classmethod
    def responseJsonArray(cls, status="success", message="请求成功", data=[]):
        dict = {
            'status' : status,
            'message' : message,
            'data' : data
        };
        return HttpResponse(json.dumps(dict));

    #以json的方式响应,数据data是字典
    @classmethod
    def responseJsonDict(cls, status="success", message="请求成功", data={}):
        dict = {
            'status' : status,
            'message' : message,
            'data' : data
        };
        return HttpResponse(json.dumps(dict));

    #渲染返回页面,同时返回login
    @classmethod
    def returnDrawPage(cls, isLogin, page, dictName, data):
        dataDict = {
            'isLogin' : json.dumps(isLogin),
            dictName : data
        };
        # if data:
        return render_to_response(page, dataDict);
        # else:
        #     raise Http404;

    #渲染返回后台类页面，需要先check用户是否login
    @classmethod
    def returnCheckLoginDrawPage(cls, isLogin, page, dictName, data):
        if isLogin:
            return cls.returnDrawPage(isLogin, page, dictName, data);
        else:
            #返回login 弹窗
            return cls.responseJsonArray('fail', '未登录');

