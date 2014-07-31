
define([
    'marionette',
    'apps/tripsFilter/templates',
    'custom',
    'apps/tripsFilter/collections/filterPeopleCount'
], function (Marionette, Templates, Cm, FilterPeopleCountCollection) {
    'use strict';

    var View = {};


    View.ItemView = Marionette.ItemView.extend({
        template: Templates.filterPeopleCount,

        className: "item",



        onRender: function() {
            if ( this.model.get("active") ) {
                this.$('a').addClass("active");
                this.$('a > input').prop("checked", true);
            }
        },

        /**
         * Helper for template
         */
        templateHelpers: function() {

            var self = this;

            return {

                showDescription: function(id) {
                    var output = '';
                    return output;
                },

                showRange: function() {
                    var output = '';

                    if (this.gt && this.lt)
                        output = this.gt + "-" + this.lt;
                    else if (this.gt) 
                        output = ">&nbsp;" + this.gt;

                    return output;
                },

                showDataGt: function() {
                    var output = '';

                    if (this.gt)
                        output = 'data-gt="' + this.gt + '"';

                    return output;
                },

                showDataLt: function() {
                    var output = '';

                    if (this.lt)
                        output = 'data-lt="' + this.lt + '"';

                    return output;
                },

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

    View.CollectionView = Marionette.CollectionView.extend({
        itemView : View.ItemView,

        buildItemView: function(item, ItemView) {

            var view = new ItemView({
                model: item,
                // viewtype: this.options.viewtype
            });

            return view;
        },

        initialize : function() {
            // this.render();
            this.collection.on("sync", function () {
                console.log('TEST+++');
                this.render();
            }, this);
        },

        events: {
            "click .user-count": "toggleItem"
        },

        toggleItem: function(e) {
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
                    if ( !$input.prop('checked') ) {
                        // @TODO вынести в custom
                        // Cm.removeFilter('people_count__gt');
                        // Cm.removeFilter('people_count__lt');
                        // Backbone.history.navigate(Cm.unsetFilter('people_count__gt'), {trigger: false});
                        // Backbone.history.navigate(Cm.unsetFilter('people_count__lt'), {trigger: true});
                        Cm.removeFilters({
                            'people_count__gt': 0,
                            'people_count__lt': 0
                        });
                    // people_count
                    } else {
                        if ($input.data('lt')) {
                            // Cm.addFilter('people_count__lt',$input.data('lt'));
                            Backbone.history.navigate(Cm.setFilter('people_count__lt',$input.data('lt')), {trigger: false});
                        } else { 
                            // Cm.removeFilter('people_count__lt');
                            Backbone.history.navigate(Cm.unsetFilter('people_count__lt'), {trigger: false});
                        }
                        // Cm.addFilter('people_count__gt',$input.data('gt'));
                        Backbone.history.navigate(Cm.setFilter('people_count__gt',$input.data('gt')), {trigger: true});
                        
                    }

                }
            }

            if (changed) $(e.currentTarget).toggleClass('active');

        },

        // toggleItem: function(e) {
        //     // $(e.currentTarget).toggleClass('active');
        //     console.log('message');

        //     var $parent = $(e.currentTarget).parent().parent();
        //     var changed = true;

        //     if ($parent.length) {
        //       var $input = $(e.currentTarget).find('input');
        //       if ($input.prop('type') == 'radio') {
        //         if ($input.prop('checked') && $(e.currentTarget).hasClass('active')) changed = true
        //         else $parent.find('.active').removeClass('active')
        //       }
        //       if (changed) {
        //         $input.prop('checked', !$(e.currentTarget).hasClass('active')).trigger('change')
        //         // Vent.trigger('filter:meta:changed', response.meta);
        //         // Cm.addFilter('user_count',$input.val());

        //         if ( !$input.prop('checked') ) 
        //             Cm.removeFilter('people',$input.val());
        //         else
        //             Cm.addFilter('people',$input.val());
        //         }
        //     }

        //     if (changed) $(e.currentTarget).toggleClass('active')

        // },

        // initialize: function() {

        //     // this.model.on('change', this.render, this);

        // },

    });


    return View.CollectionView;
});
