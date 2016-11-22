/**
 * Created by fenton-fd.zhu on 2016/11/17.
 */


define(function(require, exports) {

    var $body = $('body');
    var $page = $('#page');
    var $pop = $("#pop");
    var pageId = $page.data('id');

/******左侧选项卡*************************************************/

    switch (pageId) {
        case 'myAddress' :
            $body.find('.user-page-left .js-address').addClass('current');
            break;
        case 'myOrder' :
            $body.find('.user-page-left .js-order').addClass('current');
            break;
        case 'myCollect' :
            $body.find('.user-page-left .js-collect').addClass('current');
            break;
        case 'myPersonal' :
            $body.find('.user-page-left .js-userInfo').addClass('current');
            break;
        //管理员后台
        case 'uploadGoods' :
            $body.find('.user-page-left .js-uploader').addClass('current');
            break;
        case 'allOrder' :
            $body.find('.user-page-left .js-allOrder').addClass('current');
            break;
        case 'allGoods' :
            $body.find('.user-page-left .js-allgoods').addClass('current');
            break;

    }

    $body.on('click', '.user-page-left .js-address, .user-page-left .js-order, .user-page-left .js-collect, .user-page-left .js-userInfo', function () {
        var url = resourceUrl+'userBackgroup/' + $(this).children('a').data('id') + '/';
        console.log('user');
        account.isLoginFun(url);
    }).on('click', '.user-page-left .js-uploader, .user-page-left .js-allOrder, .user-page-left .js-allgoods', function () {
        var url = resourceUrl+'managerBackgroup/'+$(this).children('a').data('id')+'/';
        console.log('manager');
        account.isLoginFun(url);
    });

});







