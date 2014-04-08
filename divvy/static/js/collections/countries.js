
define([
    'backbone',
    'vent',
    'custom'
], function (Backbone, Vent, Cm) {
    'use strict';

    var TagModel = Backbone.Model.extend({

        defaults: {
            "id": 0, 
            "main_page": false, 
            "name": "", 
            "resource_uri": "", 
            "slug": ""
        },

    });

    var TagCollection = Backbone.Collection.extend({
        model: TagModel,

        query: {},

        url: function() {
            var default_params = {
                'format': 'json'
            };
            var params = _.extend(default_params, this.query);
            var str = $.param( params );

            return '/api/v1/country/?'+str;
        },

        parse: function(response) {
            if (!response) {
                return [];
            }

            Vent.trigger('cities:meta:changed', response.meta);

            return response.objects;
        }
    });


    return TagCollection;
});
