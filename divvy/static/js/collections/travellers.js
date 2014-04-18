
define([
    'backbone',
    'vent',
    'moment'
], function (Backbone, Vent, Moment) {
    'use strict';

    var TravellerModel = Backbone.Model.extend({

        defaults: {
            "age": 0,
            "avatar_url": "",
            "birthday": "",
            "career": null,
            "city": null,
            "date_joined": "",
            "first_name": "",
            "gender": "",
            "id": 0,
            "last_name": "",
            "resource_uri": "",
            "trips": [],
            "username": ""
        },

        // urlRoot: "/static/json/users.json"
    });

    var TravellersCollection = Backbone.Collection.extend({
        model: TravellerModel,

        query: {},

        url: function() {
            var now = Moment().format('YYYY-MM-DD');

            var default_params = {
                'format': 'json',
                'trips__start_date__gte': now
            };

            var query = {};

            _.each(this.query, function(value, key) {
                if (key == 'country') {
                    key = 'trip_' + key;
                    query[key] = value;
                } else if (key != 'v') {
                    key = 'trips__' + key;
                    query[key] = value;
                }
            });

            var params = _.extend(default_params, query);
            var str = $.param( params );

            return '/api/v1/user/?'+str;
        },

        parse: function(response) {
            if (!response) {
                return [];
            }

            /**
             * Pass trips meta to event handler
             */
            Vent.trigger('travellers:meta:changed', response.meta);

            return response.objects;
        }
    });

    return TravellersCollection;
});
