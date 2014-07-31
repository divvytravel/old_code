
define([
    'marionette',
    'apps/tripsFilter/templates',
    'custom',
    'cookie',
    'apps/tripsFilter/collections/tags'
], function (Marionette, Templates, Cm, Cookie, TagsCollection) {
    'use strict';

    var View = {};


    View.ItemView = Marionette.ItemView.extend({
        template: Templates.engineFiltersTagItem,

        className: "item",

        onRender: function() {
            var hiddenToggleActive = Cm.getCookie('hidden_toggle_active') || 'false';

            if ( this.model.get("active") ) {
                this.$('a').addClass("active");
                this.$('a > input').prop("checked", true);
            }
            
            console.log(hiddenToggleActive);
            if ( hiddenToggleActive === 'false' ) {
                if (!this.model.get("main_page"))
                    this.$('a').hide();
            }

        },

        /**
         * Helper for template
         */
        templateHelpers: function() {

            var self = this;

            return {

                showHiddenClass: function() {
                    var output = '';

                    if (!this.main_page)
                        output = "hidden-tag";2

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

    View.CollectionView = Marionette.CompositeView.extend({
        itemView : View.ItemView,
        template: Templates.engineFiltersTagWrapper,

        className: "clearfix",

        itemViewContainer: ".items",

        // hiddenToggleActive: false,

        buildItemView: function(item, ItemView) {

            var view = new ItemView({
                model: item,
                // viewtype: this.options.viewtype
            });

            return view;
        },

        // itemViewOptions: function() {

        //     return { hiddenToggleActive: this.hiddenToggleActive };

        // },

        initialize : function() {
            // this.render();
            // this.hiddenToggleActive = Cm.getCookie('hidden_toggle_active');
            console.log(Cm.getCookie('hidden_toggle_active'));

            this.collection.on("sync", function () {
                this.render();
            }, this);
        },

        events: {
            "click .tag-radio": "tagToggle",
            "click .all-tags": "hiddenToggle",
        },

        tagToggle: function(e) {
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

                    if ( !$input.prop('checked') ) 
                        Cm.removeFilter('tags',$input.val());
                    else
                        Cm.addFilter('tags',$input.val());
                }
            }

            if (changed) $(e.currentTarget).toggleClass('active')
        },

        hiddenToggle: function(e) {
            var $el = $(e.currentTarget);

            if ($el.hasClass('active')) {
                $el.parent().parent().find('.hidden-tag').hide();
            } else {
                $el.parent().parent().find('.hidden-tag').show();
            }
            
            // this.hiddenToggleActive = (this.hiddenToggleActive) ? true : false;
            // console.log(this.hiddenToggleActive);
            $el.toggleClass('active');
            Cm.setCookie('hidden_toggle_active', $el.hasClass('active') );
        },

        // initialize: function() {

        //     // this.model.on('change', this.render, this);

        // },

        templateHelpers: function() {

            var self = this;

            return {

                showToggleButton: function() {
                    var output = '';
                    // var active = (self.hiddenToggleActive) ? 'active' : '';
                    var active = ( Cm.getCookie('hidden_toggle_active') === 'true' ) ? 'active' : '';
                    
                    if (self.collection.models.length > 5)
                        output = '<a href="javascript:void(0)" class="all-tags ' + active + '"><span>Все категории</span> <span class="arrow-down-red"></span></a>';
                    else
                        output = '';

                    return output;
                },

            }
        },

    });


    return View.CollectionView;
});
