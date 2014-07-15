
define([
    'backbone'
], function (Backbone) {
    'use strict';

    var mainForm = Backbone.Model.extend({

        urlRoot: '/api/v1/trip/',
        defaults: {
            'includes'     : "test",
            'people_count' : 7,
            // 'city'         : "/api/v1/city/1/",
        },
        // url: function() {
        //     // var now = Moment().format('YYYY-MM-DD');

        //     var default_params = {
        //         // 'format': 'json',
                
        //     };

        //     var query = {};

        //     var params = _.extend(default_params, query);
        //     var str = $.param( params );

        //     return '/api/v1/date/?'+str;
        // },

    });

    return mainForm;
});
