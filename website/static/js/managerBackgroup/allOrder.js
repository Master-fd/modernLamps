/**
 * Created by Administrator on 2016/11/21.
 */

define(function (require) {

    var $body = $('body');
    var $page = $('#page');
    var $pop = $("#pop");


/********所有订单*******************************************************************************/
    $page.on('click', '.js-delete-order', function () {
        //删除订单
        var $this = $(this);
        var url = resourceUrl+'orderRequest/';
        var params = {
            operation : 'delete',
            orderId : $this.parents('li').data('id')
        };

        $.post(url, params, function (json_data) {

            if (json_data.status=='success'){

                $this.parents('li').remove();
            }
        }, 'json');

    }).on('click', '.js-modify-status', function () {

        //修改订单状态
        var $this = $(this);
        var url = resourceUrl+'orderRequest/';
        var params = {
            operation : 'get',
            orderId : $this.parents('li').data('id')
        };

        //先获取当前是什么状态，如果是新订单，则弹出填写订单号
        $.getJSON(url, params, function (json_data) {

            if (json_data.status == 'success'){
                var data = json_data.data[0];
                if (data.status == 'new'){
                    pop.popType('orderInput');  //弹窗
                    //记录订单号
                    $pop.find("input[name='orderId']").attr('data-id', $this.parents('li').data('id'));
                }
            }
        });
    });

    //填写订单之后
    $pop.on('click', '.js-submit-btn', function () {

        var company = $pop.find("input[name='company']").val();
        var expressId = $pop.find("input[name='expressId']").val();
        var orderId = $pop.find("input[name='orderId']").attr('data-id');

        if (company && expressId){
            var url = resourceUrl+'orderRequest/';
            var params = {
                operation : 'modify',
                orderId : orderId,
                status : 'process',
                company : company,
                expressId : expressId
            };
            $.post(url, params, function (json_data) {

                if (json_data.status=='success'){
                    var data = json_data.data[0];
                    var str = "li[data-id='"+orderId+"']";
                    $page.find(str).find('.js-modify-status').text(data.status);
                    $page.find(str).find('.js-company').text(data.company);
                    $page.find(str).find('.js-expressId').text(data.expressId);

                }
            }, 'json');
        }

        pop.popClose();
        $pop.find("input[name='orderId']").attr('data-id', '');
    }).on('click', '.js-cancel-btn', function () {
        pop.popClose();
        $pop.find("input[name='orderId']").attr('data-id', '');
    });


});