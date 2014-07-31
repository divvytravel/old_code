
require([
    'apps/tripsFilter/app',
    'apps/tripsFilter/todie' // Неразобранный кусок лапши -> @TODO
], function (App) {

    if ( $("#header_block").length ) {
        if ( !Divvy.is_authenticated )
            $("#header_block").removeClass("login");
    }

    App.start();

});
