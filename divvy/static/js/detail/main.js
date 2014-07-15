
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
        'slider'               : '../../vendor/pgw-slider/pgwslider'

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
        'bootstrap' : ['jquery'],
        'selectize' : ['jquery','microplugin','sifter'],
        'slider'    : ['jquery'],
    }
});


require([
    'jquery',
    'slider'
], function ($) {

    $('.thumb-list > .item').on('click', function(){
        var imgSrc = $(this).data('src');
        $('.main-img > img').attr('src',imgSrc);
    });

});
