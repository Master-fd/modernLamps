#coding:utf8
# __author__ = 'fenton-fd.zhu'

'''
请求响应数据
'''
from django.shortcuts import HttpResponse, HttpResponseRedirect, render_to_response
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


