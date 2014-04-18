
define([
    'backbone',
    'models/trip',
    'vent',
    'custom',
    'moment',
], function (Backbone, TripModel, Vent, Cm, Moment) {
    'use strict';

    var TripsCollection = Backbone.Collection.extend({
        model: TripModel,
        
        query: {
            // 'price__gt':100
        },

        url: function() {
            // var base = _.result(this, 'urlRoot');
            // if (this.isNew()) return base;
            var now = Moment().format('YYYY-MM-DD');

            var default_params = {
                'format': 'json',
                'start_date__gte': now
            };
            var params = _.extend(default_params, this.query);

            var str = $.param( params );
            // console.log(str);

            return '/api/v1/trip/?'+str;
        },

        parse: function(response) {
            if (!response) {
                return [];
            }

            Vent.trigger('trips:meta:changed', response.meta);

            return response.objects;
        }
    });

    return TripsCollection;
});
