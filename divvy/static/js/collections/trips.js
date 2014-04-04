
define([
    'backbone',
    'models/trip',
    'vent',
    'custom'
], function (Backbone, TripModel, Vent, Cm) {
    'use strict';

    var TripsCollection = Backbone.Collection.extend({
        model: TripModel,
        // url: '/static/json/trips.json',
        // url: '/api/v1/trip/',
        
        query: {
            // 'price__gt':100
        },

        url: function() {
            // var base = _.result(this, 'urlRoot');
            // if (this.isNew()) return base;
            var default_params = {
                'format': 'json',
                'some': 3
            };
            var params = _.extend(default_params, this.query);

            var str = $.param( params );
            console.log(str);

            return '/api/v1/trip/?'+str;
        },

        parse: function(response) {
            if (!response) {
                return [];
            }

            /**
             * Pass trips meta to event handler
             */
            Vent.trigger('trips:meta:changed', response.meta);

            return response.objects;
        }
    });

    return TripsCollection;
});
