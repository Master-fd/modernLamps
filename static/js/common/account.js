/**
 * Created by Administrator on 2016/11/8.
 */

define(function(require, exports){

    var $page = $('#page');
    var $body = $('body');
    var url = resourceUrl + 'userInfoRequest/';

//    判断是否登录, 设置isLogin, 未登录则弹窗
    exports.isLoginFun = function(successUrl, func){
        var params = {operation : 'isLogin'};  //获取用户详细信息
        $.getJSON(url, params, function(json_data){
            if (json_data.status == 'success'){
                //已登录
                isLogin = true;
                if (successUrl)
                    window.location.href = successUrl;
                if (func)
                    func();
            }else{
                isLogin = false;
            //    弹窗
                pop.popType('login');
            }
        });
    }
    //登录
    exports.loginOrRegister = function(account, password, operation){
        var params = {
            operation : operation,
            account : account,
            password : password
        };
        pop.popClose();

        $.post(url, params, function(json_data){
            if (json_data.status == 'success'){
                isLogin = true;
                $body.find('.js-logout').css('display' , 'block');
                $body.find('.js-login .js-loginName').text('个人中心');
            }else{
                pop.popType('error', json_data.message);
            }
        }, 'json');
    }
    //退出
    exports.logout = function(){
        var params = {operation : 'logout'};
        $.post(url, params, function(json_data){
            if (json_data.status == 'success'){
                isLogin = false;
                $body.find('.js-logout').css('display' , 'none');
                $body.find('.js-login .js-loginName').text('登录');
                window.location.href = resourceUrl+'home/';
            }
        }, 'json');
    }

//修改用户信息
    exports.modifyUserInfo = function (key, value) {

        var params = {
                operation : 'modify',
            };
        if (key=='nickname')
            params['nickname'] = value;
        if (key=='email')
            params['email'] = value;
        if (key=='password')
            params['password'] = value;

        $.post(url, params, function(json_data){
            if (json_data.status == 'success'){
            }
        }, 'json');
    }
});