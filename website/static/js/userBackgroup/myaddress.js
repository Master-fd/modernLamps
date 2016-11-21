/**
 * Created by Administrator on 2016/11/21.
 */

define(function (require) {

    var $body = $('body');
    var $page = $('#page');
    var $pop = $("#pop");

/****我的地址************************************************************************************************************/
    var url = 'http://127.0.0.1:8000/addressRequest/';
    $page.on('click', '.page-containter .js-addAddr', function(){
        pop.popType('address');   //add 地址
        //清空所有设置
        $pop.find("input[name='addressId']").attr('data-id', '');
        $pop.find("input[name='contact']").val('');
        $pop.find("input[name='phoneNumber']").val('');
        $pop.find("input[name='address']").val('');
    }).on('click', '.page-containter .js-defaults', function(){
        //设置默认
        var $item = $(this);
        var addressId = $(this).parents('tr').data('id');
        var params = {
            operation : 'modify',
            addressId : addressId,
            defaults : 1
        };
        $.post(url, params, function (json_data) {
            //修改
            if (json_data.status == 'success') {
                $page.find('.js-defaults').text('设为默认');
                $item.text('默认地址');
            }
        }, 'json');

    }).on('click', '.page-containter .js-addrmodify', function () {
        //记录修改的是哪个地址
        $page.find('tr').removeClass('record');
        $(this).parents('tr').addClass('record');
        //填充pop
        pop.popType('address');  //modify
        $pop.find("input[name='addressId']").attr('data-id', $(this).parents('tr').data('id'));
        $pop.find("input[name='contact']").val($(this).parents('tr').find('.js-contact').text());
        $pop.find("input[name='phoneNumber']").val($(this).parents('tr').find('.js-phoneNumber').text());
        $pop.find("input[name='address']").val($(this).parents('tr').find('.js-address').text());
    }).on('click', '.page-containter .js-addrdelete', function () {
        //删除
        //记录删除的是哪个地址
        $page.find('tr').removeClass('record');
        $(this).parents('tr').addClass('record');
        var addressId = $(this).parents('tr').data('id');
        var params = {
            operation : 'delete',
            addressId : addressId
        };
        $.post(url, params, function (json_data) {
            if (json_data.status == 'success'){
                $page.find('.record').remove();
            }
        }, 'json')
    });

//填写地址弹窗
    $pop.on('click', '.submit-btn', function(){

        var contact = $pop.find("input[name='contact']").val();
        var phoneNumber = $pop.find("input[name='phoneNumber']").val();
        var address = $pop.find("input[name='address']").val();
        var defaults = $pop.find("input[name='defaults']:checked").val() == 'on' ? 1 : 0;
        var addressId = $pop.find("input[name='addressId']").attr('data-id');

        if (!contact.length){
            pop.popType('error', '联系人不能为空');
            return false;
        }
        if (!phoneNumber.length){
            pop.popType('error', '电话号码不能为空');
            return false;
        }
        if (!address.length){
            pop.popType('error', '地址不能为空');
            return false;
        }
        //关闭弹窗
        pop.popClose();

        var params = {
                contact : contact,
                phoneNumber : phoneNumber,
                address : address,
                defaults : defaults,
                addressId : addressId
            }

        if(addressId){
            // 修改地址
            params['operation'] = 'modify';
            $.post(url, params, function (json_data){
                //修改
                if (json_data.status=='success'){
                    $addrTr = $page.find('.record');
                    if(defaults)
                    {
                        $page.find('.js-defaults').text('设为默认');
                        $addrTr.find('.js-defaults').text('默认地址');
                    }else{
                        $addrTr.find('.js-defaults').text('设为默认');
                    }
                    $addrTr.find('.js-phoneNumber').text(phoneNumber);
                    $addrTr.find('.js-address').text(address);
                    $addrTr.find('.js-contact').text(contact);
                }
            }, 'json');
        }else{
            console.log('add');
            //增加地址
            params['operation'] = 'add';
            $.post(url, params, function (json_data){
                if (json_data.status == 'success'){
                    data = json_data.data[0];
                    if (data.defaults){
                        //清空其他正在显示的default
                        $page.find('.page-containter .content .js-defaults').text('设为默认');
                    }
                    //插入
                    var html = [];
                    html.push('<tr data-id='+data.addressId+'>');
                    html.push('<td><div class="text-center js-contact">'+data.contact+'</div></td>');
                    html.push('<td><div class="js-address">'+data.address+'</div></td>');
                    html.push('<td><div class="text-center js-phoneNumber">'+phoneNumber+'</div></td>');
                    if (data.defaults)
                        html.push('<td><div class="text-center"><a class="js-defaults" href="javascript:void(0);">默认地址</a></div></td>');
                    else
                        html.push('<td><div class="text-center"><a class="js-defaults" href="javascript:void(0);">设为默认</a></div></td>');
                    html.push('<td><div class="text-center">');
                    html.push('<a class="js-addrmodify" href="javascript:void(0);"><i class="icon icon-address icon-edit-address"></i></a>');
                    html.push('<a class="js-addrdelete" href="javascript:void(0);"><i class="icon icon-address icon-del-address"></i></a>');
                    html.push('</div></td></tr>');
                    html.push('<tr class="gap-line"></tr>');

                    $page.find('.content tbody').prepend(html.join(''));
                }
            }, 'json');
        }
    });

});