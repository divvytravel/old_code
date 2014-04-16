
define([
    'backbone',
    'vent',
    'custom'
], function (Backbone, Vent, Cm) {
    'use strict';

    var CountrieModel = Backbone.Model.extend({

        defaults: {
            "id": 0, 
            "name": "", 
            "resource_uri": ""
        },

    });

    var CountrieCollection = Backbone.Collection.extend({
        model: CountrieModel,

        query: {},

        url: function() {
            var default_params = {
                'format': 'json'
            };

            var query = {};

            var params = _.extend(default_params, query);
            var str = $.param( params );

            return '/api/v1/country/?'+str;
        },

        parse: function(response) {
            if (!response) {
                return [];
            }

            Vent.trigger('countries:meta:changed', response.meta);
            Vent.trigger('countries:obj:changed', response.objects);

            return response.objects;
        }
    });


    return CountrieCollection;
});
