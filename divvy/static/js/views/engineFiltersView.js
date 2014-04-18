
define([
    'marionette',
    'vent',
    'templates',
    'custom',
    'moment',
    'collections/tags',
    'collections/countries',
    'collections/dates',
    'collections/filterPeopleCount',
    'views/filterPeopleCountView',
    'views/filterTagsView',
    'jquery',
    'hb',
    'jquery-ui',
    'bootstrap-datepicker',
    'typeahead',
    'touch-punch'
], function (Marionette, Vent, Templates, Cm, Moment, TagsCollection, CountriesCollection, DatesCollection, PeopleCountCollection, PeopleCountView, FilterTagsView) {
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
            fPlaceToIcon: "#fPlaceToIcon",
            fPlaceFrom: "#fPlaceFrom",
            fUserCount: ".user-count",
            dropTripFilters: ".drop-trip-filters",
            dropGroupFilters: ".drop-group-filters",
            fCheckGroup: ".check-group"
        },

        events: {

            "click .efilter": "eFilter",
            "click .drop-trip-filters": "dropTripFilters",
            "click .drop-group-filters": "dropGroupFilters"

        },

        dropTripFilters: function(e) {
            var params = ['price', 'people_count', 'start_date', 'country'];
            var filters = this._getFilterParams(params);
            Cm.removeFilters(filters);
        },

        dropGroupFilters: function(e) {
            var params = ['age', 'sex'];
            var filters = this._getFilterParams(params);
            Cm.removeFilters(filters);
        },

        onRender: function() {
            // this.model.set( 'output', this.getLinks(this.model) );
            var self = this;

            this.countriesCollection = new CountriesCollection();

            this.startTags();
            this.startPrice();
            this.startPeople();
            this.startAge();
            this.startGender();
            this.startDateTrigger();
            this.startPlaceTo();
            this.startPlaceFrom();

            Vent.on('url:changed',function(filter) {

                // self.startPeople();

                var params = ['price', 'people_count', 'start_date', 'country'];
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

            Vent.on('url:changed',function(filter) {

                var filterObj = Cm.parseQueryString(filter);
                // if ( filterObj.people_count__gt == '10' && filterObj.people_count__lt == '30' ) {
                //     self.ui.fUserCount.find("input[data-gt='10']").parent().trigger("click");
                // }

            });

            Vent.on('trips:tags:click',function(id) {
                self.ui.fTags.find('a[data-id="'+id+'"]').trigger('click');

                // @TODO
                var speed = 200;
                var to = $('.main-page').offset().top;
                $('html, body').animate({scrollTop: to}, speed);

            });

        },

        initialize: function() {
            this.model.on("sync", this.render, this);
        },

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

                // if( response.min_price < response.max_price ) {
                //     self.ui.fPrice.slider( "option", "min", response.min_price );
                //     self.ui.fPrice.slider( "option", "max", response.max_price );
                // }

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

        startPeople: function(val) {
            var self = this;

            var peopleCountCollection = new PeopleCountCollection();

            peopleCountCollection.add([
              {
                "field_name": "people_count", 
                "name": "", 
                "gt": 3, 
                "lt": 10,
                "active": false
              },
              {
                "field_name": "people_count", 
                "name": "", 
                "gt": 10, 
                "lt": 30,
                "active": false
              },
              {
                "field_name": "people_count", 
                "name": "", 
                "gt": 30, 
                "lt": 0,
                "active": false
              }
            ]);

            this.ui.fCheckGroup.html( new PeopleCountView({collection: peopleCountCollection}).render().el );

            Vent.on('url:changed',function(filter) {
                
                var filterObj = Cm.parseQueryString(filter);
                var gt = filterObj.people_count__gt || false;
                var lt = filterObj.people_count__lt || false;

                if(gt) {
                    // var model = peopleCountCollection.findWhere({gt: parseInt(gt)});
                    // model.set("active", true);
                    _.each(peopleCountCollection.models, function(model, key){
                        if (model.get("gt") == gt)
                            model.set("active", true);
                        else
                            model.set("active", false); 
                    });
                } else {
                    // var model = peopleCountCollection.findWhere({active: true});
                    _.each(peopleCountCollection.models, function(model, key){ 
                        model.set("active", false); 
                    });
                }

                self.ui.fCheckGroup.html( new PeopleCountView({collection: peopleCountCollection}).render().el );

                // alert(musketeers.length);
                
            });

        },

        startTags: function(val) {
            var self = this;

            // var tagsCollection = new TagsCollection();

            Vent.on('tags:obj:changed',function(obj) {
                
                var tagsCollection = new TagsCollection();
                tagsCollection.add(obj);
                console.log(tagsCollection.models.length);

                var filterObj = Cm.parseQueryString(Backbone.history.fragment);
                var tagId = filterObj.tags || false;

                if(tagId) {
                    var model = tagsCollection.findWhere({id: parseInt(tagId)});
                    if (!model) 
                        Cm.removeFilter('tags', 0);

                    _.each(tagsCollection.models, function(model, key){
                        if (model.get("id") == tagId)
                            model.set("active", true);
                        else
                            model.set("active", false); 
                    });
                } else {
                    _.each(tagsCollection.models, function(model, key){ 
                        model.set("active", false); 
                    });
                }

                // console.log(obj);
                // var tags = Templates.engineFiltersTags({tags: obj});
                self.ui.fTags.html( new FilterTagsView({collection: tagsCollection}).render().el );
                
            });

            Vent.on('url:changed',function(obj) {
                
                // tagsCollection.fetch();
                
            });

        },

        startTags_: function(val) {
            var self = this;

            // var tagsCollection = new TagsCollection();

            // tagsCollection.fetch({
            //     success: function(data) {

            //         // console.log(data);
            //         // var tags = Templates.travellerDetailsTags({tags: data});
            //         // self.ui.fTags.append( tags );

            //     }
            // }).always(function() { 
                
            // });

            Vent.on('tags:obj:changed',function(obj) {
                
                // console.log(obj);
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

        startDateTrigger: function() {
            var self = this;

            var datesCollection = new DatesCollection();

            this.startDate();

            datesCollection.fetch({
                success: function(data) {
                    var startDates, pluckData;
                    pluckData = _.pluck(data.toJSON(), "start_date");

                    var min = _.min( pluckData, function(o){return Moment(o);} );
                    var max = _.max( pluckData, function(o){return Moment(o);} );

                    self.setAvailableDates(min, max);
                }
            });

        },

        startDate: function() {
            var self = this;

            var current = '';
            this.ui.fDate.datepicker({
                format: "mm-yyyy",
                viewMode: "months", 
                minViewMode: "months",
                autoclose: true,
                language: "ru",
                // startDate: start.format('MM-YYYY'),
                // endDate: end.format('MM-YYYY')
            })
            .on("changeDate", function(e){
                var start = Moment( e.date );
                var end = Moment( e.date ).add('M', 1);

                Cm.removeFilters( self._getFilterParams(['country']), false );

                Cm.addFilters({
                    'start_date__gte': start.format('YYYY-MM-DD'),
                    'start_date__lt': end.format('YYYY-MM-DD'),
                });
            });

            this.ui.fDateIcon.on( "click", function() {
                self.ui.fDate.datepicker('showTrigger');
            });

            this.ui.fDateIcon
            .on( 'mouseover', function(e) {
                self.ui.fDate.addClass('hover');
            })
            .on( 'mouseleave', function(e) {
                self.ui.fDate.removeClass('hover');
            });

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

        setAvailableDates: function(start, end) {
            var self = this;
            start = start || "2014-01-01";
            end = end || "2014-10-01";

            start = Moment( start );
            end = Moment( end );

            this.ui.fDate.datepicker('setStartDate', start.format('MM-YYYY'));
            this.ui.fDate.datepicker('setEndDate', end.format('MM-YYYY'));

        },

        startPlaceTo: function(val) {
            var self = this;

            this.countriesCollection.fetch();

            this.ui.fPlaceTo.typeahead({
                hint: false,
                highlight: true,
                autoselect: true,
                minLength: 0
            },{
                name: 'counrty',
                displayKey: 'name',
                source: this.substringMatcher(this.countriesCollection),
                // source: places,
                templates: {
                  // suggestion: Handlebars.compile('<p class="name-part">{{value}}</p> <p class="addition-part">{{country}}</p>')
                  suggestion: Handlebars.compile('<p class="name-part">{{name}}</p>')
                }
            })
            .on('typeahead:selected' , function(e) {
                var params = ['start_date'];
                var filters = self._getFilterParams(params);

                Cm.removeFilters(filters, false);
                Cm.addFilters({
                    'country': $(e.currentTarget).val(),
                });
            });

            this.ui.fPlaceTo.focus(function(e) {
                self.ui.fPlaceTo.typeahead('val', '.').typeahead('val', '');
            });

            this.ui.fPlaceToIcon.on( 'click', function(e) {
                self.ui.fPlaceTo.trigger('focus');
            });

            this.ui.fPlaceToIcon
            .on( 'mouseover', function(e) {
                self.ui.fPlaceTo.addClass('hover');
            })
            .on( 'mouseleave', function(e) {
                self.ui.fPlaceTo.removeClass('hover');
            });

            Vent.on('url:changed',function(filter) {
                var filterObj = Cm.parseQueryString(filter);
                var defVal = filterObj.country || '';

                if (defVal.length) {
                    self.ui.fPlaceTo.val(defVal);
                } else {
                    self.ui.fPlaceTo.val("");
                }
                
            });
        },

        startPlaceFrom: function(val) {
            // var places = this.getPlaces();

            // this.ui.fPlaceFrom.typeahead({
            //     hint: true,
            //     highlight: true,
            //     minLength: 1
            // },{
            //     name: 'places',
            //     displayKey: 'value',
            //     // source: this.substringMatcher(places),
            //     source: places,
            //     templates: {
            //       // suggestion: Handlebars.compile('<p class="name-part">{{value}}</p> <p class="addition-part">{{country}}</p>')
            //       suggestion: Handlebars.compile('<p class="name-part">{{value}}</p>')
            //     }
            // });
        },

        substringMatcher: function(strs) {
            return function findMatches(q, cb) {
                var matches, substrRegex;

                matches = [];
                substrRegex = new RegExp(q, 'i');

                _.each(strs.models, function(val, key){
                    if (substrRegex.test(val.get("name"))) {
                        matches.push( val.toJSON() );
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
                filterParams[v] = 0;
                _.each(postfix, function(vp){
                    filterParams[v + "__" + vp] = 0;
                });
            });

            return filterParams;
        }

    });


    return EngineFilters.ItemView;

});
