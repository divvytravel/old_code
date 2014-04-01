
require.config({
    // baseUrl: '../vendor/',
    urlArgs: "bust=" + (new Date()).getTime(), // For disable cache
    waitSeconds: 0,
    paths: {
        'jquery'                  : '../vendor/jquery/dist/jquery',
        'cookie'                  : '../vendor/jquery.cookie/jquery.cookie',
        'underscore'              : '../vendor/underscore/underscore',
        'backbone'                : '../vendor/backbone/backbone',
        'tpl'                     : '../vendor/requirejs-tpl/tpl',
        'handlebars'              : '../vendor/require-handlebars-plugin/Handlebars',
        'marionette'              : '../vendor/backbone.marionette/lib/backbone.marionette',
        'bootstrap'               : '../vendor/bootstrap/dist/js/bootstrap.min',
        // 'jquery-ui'               : '../vendor/jquery-ui/ui/minified/jquery-ui.min',
        'jquery-ui'               : '../js/vendor_override/jquery-ui.custom',
        'hb'                      : '../vendor/handlebars/handlebars',
        'bootstrap-datepicker'    : '../js/vendor_override/bootstrap-datepicker',
        'typeahead'               : '../vendor/typeahead.js/dist/typeahead.jquery',
        'touch-punch'             : '../vendor/jqueryui-touch-punch/jquery.ui.touch-punch.min'

    },
    shim: {
        'underscore': {
            exports: '_'
        },
        'backbone': {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        },
        'marionette' : {
            deps : ['jquery', 'underscore', 'backbone'],
            exports : 'Marionette'
        },
        'bootstrap'               : ['jquery'],
        'jquery-ui'               : ['jquery'],
        'hb'                      : ['jquery'],
        'bootstrap-datepicker'    : ['jquery'],
        'bootstrap-datepicker-ru' : ['jquery'],
        'typeahead'               : ['jquery'],
        'touch-punch'             : ['jquery']
    }
});


require([
    'app',
    'todie' // Неразобранный кусок лапши -> @TODO
], function (App) {

    App.start();

});
