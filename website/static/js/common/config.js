/**
 * Created by Administrator on 2016/11/8.
 */
(function(resourceUrl){

    seajs.config({

        base : resourceUrl,
        alias : {   //配置模块
            'jquery' : 'js/plugin/jquery-2.1.4/jquery.js',
            'sweetalert' : 'js/plugin/sweetalert/sweetalert.min.js',
            'account' : 'js/common/account.js',
            'pop' : 'js/common/pop.js'
        }
    });

    seajs.use('js/common/main.js');  //加载不同的模块

})(resourceUrl);