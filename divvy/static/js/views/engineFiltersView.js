
define([
    'marionette',
    'vent',
    'templates',
    'custom',
    'moment',
    'collections/tags',
    'collections/countries',
    'jquery',
    'hb',
    'jquery-ui',
    'bootstrap-datepicker',
    'typeahead',
    'touch-punch'
], function (Marionette, Vent, Templates, Cm, Moment, TagsCollection, CountriesCollection) {
    'use strict';

    var EngineFilters = {};

    EngineFilters.ItemView = Marionette.ItemView.extend({
        template : Templates.engineFilters,

        ui: {
            fPrice: "#fPrice",
            fPriceMin: "#fPriceMin",
            fPriceMax: "#fPriceMax",
            fPriceMinSlide: "#fPriceMinSlide",
            fPriceMaxSlide: "#fPriceMaxSlide",

            fAge: "#fAge",
            fAgeMin: "#fAgeMin",
            fAgeMax: "#fAgeMax",

            fGender: "#fGender",
            fTags: "#fTags",
            fDate: "#fDate",
            fDateIcon: "#fDateIcon",
            fPlaceTo: "#fPlaceTo",
            fPlaceFrom: "#fPlaceFrom",
            fUserCount: ".user-count",
            dropTripFilters: ".drop-trip-filters",
            dropGroupFilters: ".drop-group-filters"
        },

        events: {

            "click .efilter": "eFilter",
            // "click .button-toggle": "toggleButton",
            "click .user-count": "userToggle",
            "click .tag-radio": "tagToggle",
            "click .drop-trip-filters": "dropTripFilters",
            "click .drop-group-filters": "dropGroupFilters"

        },

        dropTripFilters: function(e) {
            var params = ['price', 'people_count', 'start_date'];
            var filters = this._getFilterParams(params);
            Cm.removeFilters(filters);
        },

        dropGroupFilters: function(e) {
            var params = ['age', 'sex'];
            var filters = this._getFilterParams(params);
            Cm.removeFilters(filters);
        },

        toggleButton: function(e) {
            $(e.currentTarget).toggleClass('active');
        },

        userToggle: function(e) {
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

            if (changed) $(e.currentTarget).toggleClass('active')
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

        onRender: function() {
            // this.model.set( 'output', this.getLinks(this.model) );
            var self = this;

            this.startTags();
            this.startPrice();
            this.startAge();
            this.startGender();
            this.startDate();
            this.startPlaceTo();
            this.startPlaceFrom();

            Vent.on('url:changed',function(filter) {
                var params = ['price', 'people_count', 'start_date'];
                var filters = self._getFilterParams(params);

                if ( !Cm.checkFilters(filters) )
                    self.ui.dropTripFilters.hide();
                else
                    self.ui.dropTripFilters.show();

                var params = ['age', 'sex'];
                var filters = self._getFilterParams(params);

                if ( !Cm.checkFilters(filters) )
                    self.ui.dropGroupFilters.hide();
                else
                    self.ui.dropGroupFilters.show();

            });

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
            var self = this,
                alias = 'price';

            // if (this.filter.price__gt) {
                // var defMinVal = this.options.filter.price__gt || this.model.get(alias).min;
                // var defMaxVal = this.options.filter.price__lt || this.model.get(alias).max;
            // }

            this.ui.fPrice.slider({
                range: true,
                min: this.model.get(alias).min,
                max: this.model.get(alias).max,
                values: [ 
                    this.model.get(alias).min, 
                    this.model.get(alias).max
                ],
                create: function(event, ui) {
                    // self.ui.fPriceMinSlide.appendTo( self.ui.fPrice.find('a').get(0) );
                    // self.ui.fPriceMaxSlide.appendTo( self.ui.fPrice.find('a').get(1) );
                },
                slide: function(event, ui) {
                    self.ui.fPriceMin.html(ui.values[ 0 ] + '&nbsp;&euro;');
                    self.ui.fPriceMax.html(ui.values[ 1 ] + '&nbsp;&euro;');
                    // self.ui.fPrice.find(ui.handle).find('span').html(ui.value + '&nbsp;&euro;');
                },
                stop: function( event, ui ) {
                    Cm.addFilters({
                        'price__gt': ui.values[0],
                        'price__lt': ui.values[1]
                    });
                },
                change: function( event, ui ) {
                    self.ui.fPriceMin.html( self.ui.fPrice.slider( "values", 0 ) + '&nbsp;&euro;');
                    self.ui.fPriceMax.html( self.ui.fPrice.slider( "values", 1 ) + '&nbsp;&euro;');
                }
            });

            self.ui.fPriceMin.html( self.ui.fPrice.slider( "values", 0 ) + '&nbsp;&euro;');
            self.ui.fPriceMax.html( self.ui.fPrice.slider( "values", 1 ) + '&nbsp;&euro;');

            // self.ui.fPriceMinSlide.html( self.ui.fPrice.slider('values', 0) + '&nbsp;&euro;' ).position({
            //     my: 'center top',
            //     at: 'center bottom',
            //     of: self.ui.fPrice.find('a:eq(0)'),
            //     offset: "0, 10"
            // });

            // self.ui.fPriceMaxSlide.html( self.ui.fPrice.slider('values', 1) + '&nbsp;&euro;' ).position({
            //     my: 'center top',
            //     at: 'center bottom',
            //     of: self.ui.fPrice.find('a:eq(1)'),
            //     offset: "0, 10"
            // });

            // Vent.on('filter:price:changed',function(response) {
            Vent.on('trips:meta:changed',function(response) {

                // self.ui.fPriceMin.text( response.min_price );
                // self.ui.fPriceMax.text( response.max_price );
                // self.ui.fPrice.slider( "option", "min", response.min_price );
                // self.ui.fPrice.slider( "option", "max", response.max_price );

                // self.ui.fPrice.slider( "option", "values", [response.min_price,response.max_price] );

            });

            Vent.on('url:changed',function(filter) {
                var filterObj = Cm.parseQueryString(filter);

                var defMinVal = filterObj.price__gt || '';
                var defMaxVal = filterObj.price__lt || '';
                if (defMinVal.length && defMaxVal.length) {
                    self.ui.fPrice.slider( "option", "values", [defMinVal, defMaxVal] );
                } else {
                    self.ui.fPrice.slider( "option", "values", [self.model.get(alias).min, self.model.get(alias).max] );
                }
                
            });

        },

        startTags: function(val) {
            var self = this;

            var tagsCollection = new TagsCollection();

            tagsCollection.fetch({
                success: function(data) {

                    // console.log(data);
                    // var tags = Templates.travellerDetailsTags({tags: data});
                    // self.ui.fTags.append( tags );

                }
            }).always(function() { 
                
            });

            Vent.on('tags:obj:changed',function(obj) {
                
                console.log(obj);
                var tags = Templates.engineFiltersTags({tags: obj});
                self.ui.fTags.html( tags );
                
            });

            Vent.on('url:changed',function(obj) {
                
                // tagsCollection.fetch();
                
            });

        },

        startAge: function(val) {
            var self = this,
                alias = 'age';

            this.ui.fAge.slider({
                range: true,
                min: this.model.get(alias).min,
                max: this.model.get(alias).max,
                values: [ 
                    this.model.get(alias).min, 
                    this.model.get(alias).max 
                ],
                slide: function(event, ui) {
                    self.ui.fAgeMin.html(ui.values[ 0 ] );
                    self.ui.fAgeMax.html(ui.values[ 1 ] );
                },
                stop: function( event, ui ) {
                    Cm.addFilters({
                        'age__gt': ui.values[0],
                        'age__lt': ui.values[1]
                    });
                },
                change: function( event, ui ) {
                    self.ui.fAgeMin.html( self.ui.fAge.slider( "values", 0 ) );
                    self.ui.fAgeMax.html( self.ui.fAge.slider( "values", 1 ) );
                }
            });

            Vent.on('url:changed',function(filter) {
                var filterObj = Cm.parseQueryString(filter);

                var defMinVal = filterObj.age__gt || '';
                var defMaxVal = filterObj.age__lt || '';
                if (defMinVal.length && defMaxVal.length) {
                    self.ui.fAge.slider( "option", "values", [defMinVal, defMaxVal] );
                } else {
                    self.ui.fAge.slider( "option", "values", [self.model.get(alias).min, self.model.get(alias).max] );
                }
                
            });

        },

        startGender: function(val) {
            var self = this,
                offset = 10;

            var alias = 'gender';
            this.ui.fGender.slider({
                min: this.model.get(alias).min,
                max: this.model.get(alias).max,
                value: 50,
                stop: function( event, ui ) {

                    var min = ui.value - ( ui.value * offset / 100 );
                    var max = ui.value + ( ui.value * offset / 100 );
                    min = (min < 0) ? 0 : Math.round(min);
                    max = (max > 100) ? 100 : Math.round(max);

                    // Cm.addFilter('gender', value.toFixed().toString());
                    Cm.addFilters({
                        'sex__gte': min.toString(),
                        'sex__lte': max.toString(),
                    });
                }
            });

            Vent.on('url:changed',function(filter) {
                var filterObj = Cm.parseQueryString(filter);

                var defMinVal = filterObj.sex__gte || '';
                var defMaxVal = filterObj.sex__lte || '';

                if (defMinVal.length && defMaxVal.length) {

                    defMinVal = parseInt( defMinVal );
                    defMaxVal = parseInt( defMaxVal );

                    var defVal = (defMinVal + defMaxVal) / 2;
                    defVal = Math.round(defVal);

                    self.ui.fGender.slider( "option", "value", defVal );
                } else {
                    self.ui.fGender.slider( "option", "value", 50 );
                }
                
            });

        },

        startDate: function(val) {
            var self = this;

            var current = '';
            this.ui.fDate.datepicker({
                format: "mm-yyyy",
                viewMode: "months", 
                minViewMode: "months",
                autoclose: true,
                language: "ru",
                startDate: "04-2014",
                endDate: "07-2014"
            })
            .on("changeDate", function(e){
                var start = Moment( e.date );
                var end = Moment( e.date ).add('M', 1);

                Cm.addFilters({
                    'start_date__gte': start.format('YYYY-MM-DD'),
                    'start_date__lt': end.format('YYYY-MM-DD'),
                });
            });

            this.ui.fDateIcon.on( "click", function() {
                // self.ui.fDate.trigger( "click" );
                self.ui.fDate.datepicker('showTrigger');
            });            

            // start_date

            Vent.on('url:changed',function(filter) {
                var filterObj = Cm.parseQueryString(filter);

                var defVal = filterObj.start_date__gte || '';
                if (defVal.length) {
                    var date = Moment( defVal );
                    console.log(date.format('MM-YYYY'));
                    self.ui.fDate.datepicker('update', date.format('MM-YYYY'));
                } else {
                    self.ui.fDate.datepicker('update', '');
                }
                
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
        },

        _getFilterParams: function(params) {

            var postfix = ['gt', 'gte', 'lt', 'lte'];

            var filterParams = {};
            _.each(params, function(v){
                _.each(postfix, function(vp){
                    filterParams[v + "__" + vp] = 0;
                });
                // filterParams[v] = 0;
            });

            return filterParams;
        }

    });


    return EngineFilters.ItemView;

});
