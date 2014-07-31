
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
        'fotorama'             : '../../vendor/fotorama/fotorama'

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
        'fotorama'    : ['jquery'],
    }
});


require([
    'jquery',
    'fotorama'
], function ($) {

    $(function () {
        $('.fotorama').fotorama({
            // width: 700,
            // maxwidth: '100%',
            // ratio: 16/9,
            nav: 'thumbs',
            thumbheight: '60px',
            transition: 'dissolve',
            arrows: true,
            fit: 'cover',
            allowfullscreen: false
        });
    });
});
