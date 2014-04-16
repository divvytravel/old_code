
define([
    'backbone',
    'vent'
], function (Backbone, Vent) {
    'use strict';

    var TravellerModel = Backbone.Model.extend({

        defaults: {
            "age": 23,
            "avatar_url": "/static/img/promo/users/4.png",
            "birthday": "1990-07-04",
            "career": null,
            "city": null,
            "date_joined": "2014-03-08T09:43:04.638218",
            "first_name": "Жан",
            "gender": "male",
            "id": 5,
            "last_name": "Петров",
            "resource_uri": "/api/v1/user/5/",
            "trips": ["/api/v1/trip/15/", "/api/v1/trip/16/", "/api/v1/trip/17/", "/api/v1/trip/18/"],
            "username": "petrov"
        },

        // urlRoot: "/static/json/users.json"
    });

    var TravellersCollection = Backbone.Collection.extend({
        model: TravellerModel,
        // url: '/static/json/users2.json',

        query: {},

        url: function() {
            var default_params = {
                'format': 'json'
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
