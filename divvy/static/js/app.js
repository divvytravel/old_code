/**
 * Main App
 */

define(function (require) {
    "use strict";

    var Marionette = require('marionette'),
        Vent = require('vent'),
        Router = require('routers/router'),

        /** Collections & Models */
        TripsCollection = require('collections/trips'),
        TravellersCollection = require('collections/travellers'),
        TagsCollection = require('collections/tags'),
        EngineFiltersModel = require('models/engineFilters'),

        /** Views */
        EngineFiltersView = require('views/engineFiltersView'),
        TripsView = require('views/tripsView'),
        TravellersView = require('views/travellersView'),
        BreadcrumbsView = require('views/breadcrumbsView'),

        /** Custom functions & some hooks */
        Cm = require('custom');

    var App = new Marionette.Application(),
        tripsCollection = {},
        travellersCollection = {},
        tagsCollection = {},
        engineFiltersModel = {};

    // var tripsCollection = new TripsCollection();

    /**
     * Get all available regions
     */
    // regionsCollection.fetch({
    //     success: (function (regions) {
    //         var nested_regions = regionsCollection.getNestedRegions(regions.models);
    //     })
    // });

    App.addRegions({
        sidebarTravellers    : '#sidebar_travellers',
        tripsLayout          : '#trips_layout',
        tripsLayoutCount     : '#trips_layout_count',
        tripsLayoutItems     : '#trips_layout_items',
        engineFilters        : '#engine_filters',
        mainPage             : '#main_page',
        mpLoader             : '#main_page_loader',
        tLoader              : '#trips_loader'
    });

    App.addInitializer(function(){

        tripsCollection = new TripsCollection();
        // tripsCollection.query = {'price__gt':100};

        travellersCollection = new TravellersCollection();
        tagsCollection = new TagsCollection();
        engineFiltersModel = new EngineFiltersModel();

        // tripsCollection.fetch({
        //     success: function(data){
        //         console.log('TRIPS FETCH: ', data.models);
        //     }
        // });

        // Start router
        new Router();
        Backbone.history.start();

    });

    App.on("initialize:after", function(options){

        var filterObj = Cm.parseQueryString(Backbone.history.fragment);
        $("#trips_loader").hide();

        // console.log(filterObj);

        /**
         * Remember the view type
         */
        // if(!filterObj.view) {
        //     var f_view = Cm.getCookie('f_view') || 'list';
        //     filterObj.view = f_view;
        //     Cm.addFilter('view', f_view);
        // }
        if(!filterObj.v) {
            var v = '0';
            Cm.addFilter('v', v);
        }

        // App.engineFilters.show(new EngineFiltersView({query_filter: filterObj}));
        App.engineFilters.show( new EngineFiltersView({model: engineFiltersModel, filter: filterObj}) );
        App.tripsLayoutItems.show( new TripsView({collection: tripsCollection}) );
        App.sidebarTravellers.show( new TravellersView({collection: travellersCollection}) );

        engineFiltersModel.fetch({
            success: function() {
                // $("#main_page_loader").hide();
                // App.mpLoader.close();
                // App.mainPage.show();
            }
        }).always(function() { 
            $("#main_page_loader").hide();
            $("#main_page").show();
            Backbone.history.loadUrl();
        });

        tripsCollection.fetch();
        travellersCollection.fetch();

        // Marionette.Controller.extend({
        //   showById: function(id){
        //     var model = new EngineFiltersModel();

        //     var promise = model.fetch();

        //     $.when(promise).then(_.bind(this.showIt, this));
        //   },

        //   showIt: function(model){
        //     var view = new MyView({
        //       model: model
        //     });

        //     MyApp.myRegion.show(view);
        //   }
        // });

        // App.engineFilter.show(new EngineFilterView({filter: filterObj}));

        // App.productsFilterFly.show(new ProductsFilterFlyView({collection: propsCollection,filter: filterObj}));

        $("#engine_filter").show();
        $("#trips_layout").show();

    });

    Vent.on('url:changed',function(filter) {

        var filterObj = Cm.parseQueryString(filter);

        /**
         * Remember the view type
         */

        // if(filterObj.view) {
        //     Cm.setCookie('f_view', filterObj.view);
        // }

        /**
         * Draw all filters
         */
        // App.viewFilter.show(new ViewFilterView({filter: filterObj}));

        // tripsCollection.url = '/api/query?' + Cm.getServerQueryString(filter);

        // var tripsViewOptions = {
        //     collection: productsCollection,
        //     viewtype: filterObj.view || 'list'
        // };

        // App.productsListing.show(new ProductsCollectionView(productsViewOptions));
        // App.breadcrumbs.show(new BreadcrumbsView({model: breadcrumbsModel}))

        travellersCollection.query = filterObj;
        tripsCollection.query = filterObj;

        travellersCollection.fetch();

        $("#trips_loader").show();
        $("#trips_layout").hide();
        tripsCollection.fetch({
            success: function(){
                $("#trips_loader").hide();
                $("#trips_layout").show();
            }
        }).always(function() { 
            //
        });

    });

    Vent.on('trips:meta:changed',function(response) {
        if (response.total_count) {
            $("#trips_layout_count").text('Подходит '+response.total_count+' путешеств' + Cm.getCorrectStr(response.total_count,'ие','ия','ий') ).show();
        } else {
            // $("#trips_layout_count").html('Ничего не найдено <br><br>').show();
            $("#trips_layout_count").hide();
        }
        
    });

    return App;

});
