require.config({
    // baseUrl: '../vendor/',
    urlArgs: "bust=" + (new Date()).getTime(), // For disable cache
    waitSeconds: 0,
    paths: {
        'jquery'               : '../vendor/jquery/dist/jquery',
        'cookie'               : '../vendor/jquery.cookie/jquery.cookie',
        'underscore'           : '../vendor/underscore/underscore',
        'backbone'             : '../vendor/backbone/backbone',
        'tpl'                  : '../vendor/requirejs-tpl/tpl',
        'handlebars'           : '../vendor/require-handlebars-plugin/Handlebars',
        'marionette'           : '../vendor/backbone.marionette/lib/backbone.marionette',
        'bootstrap'            : '../vendor/bootstrap/dist/js/bootstrap.min',
        // 'jquery-ui'            : '../vendor/jquery-ui/ui/minified/jquery-ui.min',
        'jquery-ui'            : '../js/vendor_override/jquery-ui.custom',
        'hb'                   : '../vendor/handlebars/handlebars',
        'bootstrap-datepicker' : '../js/vendor_override/bootstrap-datepicker',
        'typeahead'            : '../vendor/typeahead.js/dist/typeahead.jquery',
        'touch-punch'          : '../vendor/jqueryui-touch-punch/jquery.ui.touch-punch.min',
        'moment'               : '../vendor/moment/min/moment-with-locales.min',
        'fotorama'             : '../vendor/fotorama/fotorama',
        'domReady'             : '../vendor/requirejs-domready/domReady',
        'eventEmitter'         : '../vendor/eventEmitter/EventEmitter',

        'sifter'               : '../vendor/sifter/sifter.min',
        'microplugin'          : '../vendor/microplugin/src/microplugin',
        'selectize'            : '../vendor/selectize/dist/js/selectize',
        'dropzone'             : '../vendor/dropzone/downloads/dropzone-amd-module',
        'rivets'               : '../vendor/rivets/dist/rivets.min',
        'rivets-adapter'       : '../vendor/rivets-backbone-adapter/rivets-backbone',
        'jquery-simulate'      : '../vendor/jquery-simulate/jquery.simulate',
        'native-trigger'       : '../js/vendor_override/native-trigger',
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
        'touch-punch'             : ['jquery', 'jquery-ui'],
        'fotorama'                : ['jquery'],
        'typeahead'               : ['jquery'],
        'selectize'               : ['jquery','microplugin','sifter'],
        'rivets-adapter'          : ['rivets'],
        'jquery-simulate'         : ['jquery'],
        'native-trigger'          : ['jquery'],
    },
    // packages: [
    //     { 
    //         name: 'tripsFilter',
    //         location: 'apps/tripsFilter',
    //     }
    // ]

});
