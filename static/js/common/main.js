/**
 * Created by Administrator on 2016/11/8.
 */


define(function(require){

    window.$ = window.jQuery = require('jquery');  //加载jq
    window.pop = require('pop'); //加载蒙版弹框

    var _page = $('#page').data('id');

    switch (_page){

        case 'home' : seajs.use('static/js/home/home.js'); break;   //加载Home
        case 'goodsBrowse' : seajs.use('static/js/goods/goodsBrowse.js'); break;
        case 'goodsInfo' : seajs.use('static/js/goods/goodsInfo.js'); break;
        case 'shoppingCart' : seajs.use('static/js/goods/shoppingCart.js');break;
        case 'orderCheckout' : seajs.use('static/js/goods/orderCheckout.js');break;

        //用户后台
        case 'myAddress' : seajs.use('static/js/userBackgroup/userBackgroup.js');
                            seajs.use('static/js/userBackgroup/myAddress.js'); break;
        case 'myCollect' : seajs.use('static/js/userBackgroup/userBackgroup.js');
                            seajs.use('static/js/userBackgroup/myCollect.js'); break;
        case 'myOrder' : seajs.use('static/js/userBackgroup/userBackgroup.js');
                            seajs.use('static/js/userBackgroup/myOrder.js'); break;
        case 'myPersonal' : seajs.use('static/js/userBackgroup/userBackgroup.js');
                            seajs.use('static/js/userBackgroup/myPresonal.js');break;
        //manager后台
        case 'allGoods' : seajs.use('static/js/userBackgroup/userBackgroup.js');
                            seajs.use('static/js/managerBackgroup/allGoods.js'); break;
        case 'allOrder' : seajs.use('static/js/userBackgroup/userBackgroup.js');
                            seajs.use('static/js/managerBackgroup/allOrder.js');break;
        case 'uploadGoods' : seajs.use('static/js/userBackgroup/userBackgroup.js');
                            seajs.use('static/js/managerBackgroup/uploadGoods.js');break;
        default : break;
    }

    seajs.use('static/js/common/base.js');   //加载nav和bottom的js
});