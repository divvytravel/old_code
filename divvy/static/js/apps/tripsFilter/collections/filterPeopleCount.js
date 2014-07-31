
define([
    'backbone',
    'apps/tripsFilter/vent',
    'custom'
], function (Backbone, Vent, Cm) {
    'use strict';

    var Model = Backbone.Model.extend({

        defaults: { 
            "field_name": "people_count", 
            "name": "", 
            "gt": 0, 
            "lt": 0,
            "active": false
        },

    });

    var Collection = Backbone.Collection.extend({
        
        model: Model,

    });


    return Collection;
});
