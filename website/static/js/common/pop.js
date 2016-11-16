/**
 * Created by Administrator on 2016/11/8.
 */


define(function (require, exports) {

    seajs.use('static/js/plugin/sweetalert/sweetalert.min.js');
    $body = $('body');



    exports.popType = function (type, title, confirmText) {

        switch (type){
            case 'login' : $body.find('.login-modal').css('display', 'block');
            case 'error' : swal({
                               title : title,
                               type : 'error',
                               showCancelButton : false,
                               closeOnConfirm: false,
                               confirmButtonText: confirmText,
                               confirmButtonColor: "rgba(230,69, 102, 1)"
                           }, function(){
                                swal.close();
                            });
            case 'success' : swal({
                               title : title,
                               type : 'success',
                               showCancelButton : false,
                               closeOnConfirm: false,
                               confirmButtonText: confirmText,
                               confirmButtonColor: "rgba(230,69, 102, 1)"
                           }, function(){
                                swal.close();
                            });
        }
    }

    //代码主动关闭弹窗
    exports.popClose = function(){
        $body.find('#pop').css('display', 'none');
    }

    //单击‘x’，或者外面阴影部分，关闭弹窗
    $body.on('click', '.js-modal-close', function(){
        $body.find('#pop').css('display', 'none');
    })



});


