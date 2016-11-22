/**
 * Created by Administrator on 2016/11/21.
 */

define(function (require) {

    var $body = $('body');
    var $page = $('#page');
    var $pop = $("#pop");


/*********所有商品**********************************************************************/

    $page.on('click', '.orders-info .js-delete', function(){
        //删除
        $item = $(this);
        var params = {
            operation : 'delete',
            goodsId : $item.parents('tr').find('.js-goodsId').text()
        };
        $.post(resourceUrl+"goodsInfoRequest/", params, function(json_data){

            if (json_data.status == 'success'){
                //删除成功
                $item.parents('tr').remove();
            }else{
                pop.popType('error', '删除失败，请检查网络');
            }
        }, 'json');

    });

});

