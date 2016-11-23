/**
 * Created by Administrator on 2016/11/8.
 */
define(function(require, exports){

    account = require('account');

    var $body = $('body'),
        $page = $('#page');

/************导航栏头像login数据*******************/
    //登录头像被点击,
    $body.on('click', '.nav .js-login', function(){
        account.isLoginFun(resourceUrl+'userBackgroup');  //弹出登录
    }).on('click', '.nav .js-logout', function () {
        account.logout();  //退出
    }).on('click', '.login-modal .submit-btn', function(){
        //login or register
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
    });

/*********前往购物车****************************************************************************/
    $body.on('click', '.nav .js-cart', function () {
        var url = resourceUrl+'shoppingCart/';
        account.isLoginFun(url);
    });

/*********商品和首页选择************************************************************************/
    var pageId = $page.data('id');
    switch (pageId){
        case 'home' : $body.find('.js-home').addClass('current');break;
        case 'goodsBrowse' : $body.find('.js-goods').addClass('current');break;
    }



});