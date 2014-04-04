
define([
    'marionette',
    'templates'
], function (Marionette, Templates) {
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
            // var $parent = $(e.currentTarget).closest('');
            var changed = true;

            if ($parent.length) {
              var $input = $(e.currentTarget).find('input');
              if ($input.prop('type') == 'radio') {
                // console.log( $input.prop('checked') );
                if ($input.prop('checked') && $(e.currentTarget).hasClass('active')) changed = false
                else $parent.find('.active').removeClass('active')
              }
              if (changed) {
                $input.prop('checked', !$(e.currentTarget).hasClass('active')).trigger('change')
                // Vent.trigger('filter:meta:changed', response.meta);
                // Cm.addFilter('user_count',$input.val());
                }
            }

            if (changed) $(e.currentTarget).toggleClass('active')

        },

        /**
         * Helper for template
         */
        templateHelpers: {
            //
        }

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
