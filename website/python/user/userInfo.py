#coding:utf8
# __author__ = 'fenton-fd.zhu'

from django.http import HttpRequest,HttpResponse, HttpResponseRedirect
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
import random
import hashlib

from website import models
from website.python.common.response import Responses
from modernLamps import settings
from modernLamps import settings
'''
根据用户信息数据增删改查
'''
class UserInfo(object):

    #管理请求端口,分发任务
    @classmethod
    def userInfoRequestPortManager(cls, request=HttpRequest()):
        if request.method == 'POST':
            operation = request.POST.get('operation', None);
            if operation == 'register':   #注册
                return cls.__userRegister(request);
            elif operation == 'login':   # 登录
                return cls.__userLogin(request);
            elif operation == 'logout':  #注销
                return cls.__userLogout(request);
            elif operation == 'modify':
                return cls.__userModify(request);
            else:
                return Responses.responseJsonArray('fail', 'operation有误');
        elif request.method == 'GET':
            operation = request.GET.get('operation', None);
            if operation == 'getUserInfo':   #获取用户资料
                return cls.__getUserInfo(request);
            elif operation == 'superUser':  #判断用户是否是管理员
                return cls.checkIsSuperUser(request);
            elif operation == 'isLogin':
                isLogin, account = cls.checkIsLogin(request);
                if isLogin:
                    return Responses.responseJsonArray('success', '已登录', [{'isLogin': True,
                                                                           'account': account}]);
                else:
                    return Responses.responseJsonArray('fail', '未登录');
            else:
                return Responses.responseJsonArray('fail', 'operation有误');
        else:
            return Responses.responseJsonArray('fail', '请使用get或post请求');

    #检测账户密码输入合法性
    @classmethod
    def __inputDataCheck(cls, account, password):
        result = True;
        #判断合法性
        if not account:
            result = "账户不能为空";
        if not password:
            result = "密码不能为空";
        if len(account)<6 or len(account)>15:
            result = "合法账户长度6-15位";
        if len(password)<6 or len(password)>15:
            result = "合法密码长度6-15位";
        #检验OK
        return result;

    #用户注册
    @classmethod
    def __userRegister(cls, request=HttpRequest()):
        #输入合法性检验
        account = request.POST.get('account', None);
        password = request.POST.get('password', None);
        print account , password
        checkResult = cls.__inputDataCheck(account, password);
        print account , password, checkResult
        if checkResult == True:
            hash_md5 = hashlib.md5(); #加密
            hash_md5.update(password);
            hashPassword = hash_md5.hexdigest();
            #查询数据库
            result = models.UsersTable.objects.filter(account=account);
            if result:
                return Responses.responseJsonArray("fail", "账号已被注册");
            else:
                #插入数据库
                result = models.UsersTable.objects.create(account=account, password=hashPassword);
                if result:
                    data = [{ 'account' : account}];
                    request.session['account'] = account;  #注册之后直接登录
                    return Responses.responseJsonArray("success", "注册成功", data);
                else:
                    return Responses.responseJsonArray("fail", "注册失败，请重试");
        else:
            return Responses.responseJsonArray("fail", checkResult);

    #用户登录
    @classmethod
    def __userLogin(cls, request=HttpRequest()):
        #输入合法性检验
        account = request.POST.get('account', None);
        password = request.POST.get('password', None);
        checkResult = cls.__inputDataCheck(account, password);
        if checkResult == True:
            #查询数据库
            hash_md5 = hashlib.md5();
            hash_md5.update(password);
            hashPassword = hash_md5.hexdigest();
            try:
                results = models.UsersTable.objects.filter(account=account, password=hashPassword);
                if results[0]:#登录成功
                    data = [{ 'account' : account}];
                    request.session['account'] = account;
                    return Responses.responseJsonArray("success", "登录成功", data);
                else:
                    return Responses.responseJsonArray("fail", "账户或密码错误");
            except Exception, e:
                return Responses.responseJsonArray("fail", "账户或密码错误");
        else:
            return Responses.responseJsonArray("fail", checkResult);

    #注销
    @classmethod
    def __userLogout(cls, request):
        isLogin, account = cls.checkIsLogin(request);
        if isLogin:
            del request.session['account'];
        return Responses.responseJsonArray("success", "已退出");

    #读取用户信息
    @classmethod
    def __getUserInfo(cls, request=HttpRequest()):
        isLogin, account = cls.checkIsLogin(request);
        if isLogin == True:
            #查找用户信息
            data = cls.getUserInfoData(account);
            if data:
                return Responses.responseJsonArray("success", "查找用户信息", data);
            else:
                return Responses.responseJsonArray("fail", "查找失败");
        else:
            return Responses.responseJsonArray("fail", "未登录");

    @classmethod
    def checkIsSuperUser(cls, request=HttpRequest()):
        isLogin, account = cls.checkIsLogin(request);
        if isLogin == True:
            #查找用户信息
            result = models.UsersTable.objects.get(account=account);
            if result:
                return result.superUser;
            else:
                return False;
        else:
            return False;

    @classmethod
    def getUserInfoData(cls, account):
        #查找用户信息
        try:
            result = models.UsersTable.objects.get(account=account);
            data = [model_to_dict(result)];
            return data;
        except Exception, e:
            return None;


    #检测用户是否已经登录
    @classmethod
    def checkIsLogin(cls, request=HttpRequest()):
        account = None;
        try:
            account = request.session.get('account', None);
            if account:
                return True, account;
            else:
                return False, account;
        except:
            return False, account;
    #修改用户信息
    @classmethod
    def __userModify(cls, request=HttpRequest()):
        isLogin, account = cls.checkIsLogin(request);
        if isLogin:
            condition = {};
            if request.POST.get('password', None):
                password = request.POST.get('password', None);
                hash_md5 = hashlib.md5();
                hash_md5.update(password);
                hashPassword = hash_md5.hexdigest();
                condition['password'] = hashPassword;
            if request.POST.get('nickname', None):
                condition['nickname'] = request.POST.get('nickname', None);
            if request.POST.get('email', None):
                condition['email'] = request.POST.get('email', None);

            try:
                result = models.UsersTable.objects.filter(account=account).update(**condition);
                if result:
                    return Responses.responseJsonArray('success', '修改成功');
                else:
                    return Responses.responseJsonArray('fail', '修改失败');
            except Exception, e:
                return Responses.responseJsonArray('fail', '修改失败');
