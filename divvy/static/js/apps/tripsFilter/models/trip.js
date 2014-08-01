
define([
    'backbone'
], function (Backbone) {
    'use strict';

    var TripModel = Backbone.Model.extend({

        defaults: {
            "age": null,
            "categories": [],
            "city": {
              "country": {
                "id": 0,
                "name": "",
                "name_en": "",
                "resource_uri": ""
              },
              "iata": "",
              "id": 0,
              "name": "",
              "name_en": "",
              "resource_uri": ""
            },
            "consist": null,
            "currency": "",
            "descr_additional": "",
            "descr_company": "",
            "descr_main": "",
            "descr_share": "",
            "end_date": "",
            "end_people_date": "",
            "id": 0,
            "image": "",
            "images": [],
            "includes": "",
            "people": [{
              "age": 0,
              "avatar_url": "",
              "birthday": "",
              "career": null,
              "city": null,
              "date_joined": "",
              "first_name": "",
              "gender": "",
              "id": 2,
              "last_name": "",
              "resource_uri": "",
              "trips": [],
              "username": ""
            }],
            "people_count": 0,
            "people_max_count": 0,
            "price": 0,
            "price_type": "",
            "recommended": false,
            "resource_uri": "",
            "sex": null,
            "start_date": "",
            "tags": [{
              "id": 0,
              "main_page": true,
              "name": "Экскурсия",
              "resource_uri": "/api/v1/tags/13/",
              "slug": "excursion"
            }],
            "title": "",
            "trip_type": ""
        },

        urlRoot: "/static/json/trips.json",

        initialize: function () {
            //this.trips = new TripsCollection();
            //this.trips.url = this.urlRoot + "/" + this.id + "/info";
        }
    });

    return TripModel;
});
