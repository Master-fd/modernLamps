/**
 * Created by Administrator on 2016/11/8.
 */


define(function(require){

    window.$ = window.jQuery = require('jquery');  //加载jq
    window.swal = require('sweetalert');        //加载弹窗对话框
    window.pop = require('pop');    //加载蒙版


    var _page = $('#page').data('id');

    switch (_page){

        case 'home' : seajs.use('static/js/home/home.js'); break;   //加载Home

        default : break;
    }

    seajs.use('static/js/common/base.js');   //加载nav和bottom的js

});