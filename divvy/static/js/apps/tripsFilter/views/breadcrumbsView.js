
define([
    'marionette',
    'apps/tripsFilter/templates',
    'custom'
], function (Marionette, Templates, Cm) {
    'use strict';

    /**
     * Helper model
     */
    var bcItem = Backbone.Model.extend({
        defaults: {
            'value': 1,
            'link': 1,
            'active': 0,
            'disabled': 0
        }
    });

    /**
     * Helper collection
     */
    var bcItems = Backbone.Collection.extend({
        model: bcItem
    });

    var View = Marionette.ItemView.extend({
        template : Templates.breadcrumbsTemplate,

        modelEvents: {
            'change': "modelChanged"
        },

        modelChanged: function() {
            this.render();
        },

        onRender: function() {
            this.model.set( 'output', this.getLinks(this.model) );
        },

        templateHelpers: {

            /**
             * Helper showClass for set classes in template
             */
            showClass: function(item){
                var output = [];

                if( item.active ) output.push('active');
                if( item.disabled ) output.push('disabled');

                return output.join(' ');
            }
        },

        /**
         * Render the Bootstrap pagination contents
         */
        getLinks: function(params) {
            var output = [],
                last_page = this.model.get('last_page'),
                current_page = this.model.get('current_page');

            var out = new bcItems();

            if (last_page < 13){
                output = this.getPageRange(1, last_page);
            } else {
                output = this.getPageSlider();
            }

            out.push( this.getPrevious() );
            out.push( output );
            out.push( this.getNext() );

            return out.toJSON();
        },

        /**
         * Create a range of pagination links
         */
        getPageRange: function (start, end) {
            var output = [],
                item = {},
                current_page = this.model.get('current_page');

            for (var i = start; i <= end; i++) {
                item = {
                    value: i,
                    link: '#'+Cm.setFilter('page', i)
                };

                if(i == current_page){
                    item['active'] = 1;
                }
                output.push(item);
            }

            return output;
        },

        getPageSlider: function () {
            var output = [],
                current_page = this.model.get('current_page'),
                last_page = this.model.get('last_page'),
                window = 6;

            var out = new bcItems();

            if (current_page <= window)
            {
                out.push( this.getPageRange(1, window + 2) );
                out.push( this.getFinish() );

                return out.toJSON();
            }
            else if (current_page >= (last_page - window))
            {
                var start = last_page - 8;

                out.push( this.getStart() );
                out.push( this.getPageRange(start, last_page) );

                return out.toJSON();
            }
            else
            {
                out.push( this.getStart() );
                out.push( this.getAdjacentRange() );
                out.push( this.getFinish() );

                return out.toJSON();
            }

            return output;
        },

        getAdjacentRange: function() {
            var output = [],
                current_page = this.model.get('current_page');

            output = this.getPageRange(current_page - 3, current_page + 3);

            return output;
        },

        getStart: function () {
            var output = [],
                out = new bcItems();

            out.push( this.getPageRange(1, 2) );
            out.push( this.getDots() );

            return out.toJSON();
        },

        getFinish: function () {
            var output = [],
                last_page = this.model.get('last_page'),
                out = new bcItems();

            var output1 = this.getDots();
            var output2 = this.getPageRange(last_page - 1, last_page);
            _.each(output1, function(item){ out.add( item ); });
            _.each(output2, function(item){ out.add( item ); });

            return out.toJSON();
        },

        getDots: function (value) {
            value = value || '...';
            var output = [];

            output.push({
                value: value,
                disabled: 1,
                link: '#'
            });

            return output;
        },

        getPrevious: function ( value ) {
            value = value || '&laquo;';
            var output = [],
                disabled = 0,
                link = '#',
                current_page = this.model.get('current_page');

            if(current_page == 1) {
                disabled = 1;
            } else {
                link = '#'+Cm.setFilter('page', current_page-1);
            }

            output.push({
                value: value,
                link: link,
                disabled: disabled
            });

            return output;
        },

        getNext: function ( value ) {
            value = value || '&raquo;';
            var output = [],
                disabled = 0,
                link = '#',
                last_page = this.model.get('last_page'),
                current_page = this.model.get('current_page');

            if(current_page == last_page) {
                disabled = 1;
            } else {
                link = '#'+Cm.setFilter('page', current_page+1);
            }

            output.push({
                value: value,
                link: link,
                disabled: disabled
            });

            return output;
        }

        /**
         * End of pagination method set
         */

//        render: function() {
//            console.log(this.model);
//            this.$el.html( this.template( this.model.toJSON() ) );
//        }

    });

    return View;

});
