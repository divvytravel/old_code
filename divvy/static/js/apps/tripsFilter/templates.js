
define(function(require){
    "use strict";

    return {
        tripItem                 : require('tpl!apps/tripsFilter/templates/trip_item.tpl'),
        sidebarTravellersItem    : require('tpl!apps/tripsFilter/templates/sidebar_travellers_item.tpl'),
        tripTravellersItem       : require('tpl!apps/tripsFilter/templates/trip_travellers_item.tpl'),
        travellerDetails         : require('tpl!apps/tripsFilter/templates/traveller_details.tpl'),

        engineFilters            : require('tpl!apps/tripsFilter/templates/engine_filters.tpl'),
        filterPeopleCount        : require('tpl!apps/tripsFilter/templates/engine_filters_people_count.tpl'),
        filterPeopleCountLayout  : require('tpl!apps/tripsFilter/templates/filter_people_count_layout.tpl'),

        engineFiltersTags        : require('tpl!apps/tripsFilter/templates/engine_filters_tags.tpl'),
        engineFiltersTagItem     : require('tpl!apps/tripsFilter/templates/engine_filters_tag_item.tpl'),
        engineFiltersTagWrapper  : require('tpl!apps/tripsFilter/templates/engine_filters_tag_wrapper.tpl'),

        emptyTrips               : require('tpl!apps/tripsFilter/templates/empty_trips.tpl'),
        emptyTravellers          : require('tpl!apps/tripsFilter/templates/empty_travellers.tpl')

    };
});
