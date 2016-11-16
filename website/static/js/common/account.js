/**
 * Created by Administrator on 2016/11/8.
 */

define(function(require, exports){

    var $page = $('#page');
    var $body = $('body');
    var url = resourceUrl + 'userInfoRequest';

//    判断是否登录, 设置isLogin, 未登录则弹窗
    exports.isLoginFun = function(){
        var params = {operation : 'isLogin'};  //获取用户详细信息
        $.getJSON(url, params, function(json_data){
            if (json_data.status == 'success'){
                //已登录
                isLogin = true;
            }else{
                isLogin = false;
            //    弹窗
                pop.popType('login');
            }
        });
    }
    //登录
    exports.loginOrRegister = function(account, password, operation){
        var params = {operation : operation};
        pop.popClose();
        $.post(url, params, function(json_data){
            if (json_data.status == 'success'){
                isLogin = 1;
                $body.find('.js-logout').css('display' , 'block');
                $body.find('.js-login .js-loginName').text('个人中心');
            }
        });
    }
    //退出
    exports.logout = function(){
        var params = {operation : 'logout'};
        $.post(url, params, function(json_data){
            if (json_data.status == 'success'){
                isLogin = 0;
                $(this).css('display' , 'none');
                $body.find('.js-login .js-loginName').text('登录');
            }
        });
    }
//    获取用户信息,设置导航栏
    exports.getUserInfo = function(){
        var params = {operation : 'getUserInfo'};  //获取用户详细信息
        $.getJSON(url, params, function(json_data){
            if (json_data.status == 'success'){
                //获取成功
                $body.find(".nav .js-login").child('span').text(json_data.data[0].nickName);
            }
        });
    }

});