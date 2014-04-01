
define([
    'backbone'
], function (Backbone) {
    'use strict';

    var TripModel = Backbone.Model.extend({

        defaults: {
            "age": null,
            "categories": [],
            "city": "London",
            "city_id": 12,
            "consist": null,
            "country": "England",
            "country_id": 11,
            "currency": "euro",
            "descr_additional": "",
            "descr_company": "",
            "descr_main": "Опишите суть поездки.",
            "descr_share": "",
            "end_date": "2014-02-16",
            "end_people_date": "2014-02-07",
            "id": 15,
            "image": "/static/img/promo/trips/1.png",
            "images": [],
            "includes": "Что входит.",
            "people": [{
              "age": 24,
              "avatar_url": "/static/img/promo/users/1.png",
              "birthday": "1989-07-04",
              "career": null,
              "city": null,
              "date_joined": "2014-03-08T09:43:04.623456",
              "first_name": "Виктор",
              "gender": "male",
              "id": 2,
              "last_name": "Клевцов",
              "resource_uri": "/api/v1/user/2/",
              "trips": ["/api/v1/trip/15/", "/api/v1/trip/16/", "/api/v1/trip/17/", "/api/v1/trip/18/"],
              "username": "v-klevzov"
            }, {
              "age": 24,
              "avatar_url": "/static/img/promo/users/2.png",
              "birthday": "1989-07-04",
              "career": null,
              "city": null,
              "date_joined": "2014-03-08T09:43:04.628598",
              "first_name": "Евгения",
              "gender": "female",
              "id": 3,
              "last_name": "Милошевич",
              "resource_uri": "/api/v1/user/3/",
              "trips": ["/api/v1/trip/15/", "/api/v1/trip/16/", "/api/v1/trip/17/", "/api/v1/trip/18/"],
              "username": "miloshevich"
            }, {
              "age": 27,
              "avatar_url": "/static/img/promo/users/3.png",
              "birthday": "1986-07-04",
              "career": null,
              "city": null,
              "date_joined": "2014-03-08T09:43:04.633588",
              "first_name": "Константина",
              "gender": "female",
              "id": 4,
              "last_name": "Константинопольская",
              "resource_uri": "/api/v1/user/4/",
              "trips": ["/api/v1/trip/15/", "/api/v1/trip/16/", "/api/v1/trip/17/", "/api/v1/trip/18/"],
              "username": "const"
            }, {
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
            }, {
              "age": 24,
              "avatar_url": "/static/img/promo/users/5.png",
              "birthday": "1989-07-04",
              "career": null,
              "city": null,
              "date_joined": "2014-03-08T09:43:04.642836",
              "first_name": "Евгения",
              "gender": "female",
              "id": 6,
              "last_name": "Милошевич",
              "resource_uri": "/api/v1/user/6/",
              "trips": ["/api/v1/trip/15/", "/api/v1/trip/16/", "/api/v1/trip/17/", "/api/v1/trip/18/"],
              "username": "mmiloshevich"
            }],
            "people_count": 10,
            "people_max_count": 20,
            "price": 30000,
            "price_type": "noncom",
            "recommended": false,
            "resource_uri": "/api/v1/trip/15/",
            "sex": null,
            "start_date": "2014-02-08",
            "tags": [{
              "id": 13,
              "main_page": true,
              "name": "Экскурсия",
              "resource_uri": "/api/v1/tags/13/",
              "slug": "excursion"
            }, {
              "id": 14,
              "main_page": false,
              "name": "Итальянский язык",
              "resource_uri": "/api/v1/tags/14/",
              "slug": "italian-lang"
            }],
            "title": "Итальянская архитектура",
            "trip_type": "open"
        },

        urlRoot: "/static/json/trips.json",

        initialize: function () {
            //this.trips = new TripsCollection();
            //this.trips.url = this.urlRoot + "/" + this.id + "/info";
        }
    });

    return TripModel;
});
