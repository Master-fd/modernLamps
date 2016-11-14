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
                $body.find(".login-modal").css('display', 'none');
            }else{
                isLogin = false;
            //    弹窗
                $body.find(".login-modal").css('display' , 'block');
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