
define([
    'backbone',
    'vent',
    'custom',
    'moment'
], function (Backbone, Vent, Cm, Moment) {
    'use strict';

    var DateModel = Backbone.Model.extend({

        defaults: {
            "end_date": "", 
            "end_people_date": "", 
            "start_date": ""
        },

    });

    var DateCollection = Backbone.Collection.extend({
        model: DateModel,

        query: {},

        url: function() {
            var now = Moment().format('YYYY-MM-DD');

            var default_params = {
                'format': 'json',
                'limit': 100,
                'end_people_date__gte': now
            };

            var query = {};

            var params = _.extend(default_params, query);
            var str = $.param( params );

            return '/api/v1/date/?'+str;
        },

        parse: function(response) {
            if (!response) {
                return [];
            }

            Vent.trigger('dates:meta:changed', response.meta);
            Vent.trigger('dates:obj:changed', response.objects);

            return response.objects;
        }
    });


    return DateCollection;
});
