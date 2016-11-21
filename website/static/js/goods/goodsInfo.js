/**
 * Created by Administrator on 2016/11/19.
 */

define(function (require, exports) {


    var $page = $("#page"),
        $body = $('body'),
        $pop = $('#pop'),
        inventoryCount = 0,  //库存
        inputNum = parseInt($page.find("input[name='count']").val()),  //计数
        goodsId = $page.find('.header .js-goodsId').val();


    var url = resourceUrl + 'goodsInfoRequest/',
        params = {};
/************获取库存等参数*************************************************************/
    params = {
        operation : 'get',
        goodsId : goodsId
    };
    $.get(url, params, function (json_data) {

        if (json_data.status == 'success'){
            data = json_data.data[0];
            inventoryCount = data.inventoryCount;  //在线获取
        }else{
            //直接获取
            inventoryCount = parseInt($page.find('.header .js-inventoryCount').text());
        }
    });

/************左边显示框图片选择***************************************************/
    
    $page.find('.header .list .item').hover(function () {
        $(this).siblings().removeClass('current');
        $(this).addClass('current');
        $page.find('.header .js-big-headerImg').attr('src', $(this).children('img').attr('src'));
    });

/***********收藏******************************************************************/
    url = resourceUrl + 'collectRequest/';
    if (isLogin)
    {  //获取用户资料是否已经收藏了,并显示

        params = {
            operation : 'check',
            goodsId : $page.find('.header .js-goodsId').val()
        };

        $.getJSON(url, params, function(json_data){

            if (json_data.status == 'success'){
                //已经收藏了
                $page.find('.header .js-collect').addClass('current');
            }else{
                $page.find('.header .js-collect').removeClass('current');
            }
        });
    }

    $page.on('click', '.header .js-collect', function(){
        //检测是否login
        var $this = $(this);
        account.isLoginFun('', function(){
            //已经login了
            if ($this.hasClass('current')){
                //已经高亮，说明已经收藏了，就要取消
                params = {
                    operation : 'delete',
                    goodsId : goodsId
                };
                $.post(url, params, function(json_data){
                    if (json_data.status == 'success'){
                    //删除成功
                        $page.find('.header .js-collect').removeClass('current');
                    }else{
                        $page.find('.header .js-collect').addClass('current');
                    }
                }, 'json');
            }else{
                //未收藏
                params = {
                    operation : 'add',
                    goodsId : goodsId
                };
                    $.post(url, params, function(json_data){
                    if (json_data.status == 'success'){
                    //收藏成功
                        $page.find('.header .js-collect').addClass('current');
                    }else{
                        $page.find('.header .js-collect').removeClass('current');
                    }
                }, 'json');
            }

        });
    });

/***************数量选择*********************************/
    $page.on('click', '.js-minus, .js-plus', function(){
        $inputNum = $page.find("input[name='count']");
        inputNum = parseInt($inputNum.val());

        if ($(this).hasClass('js-minus')){
            //减
            inputNum -= 1;
        }
        if ($(this).hasClass('js-plus')){
            //加
            inputNum+= 1;
        }
        if (inputNum<1){
            inputNum = 1;
        }
        if (inputNum>inventoryCount){
            inputNum = inventoryCount;
        }
        $inputNum.val(inputNum);
    });
    //直接输入
    $page.find("input[name='count']").blur(function(){
        //检测输入合法性
        var match = $(this).val().match(/\d+/);
        if (match != null){
            inputNum = parseInt(match[0]);
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
        $inputNum.val(inputNum);
    });

/***************加入购物车**  立即购买*****************************************************************************/
    url = resourceUrl + 'shoppingCartRequest/';
    $page.on('click', '.header .js-add-cart', function(){
        //加入购物车
        var sumPrice = inputNum * parseFloat($page.find('.header .js-price').text()) + parseFloat($page.find('.header .js-freightCost').text());
        params = {
            operation : 'add',
            goodsId : goodsId,
            sumPrice : sumPrice,
            count : inputNum
        };
        account.isLoginFun('', function () {
            $.post(url, params, function(json_data){

                if (json_data.status == 'success'){
                    pop.popType('success', '已添加到购物车');
                }else{
                    pop.popType('error', json_data.message);
                }
            }, 'json');
        });

    }).on('click', '.header .js-buy-now', function(){
        //立即购买
        var url = resourceUrl+'order/checkout?goodsId='+goodsId+'&count='+inputNum;
        account.isLoginFun(url);
    });


});