require(['config'], function() {
    require([
        'domReady!',
        'jquery',
    ], function (doc,$) {

        // if ( $("#header_block").length ) {
        //     if ( !Divvy.is_authenticated )
        //         $("#header_block").removeClass("login");
        // }

        /*
            - Главный файл приложения находится по адресу apps/имяприложения/main.js
        */

        $(doc).find('.require-js-app').each(function() {
            var dom = this, params = $(dom).data('params');
            params && params.name && require(['apps/'+params.name+'/main'],function(Model) {
                console.log('App start:',params.name);
            });
        });
    });
});
