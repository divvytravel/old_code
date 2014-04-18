
define(function(require){
    "use strict";

    return {
        tripItem                 : require('tpl!templates/trip_item.tpl'),
        sidebarTravellersItem    : require('tpl!templates/sidebar_travellers_item.tpl'),
        tripTravellersItem       : require('tpl!templates/trip_travellers_item.tpl'),
        travellerDetails         : require('tpl!templates/traveller_details.tpl'),

        engineFilters            : require('tpl!templates/engine_filters.tpl'),
        filterPeopleCount        : require('tpl!templates/engine_filters_people_count.tpl'),
        filterPeopleCountLayout  : require('tpl!templates/filter_people_count_layout.tpl'),

        engineFiltersTags        : require('tpl!templates/engine_filters_tags.tpl'),
        engineFiltersTagItem     : require('tpl!templates/engine_filters_tag_item.tpl'),
        engineFiltersTagWrapper  : require('tpl!templates/engine_filters_tag_wrapper.tpl'),

        emptyTrips               : require('tpl!templates/empty_trips.tpl'),
        emptyTravellers          : require('tpl!templates/empty_travellers.tpl')

    };
});
