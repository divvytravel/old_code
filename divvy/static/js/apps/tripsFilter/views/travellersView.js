
define([
    'marionette',
    'apps/tripsFilter/templates',
    'custom'
], function (Marionette, Templates, Cm) {
    'use strict';

    var View = {};


    View.ItemView = Marionette.ItemView.extend({
        template: Templates.sidebarTravellersItem,

        events: {
            "click .item": "toggleItem"
        },

        toggleItem: function(e) {
            // $(e.currentTarget).toggleClass('active');

            var $parent = $(e.currentTarget).parent().parent();
            var changed = true;

            if ($parent.length) {
              var $input = $(e.currentTarget).find('input');
              if ($input.prop('type') == 'radio') {
                if ($input.prop('checked') && $(e.currentTarget).hasClass('active')) changed = true
                else $parent.find('.active').removeClass('active')
              }
              if (changed) {
                $input.prop('checked', !$(e.currentTarget).hasClass('active')).trigger('change')
                // Vent.trigger('filter:meta:changed', response.meta);
                // Cm.addFilter('user_count',$input.val());

                if ( !$input.prop('checked') ) 
                    Cm.removeFilter('people',$input.val());
                else
                    Cm.addFilter('people',$input.val());
                }
            }

            if (changed) $(e.currentTarget).toggleClass('active')

        },

        /**
         * Helper for template
         */
        templateHelpers: function() {

            var self = this;

            return {

                showChecked: function(id) {
                    var output = '';

                    var filterObj = Cm.parseQueryString(Backbone.history.fragment);
                    // console.log(id, filterObj);
                    if(filterObj.people && parseInt( filterObj.people ) == id) {
                        output = "checked";
                    }

                    return output;
                },

                showActive: function(id) {
                    var output = '';

                    var filterObj = Cm.parseQueryString(Backbone.history.fragment);
                    if(filterObj.people && parseInt( filterObj.people ) == id) {
                        output = "active";
                    }

                    return output;
                },

            }
        },

    });


    View.EmptyView = Marionette.CompositeView.extend({
        template: Templates.travellersEmpty
    });


    View.CollectionView = Marionette.CollectionView.extend({
        itemView : View.ItemView,

        /**
         * Custom build for pass viewtype to ItemView
         */
        buildItemView: function(item, ItemView) {

            var view = new ItemView({
                model: item,
                // viewtype: this.options.viewtype
            });

            return view;
        },

        initialize : function() {
            this.collection.on("sync", function () {
                this.render();
            }, this);
        },

        ui: {
            spinner: "#loading_spinner"
        },

        _showSpinner: function() {
            $("#loading_spinner").removeClass("hide");
        },

        _hideSpinner: function() {
            $("#loading_spinner").addClass("hide");
        },

        onRender: function() {
        
        }
    });


    return View.CollectionView;
});
