
define([
    'marionette',
    'vent',
    'templates',
    'custom',
    'jquery',
    'hb',
    'jquery-ui',
    'bootstrap-datepicker',
    'typeahead',
    'touch-punch'
], function (Marionette, Vent, Templates, Cm) {
    'use strict';

    var EngineFilters = {};

    EngineFilters.ItemView = Marionette.ItemView.extend({
        template : Templates.engineFilters,

        ui: {
            fPrice: "#fPrice",
            fPriceMin: "#fPriceMin",
            fPriceMax: "#fPriceMax",

            fAge: "#fAge",
            fGender: "#fGender",
            fDate: "#fDate",
            fPlaceTo: "#fPlaceTo",
            fPlaceFrom: "#fPlaceFrom",
            fUserCount: ".user-count",
        },

        events: {

            "click .efilter": "eFilter",
            // "click .button-toggle": "toggleButton",
            "click .user-count": "userToggle",
            "click .tag-radio": "tagToggle"

        },

        toggleButton: function(e) {
            $(e.currentTarget).toggleClass('active');
        },

        userToggle: function(e) {
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
                Cm.addFilter('user_count',$input.val());
                }
            }

            if (changed) $(e.currentTarget).toggleClass('active')
        },

        tagToggle: function(e) {
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
                }
            }

            if (changed) $(e.currentTarget).toggleClass('active')
        },

        onRender: function() {
            // this.model.set( 'output', this.getLinks(this.model) );

            this.startPrice();
            this.startAge();
            this.startGender();
            this.startDate();
            this.startPlaceTo();
            this.startPlaceFrom();

        },

        initialize: function() {
            this.model.on("sync", this.render, this);
        },

        // render: function() {
        //     console.log(this.model);
        // },

        // onRender: function(){

            // _.each(this.options.filter, function (val, name) {

            //     var self = this;

            //     if ( /-min$/.test(name) || /-max$/.test(name) ) {
            //         this.$("*[data-filter-name='"+name+"']").val(val);
            //     } else if( /^pr-/.test(name) ) {

            //         var vals = val.toString().split('-');
            //         _.each(vals, function(v){
            //             //
            //             self.$("*[data-filter-name='"+name+"'][data-filter-val='"+v+"']").prop("checked",true);
            //         });

            //     } else {
            //         this.$("*[data-filter-name='"+name+"'][data-filter-val='"+val+"']").prop("checked",true);
            //     }

            // }, this);

        // },

        /**
         * Helper for template
         */
        templateHelpers: function() {

            var self = this;

            return {

                showFilter: function(alias, prop) {
                    var output = '';

                    _.each(this, function (val, name) {

                        if (alias == val.alias) {

                            console.log(typeof val.min);
                            // if (typeof val.min !== 'undefined') {
                            //     output = val[prop];
                            // }
                        }

                    }, this);

                    return output;
                },

                showPrice: function() {
                    
                },

                startSlider: function() {

                    console.log( this.price.min );

                    // self.ui.fPrice.text('ter');
                    $( "#fPrice" ).slider({
                        range: true,
                        min: 4,
                        max: 8,
                        values: [4,8],
                        // slide: function( event, ui ) {
                        //     //
                        // }
                    });

                }

            }
        },

        startPrice: function(val) {
            var self = this;

            var alias = 'price';
            this.ui.fPrice.slider({
                range: true,
                min: this.model.get(alias).min,
                max: this.model.get(alias).max,
                values: [ 
                    this.model.get(alias).min, 
                    this.model.get(alias).max
                ],
                stop: function( event, ui ) {
                    Cm.addFilter('price_min',ui.values[0]);
                    Cm.addFilter('price_max',ui.values[1]);
                }
            });

            // this.ui.fPrice.slider({
            //     stop: function( event, ui ) {

            //     }
            // });

            // Vent.on('filter:price:changed',function(response) {
            Vent.on('trips:meta:changed',function(response) {

                self.ui.fPriceMin.text( response.min_price );
                self.ui.fPriceMax.text( response.max_price );
                self.ui.fPrice.slider( "option", "min", response.min_price );
                self.ui.fPrice.slider( "option", "max", response.max_price );
                // self.ui.fPrice.slider( "option", "values", [response.min_price,response.max_price] );

            });

        },

        startAge: function(val) {

            var alias = 'age';
            this.ui.fAge.slider({
                range: true,
                min: this.model.get(alias).min,
                max: this.model.get(alias).max,
                values: [ 
                    this.model.get(alias).min, 
                    this.model.get(alias).max 
                ],
                stop: function( event, ui ) {
                    Cm.addFilter('age_min',ui.values[0]);
                    Cm.addFilter('age_max',ui.values[1]);
                }
            });

        },

        startGender: function(val) {

            var alias = 'gender';
            this.ui.fGender.slider({
                min: this.model.get(alias).min,
                max: this.model.get(alias).max,
                value: 5,
                stop: function( event, ui ) {
                    Cm.addFilter('gender',ui.value.toString());
                }
            });

        },

        startDate: function(val) {

            var current = '';
            this.ui.fDate.datepicker({
                format: "mm-yyyy",
                viewMode: "months", 
                minViewMode: "months",
                language: "ru"
            });

        },

        startPlaceTo: function(val) {
            var places = this.getPlaces();

            this.ui.fPlaceTo.typeahead({
                hint: true,
                highlight: true,
                minLength: 1
            },{
                name: 'places',
                displayKey: 'value',
                source: this.substringMatcher(places),
                templates: {
                  suggestion: Handlebars.compile('<p class="name-part">{{value}}</p> <p class="addition-part">{{country}}</p>')
                }
            });
        },

        startPlaceFrom: function(val) {
            var places = this.getPlaces();

            this.ui.fPlaceFrom.typeahead({
                hint: true,
                highlight: true,
                minLength: 1
            },{
                name: 'places',
                displayKey: 'value',
                source: this.substringMatcher(places),
                templates: {
                  suggestion: Handlebars.compile('<p class="name-part">{{value}}</p> <p class="addition-part">{{country}}</p>')
                }
            });
        },

        substringMatcher: function(strs) {
            return function findMatches(q, cb) {
                var matches, substrRegex;

                // an array that will be populated with substring matches
                matches = [];

                // regex used to determine if a string contains the substring `q`
                substrRegex = new RegExp(q, 'i');

                // iterate through the pool of strings and for any string that
                // contains the substring `q`, add it to the `matches` array
                $.each(strs, function(i, str) {
                    // console.log("op - ",str);
                    if (substrRegex.test(str.value)) {
                        // the typeahead jQuery plugin expects suggestions to a
                        // JavaScript object, refer to typeahead docs for more info
                        matches.push(str);
                    }
                });

                cb(matches);
            };
        },

        getPlaces: function() {
            var states = [
                {'value':'Москва','country':'Россия'},
                {'value':'Паттайя','country':'Тайланд'},
                {'value':'Пицунда','country':'Абхазия'},
                {'value':'Мосул','country':'Ирак'}
            ];
            return states;
        }

    });


    return EngineFilters.ItemView;

});
