/**
 * Created by Administrator on 2016/11/8.
 */


define(function (require, exports) {

    seajs.use('static/js/plugin/sweetalert/sweetalert.min.js');
    $body = $('body');



    exports.popType = function (type, title, confirmText) {

        switch (type){
            case 'login' : $body.find('.login-modal').css('display', 'block'); break;
            case 'address' : $body.find('.address-modal').css('display', 'block'); break;
            case 'error' : swal({
                               title : title,
                               type : 'error',
                               showCancelButton : false,
                               showConfirmButton : false,
                                timer : 1500
                               //closeOnConfirm: false,
                               //confirmButtonText: confirmText,
                               //confirmButtonColor: "rgba(230,69, 102, 1)"
                           }, function(){
                                swal.close();
                            });
                break;
            case 'success' : swal({
                               title : title,
                               type : 'success',
                               showCancelButton : false,
                                showConfirmButton : false,
                                timer : 1500
                               //closeOnConfirm: false,
                               //confirmButtonText: confirmText,
                               //confirmButtonColor: "rgba(230,69, 102, 1)"
                           }, function(){
                                swal.close();
                            });
                break;
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


