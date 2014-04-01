
define([
    'backbone'
], function (Backbone) {
    'use strict';

    var FiltersModel = Backbone.Model.extend({

        defaults: {
            "price": {
                "min": 100,
                "max": 2400,
                "alias": "price",
            },
            "age": {
                "min": 20,
                "max": 40,
                "alias": "age",
            },
            "gender": {
                "min": 0,
                "max": 100,
                "alias": "age",
            }
        },

        urlRoot: "/static/json/filters.json",

        initialize: function () {
            //this.trips = new TripsCollection();
            //this.trips.url = this.urlRoot + "/" + this.id + "/info";
        }
    });

    return FiltersModel;
});
