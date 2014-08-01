
define([
    'backbone',
    'apps/tripsFilter/vent'

], function (Backbone, Vent) {
    'use strict';

    var Workspace = Backbone.Router.extend({
        routes: {
            '*filter': 'setFilter'
        },

        setFilter: function (param) {
            if(param){
                Vent.trigger('url:changed', param.trim() || '');
            }
        }

    });

    return Workspace;
});
