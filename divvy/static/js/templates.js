
define(function(require){
    "use strict";

    return {
        tripItem               : require('tpl!templates/trip_item.tpl'),
        sidebarTravellersItem  : require('tpl!templates/sidebar_travellers_item.tpl'),
        tripTravellersItem     : require('tpl!templates/trip_travellers_item.tpl'),
        engineFilters          : require('tpl!templates/engine_filters.tpl'),

        travellerDetails       : require('tpl!templates/traveller_details.tpl'),
        engineFiltersTags      : require('tpl!templates/engine_filters_tags.tpl'),
        emptyTrips             : require('tpl!templates/empty_trips.tpl'),
        emptyTravellers        : require('tpl!templates/empty_travellers.tpl')

    };
});
