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
            //跳转到用户后台界面
            window.location.href = resourceUrl+'userBackgroup';
        }

    }).on('click', '.nav .js-logout', function () {
        account.logout();  //退出
    }).on('click', '.login-modal .submit-btn', function(){  //login or register

        userAccount = $(this).siblings("input[name='account']").val();
        password = $(this).siblings("input[name='password']").val();
        operation = $(this).data('id');

        if (userAccount.length>15 || userAccount.length<6){
            pop.popType('error', '账户长度6-15字符', '返回修改');
            return false;
        }
        if (password.length>15 || password.length<6){
            pop.popType('error', '密码长度6-15字符', '返回修改');
            return false
        }

        account.loginOrRegister(userAccount, password, operation);

    })



});