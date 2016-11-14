/**
 * Created by Administrator on 2016/11/8.
 */
define(function(require, exports){

    account = require('account');
    $body = $('body');

    //获取用户信息，设置导航栏
    account.getUserInfo();


    //登录头像被点击,
    $body.on('click', '.nav .js-login', function(){
        if (isLogin == false){
            account.isLoginFun();  //弹出登录
        }else{
            //跳转到用户界面
            window.location.href = resourceUrl+'userBackgroup';
        }
    });

});