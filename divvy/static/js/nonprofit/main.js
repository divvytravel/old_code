
require.config({
    // baseUrl: '../',
    urlArgs: "bust=" + (new Date()).getTime(), // For disable cache
    waitSeconds: 0,
    paths: {
        'jquery'               : '../../vendor/jquery/dist/jquery',
        'cookie'               : '../../vendor/jquery.cookie/jquery.cookie',
        'underscore'           : '../../vendor/underscore/underscore',
        'backbone'             : '../../vendor/backbone/backbone',
        'tpl'                  : '../../vendor/requirejs-tpl/tpl',
        'marionette'           : '../../vendor/backbone.marionette/lib/backbone.marionette',
        'bootstrap'            : '../../vendor/bootstrap/dist/js/bootstrap.min',
        'hb'                   : '../../vendor/handlebars/handlebars',
        'bootstrap-datepicker' : '../../js/vendor_override/bootstrap-datepicker',
        'typeahead'            : '../../vendor/typeahead.js/dist/typeahead.jquery',
        'moment'               : '../../vendor/moment/min/moment-with-langs.min',
        'sifter'               : '../../vendor/sifter/sifter.min',
        'microplugin'          : '../../vendor/microplugin/src/microplugin',
        'selectize'            : '../../vendor/selectize/dist/js/selectize',
        'dropzone'             : '../../vendor/dropzone/downloads/dropzone-amd-module',
        'rivets'               : '../../vendor/rivets/dist/rivets.min',
        'rivets-adapter'       : '../../vendor/rivets-backbone-adapter/rivets-backbone',
        'jquery-simulate'      : '../../vendor/jquery-simulate/jquery.simulate',
        'native-trigger'       : '../../js/vendor_override/native-trigger',
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
        'hb'                      : ['jquery'],
        'bootstrap-datepicker'    : ['jquery'],
        'bootstrap-datepicker-ru' : ['jquery'],
        'typeahead'               : ['jquery'],
        'selectize'               : ['jquery','microplugin','sifter'],
        'rivets-adapter'          : ['rivets'],
        'jquery-simulate'         : ['jquery'],
        'native-trigger'          : ['jquery'],
    }
});


require([
    'app',
    // 'todie'
], function (App) {

    App.start();

});
