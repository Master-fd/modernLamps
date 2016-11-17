/**
 * Created by Administrator on 2016/11/8.
 */


define(function(require){

    window.$ = window.jQuery = require('jquery');  //加载jq
    window.pop = require('pop');    //加载蒙版弹框


    var _page = $('#page').data('id');

    switch (_page){

        case 'home' : seajs.use('static/js/home/home.js'); break;   //加载Home
        case 'myAddress' : seajs.use('static/js/userBackgroup/userBackgroup.js'); break;
        case 'myCollect' : seajs.use('static/js/userBackgroup/userBackgroup.js'); break;
        case 'myOrder' : seajs.use('static/js/userBackgroup/userBackgroup.js'); break;
        case 'myPersonal' : seajs.use('static/js/userBackgroup/userBackgroup.js');break;


        default : break;
    }

    seajs.use('static/js/common/base.js');   //加载nav和bottom的js

});