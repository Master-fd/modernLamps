/**
 * Created by Administrator on 2016/11/20.
 */

define(function () {

    var $page = $("#page"),
        $body = $('body'),
        $pop = $('#pop');
        $totalPrice =  $page.find('.js-totalPrice');   //总额


/************数量、金额发生该变，同步到数据库************************************************************/
    function changeShoppingCartToRemote(goodsId, inputNum, $sumPrice) {

        var $totalPrice =  $page.find('.js-totalPrice');
        var url = resourceUrl + 'shoppingCartRequest/';

        var params = {
            operation : 'modify',
            goodsId : goodsId,
            count : inputNum
        };

        $.post(url, params, function(json_data){

            if (json_data.status == 'success'){
                var data = json_data.data[0];
                $sumPrice.text(data.sumPrice);  //修改单行价格数据 //修改订单总价格
                $totalPrice.text(data.totalPrice);   //修改总的
            }
        }, 'json');
    }

/************数量增减*************************************************************/
    $page.on('click', '.js-minus, .js-plus', function(){
        var goodsId = $(this).parents('tr').data('id');
        var inventoryCount = 0;
        var $inputNum = $(this).siblings("input[name='count']");
        var inputNum = parseInt($inputNum.val());
        var $this = $(this);
        var $sumPrice = $this.parents('td').siblings('.js-sumprice').find('span');
        var url = resourceUrl + 'goodsInfoRequest/';
        var params = {};
        //**获取库存等参数
        params = {
            operation : 'get',
            goodsId : goodsId
        };
        $.getJSON(url, params, function (json_data) {

            if (json_data.status == 'success'){
                data = json_data.data[0];
                inventoryCount = data.inventoryCount;  //在线获取

                if ($this.hasClass('js-minus')){//减
                    inputNum -= 1;
                }
                if ($this.hasClass('js-plus')){//加
                    inputNum+= 1;
                }
                if (inputNum<1){
                    inputNum = 1;
                }
                if (inputNum>inventoryCount){
                    inputNum = inventoryCount;
                }
                if (inputNum<=inventoryCount){
                    //删除库存不足提示
                    $this.siblings('.js-stock-tip').addClass('hidden');
                }
                $inputNum.val(inputNum); //更改数量显示
                changeShoppingCartToRemote(goodsId, inputNum, $sumPrice);  //同步到数据库

            }
        });
    });
    //直接输入
    $page.find("input[name='count']").blur(function(){
        var goodsId = $(this).parents('tr').data('id');
        var inventoryCount = 0;
        var $inputNum = $(this).siblings("input[name='count']");
        var inputNum = parseInt($inputNum.val());
        var $this = $(this);
        var $sumPrice = $this.parents('td').siblings('.js-sumprice').find('span');
        var url = resourceUrl + 'goodsInfoRequest/';
        var match = $(this).val().match(/\d+/);
        var params = {};
        //**获取库存等参数
        params = {
            operation : 'get',
            goodsId : goodsId
        };
        if (match != null){
            $.getJSON(url, params, function (json_data) {

                if (json_data.status == 'success'){
                    data = json_data.data[0];
                    inventoryCount = data.inventoryCount;  //在线获取
                    //检测输入合法性
                    inputNum = parseInt(match[0]);
                    if (match != null){
                        if (inputNum<1){
                            inputNum=1;
                        }else if (inputNum>inventoryCount){
                            inputNum=inventoryCount;
                        }
                    }else{
                        if (inventoryCount>0){
                            inputNum=1;
                        }else{
                            inputNum=0;
                        }
                    }
                    if (inputNum<=inventoryCount){
                        //删除库存不足提示
                        $this.siblings('.js-stock-tip').addClass('hidden');
                    }
                    $this.val(inputNum);  //显示数量
                    changeShoppingCartToRemote(goodsId, inputNum, $sumPrice);  //同步到数据库
                }
            });
        }
    });

/************选择框、全选框、删除***************************************************/
    $page.on('click', ".js-checkbox", function(){
        //选择框
        var $this = $(this);
        var $checkAll = $page.find('.js-checkboxall');
        var url = resourceUrl+'shoppingCartRequest/';
        var params = {
            operation : 'checkBox',
            goodsId : $this.parents('tr').data('id')
        };
        $.post(url, params, function (json_data) {
            //检查是否全选
            if (json_data.status == 'success'){
                //将全选框打钩
                $checkAll.prop('checked', 'checked');
            }else{
                $checkAll.removeAttr('checked');
            }
            if (json_data.data){
                var data = json_data.data[0];
                $totalPrice.text(data.totalPrice);   //修改总额
            }
        }, 'json');
    }).on('click', '.js-checkboxall', function(){
        //全选
        var checkAll = $page.find("input[name='checkboxall']:checked").val() == 'on' ? 1 : 0;
        var url = resourceUrl+'shoppingCartRequest/';
        var params = {
            operation : 'checkBoxAll'
        };

        $.post(url, params, function (json_data) {

            if (json_data.status == 'success'){
                //全选所有
                $page.find("input[type='checkbox']").prop('checked', 'checked');
            }else {
                //全不选所有
                $page.find("input[type='checkbox']").removeAttr('checked');
            }
            if (json_data.data){
                var data = json_data.data[0];
                $totalPrice.text(data.totalPrice);   //修改总额
            }
        }, 'json');

    }).on('click', ".js-delete", function () {
        //删除
        var $this = $(this);
        var goodsId = $(this).parents('tr').data('id');
        var url = resourceUrl+'shoppingCartRequest/';
        var params ={
            operation : 'delete',
            goodsId : goodsId
        };

        $.post(url, params, function (json_data) {

            if (json_data.status == 'success'){
                var data = json_data.data[0];
                $this.parents('tr').remove();
                $totalPrice.text(data.totalPrice);   //修改总额
            }
        }, 'json');

    });

/******************结算**********************************************************/
    $page.on('click', '.js-calcuate', function() {
        var url = resourceUrl + 'shoppingCartRequest/';
        var params = {
            operation : 'checkStock'
        };
        //检查是否有库存不足的情况
        $.getJSON(url, params, function (json_data) {

            if (json_data.status == 'success'){
                //没有出现库存不足
                //检查login
                account.isLoginFun(resourceUrl + 'order/checkout');
            }else{//刷新
                location.reload();
            }
        });

    });

});
