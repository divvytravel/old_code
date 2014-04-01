
define([
    'backbone',
    'models/trip',
    'vent'
], function (Backbone, TripModel, Vent) {
    'use strict';

    var TripsCollection = Backbone.Collection.extend({
        model: TripModel,
        url: '/static/json/trips.json',
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
