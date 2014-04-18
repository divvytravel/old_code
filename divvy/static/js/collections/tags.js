
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
            "slug": "",
            "active": false
        },

    });

    var TagCollection = Backbone.Collection.extend({
        model: TagModel,

        query: {},

        url: function() {
            var default_params = {
                'format': 'json',
                'distinct': 'True'
            };

            var query = {};

            _.each(this.query, function(value, key) {
                if (key == 'country') {
                    key = 'trip_' + key;
                    query[key] = value;
                } else if (key == 'start_date__gte' || key == 'start_date__lt') {
                    key = 'trips__' + key;
                    query[key] = value;
                }
            });

            var params = _.extend(default_params, query);
            var str = $.param( params );

            return '/api/v1/tags/?'+str;
        },

        comparator: function(tag) {
            return -tag.get("main_page");
        },

        parse: function(response) {
            if (!response) {
                return [];
            }

            Vent.trigger('tags:meta:changed', response.meta);
            Vent.trigger('tags:obj:changed', response.objects);

            return response.objects;
        }
    });


    return TagCollection;
});
