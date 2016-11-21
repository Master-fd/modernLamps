/**
 * Created by Administrator on 2016/11/17.
 */

define(function (require) {


    var $body = $('body');
    var $page = $('#page');
    var $pop = $("#pop");

/*******左侧导航栏选择*****************************************************************/
    var pageId = $page.data('id');

    switch (pageId){
        case 'uploadGoods' : $body.find('.user-page-left .js-uploader').addClass('current');break;
        case 'allOrder' : $body.find('.user-page-left .js-allOrder').addClass('current');break;
        case 'allGoods' : $body.find('.user-page-left .js-allgoods').addClass('current');break;
    }

    $body.on('click', '.user-page-left a', function () {
        var url = 'http://127.0.0.1:8000/managerBackgroup/'+$(this).data('id')+'/';
        account.isLoginFun(url);
    });




});

