/**
 * Created by Administrator on 2016/11/20.
 */

define(function (require) {


    var $page = $("#page"),
        $body = $('body'),
        $pop = $('#pop');


/************添加地址*******************************/
    $page.on('click', '.addressInfo .js-goto-addr', function () {
        account.isLoginFun(resourceUrl+'userBackgroup/address/');
    });

/************地址选择*******************************/
    $page.on('click', '.addressInfo .list .item', function () {
        //移除其他的
        $(this).siblings().removeClass('current');
        $(this).siblings().find("input[type='checkbox']").removeAttr('checked');
        //添加自己
        $(this).addClass('current');
        $(this).find("input[type='checkbox']").prop('checked', 'checked');
    });


/**********结算************************************************/
    //从url中获取参数, 判断是否存在goodsId,用来区分是立即购买还是购物车购买
    function getRequestFromUrl(){
        var url = window.location.search;   //url中?后面的字符串
        var patt = new RegExp('goodsId');
        match = patt.test(url);
        return match;
    }
    $page.on('click', '.goodsInfo .js-calcuate', function () {

        var selectAddressId = $page.find(".addressInfo .list .item.current").data('id'); //获取选中的地址
        var $items = $page.find('.table tbody tr');   //获取行
        var goodsList = [];

        for (var i=0; i<$items.length; i++){  //遍历获取goods
            var $obj = $items.eq(i);

            if ($obj.data('id')) {
                var goods = {
                    goodsId: $obj.data('id'),
                    count: parseInt($obj.find('.js-count').text()),
                    sumPrice: $obj.find('.js-sumPrice').text()
                };
                goodsList.push(goods);
            }
        }

        var url = resourceUrl+'orderRequest/';
        var params = {
            operation : 'add',
            addressId : selectAddressId,
            goodsList : goodsList,
            totalPrice : parseFloat($page.find('.js-totalPrice').text()),
            buyNow : getRequestFromUrl()
        };

        params = JSON.stringify(params);
        $.post(url, params, function (json_data) {

            if (json_data.status == 'success'){
                pop.popType('success', '下单成功', '', function () {
                    window.location.href = resourceUrl+'userBackgroup/order/';
                });

            }else{
                pop.popType('error', json_data.message);
            }
        }, 'json');
    });
});