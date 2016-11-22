/**
 * Created by Administrator on 2016/11/21.
 */

define(function (require) {
    var $body = $('body');
    var $page = $('#page');
    var $pop = $("#pop");

/***********用户订单管理********************************************************/
    $page.on('click', '.js-delete-order', function () {
        //删除订单
        var $this = $(this);
        var url = resourceUrl+'orderRequest/';
        var params = {
            operation : 'delete',
            orderId : $this.data('id')
        };

        $.post(url, params, function (json_data) {

            if (json_data.status=='success'){

                $this.parents('li').remove();
            }
        }, 'json');
    });

});