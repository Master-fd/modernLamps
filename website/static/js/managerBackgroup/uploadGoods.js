/**
 * Created by Administrator on 2016/11/21.
 */

define(function (require) {

    var $body = $('body');
    var $page = $('#page');
    var $pop = $("#pop");

/***********上传*****************************************************************/


    $page.on('click', '.js-subclass li', function(){
    //    切换选择的分类
        $(this).siblings().removeClass('current');
        $(this).addClass('current');
    });

    //显示图片
    $page.on('change', '.header-image input, .desc-image input, .about-image input', function () {
        var file = null;
        var url = null;

        file = $(this)[0].files[0];
        if (window.createObjectURL != undefined) {
            url = window.createObjectURL(file)
        } else if (window.URL != undefined) {
            url = window.URL.createObjectURL(file)
        } else if (window.webkitURL != undefined) {
            url = window.webkitURL.createObjectURL(file)
        }//获取图片的url
        //显示图片
        $(this).siblings('img').attr("src", url);
    });

    //上传
    $page.on('click', '.upload-info .submit-btn', function () {

        var data = new FormData();

        data.append('operation', 'add');  //上传
        data.append('minImageUrl1', $page.find("input[name='minImageUrl1']")[0].files[0]);
        data.append('minImageUrl2', $page.find("input[name='minImageUrl2']")[0].files[0]);
        data.append('minImageUrl3', $page.find("input[name='minImageUrl3']")[0].files[0]);
        data.append('descImageUrl1', $page.find("input[name='descImageUrl1']")[0].files[0]);
        data.append('descImageUrl2', $page.find("input[name='descImageUrl2']")[0].files[0]);
        data.append('descImageUrl3', $page.find("input[name='descImageUrl3']")[0].files[0]);
        data.append('descImageUrl4', $page.find("input[name='descImageUrl4']")[0].files[0]);
        data.append('descImageUrl5', $page.find("input[name='descImageUrl5']")[0].files[0]);
        data.append('descImageUrl6', $page.find("input[name='descImageUrl6']")[0].files[0]);
        data.append('descImageUrl7', $page.find("input[name='descImageUrl7']")[0].files[0]);
        data.append('descImageUrl8', $page.find("input[name='descImageUrl8']")[0].files[0]);
        data.append('descImageUrl9', $page.find("input[name='descImageUrl9']")[0].files[0]);
        data.append('descImageUrl10', $page.find("input[name='descImageUrl10']")[0].files[0]);
        data.append('aboutImageUrl', $page.find("input[name='aboutImageUrl']")[0].files[0]);
        data.append('remarkImageUrl', $page.find("input[name='aboutImageUrl']")[0].files[0]);

        data.append('goodsName', $page.find("input[name='goodsName']").val());
        data.append('price', $page.find("input[name='price']").val());
        data.append('freightCost', $page.find("input[name='freightCost']").val());
        data.append('inventoryCount', $page.find("input[name='inventoryCount']").val());
        data.append('description', $page.find("textarea[name='description']").val());
        data.append('subClass', $page.find('.js-subclass').children('.current').data('id'));

        //合法性判断
        if (! $page.find("input[name='goodsName']").val())
        {
            pop.popType('error', '名称不能为空');
            return false;
        }
        if (! $page.find("input[name='price']").val())
        {
            pop.popType('error', '价格不能为空');
            return false;
        }
        if (! $page.find("input[name='freightCost']").val())
        {
            pop.popType('error', '运费不能为空');
            return false;
        }
        if (! $page.find("input[name='inventoryCount']").val())
        {
            pop.popType('error', '库存不能为空');
            return false;
        }
        if (! $page.find("textarea[name='description']").val())
        {
            pop.popType('error', '描述不能为空');
            return false;
        }


        //弹窗蒙版
        pop.popType('message', '正在上传 . . . . ');
        $.ajax({
            type : "POST",
            url : resourceUrl+"goodsInfoRequest/",
            data : data,
            cache : false,
            dataType : 'json',
            contentType : false,   //不可缺
            processData : false, //不可缺
            success : function(json_data){
                if (json_data.status == 'success'){

                    pop.popType('success', '上传成功', '', function(){
                        location.reload();
                    });


                }else{
                    pop.popClose();
                }
            },
            error : function(data){
                pop.popClose();
            }
        });
    });

});