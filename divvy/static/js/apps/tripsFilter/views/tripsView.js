
define([
    'marionette',
    'apps/tripsFilter/templates',
    'apps/tripsFilter/vent',
    'moment',
    'bootstrap'
], function (Marionette, Templates, Vent, Moment) {
    'use strict';

    var View = {};


    View.ItemView = Marionette.ItemView.extend({
        template: Templates.tripItem,

        events: {
            "click .next": "allTravellers",
            "click .traveller-item": "travellerDetails",
            "click .details-wrap-close": "destroyDetails",
            "click .tag": "activateTag"
        },

        ui: {
            helpTooltip: ".help-tooltip",
            sexSlider: ".sex-slider",
        },

        allTravellers: function(e) {
            $(e.currentTarget).prev().toggleClass('expanded');
            $(e.currentTarget).toggleClass('prev');
            // $(e.currentTarget).find('i').toggleClass('arrow-up');
            var arrow = $(e.currentTarget).find('i');
            if (arrow.hasClass('arrow-down')) {
                arrow.removeClass('arrow-down').addClass('arrow-up');
            } else {
                arrow.removeClass('arrow-up').addClass('arrow-down');
            }
        },

        travellerDetails: function(e) {
            
            var position = $(e.currentTarget).position();

            var index = $(e.currentTarget).index() + 1;
            var step = 61;
            var top = -9;
            var left = -9;
            top = top + position.top;
            left = left + position.left;
            // if (index > 3) top = top + step;
            // if (index % 3 == 0) left = left + step;
            var details = Templates.travellerDetails({top: top, left: left, data: $(e.currentTarget).data() });
            $(e.currentTarget).parent().append(details);
        },

        destroyDetails: function(e) {
            $(e.currentTarget).parent().parent().remove();
        },

        activateTag: function(e) {
            var id = $(e.currentTarget).data("id");
            Vent.trigger('trips:tags:click', id);
        },

        startTooltips: function() {

            this.ui.helpTooltip.tooltip({
                // position: { my: "center top-10", at: "right center" },
                // tooltipClass: "tooltip-proj",
                // content: "Пример текста для подсказки",
                placement: "bottom",
                html: true,
                title: "Пример текста для подсказки"
            });
        },

        onRender: function() {
            // this.model.set( 'output', this.getLinks(this.model) );

            this.startTooltips();
            // console.log(this.model.get('people'));
            this.buildSexSlider();

        },

        buildSexSlider: function() {

            var output = '',
                maleTotal = 0,
                femaleTotal = 0,
                factTotal = 0,
                maleTotalProc = 0,
                femaleTotalProc = 0,
                minTotal = this.model.get('people_count'),
                maxTotal = this.model.get('people_max_count');

            var people = this.model.get('people');
            factTotal = people.length;
            maleTotal = _.where(people, {gender: "male"}).length;
            femaleTotal = _.where(people, {gender: "female"}).length;

            // @TODO
            if (factTotal > minTotal) minTotal = factTotal;

            var sliderWidth = 0,
                leftPercent = 0,
                rightPercent = 0;
            sliderWidth = (100 / minTotal) * factTotal;

            if (factTotal > 1) {
                maleTotalProc = (100 / factTotal) * maleTotal;
                femaleTotalProc = 100 - maleTotalProc;

                var min = Math.min.apply(null, [maleTotalProc, femaleTotalProc]);
                // min = min/2;
                leftPercent = maleTotalProc - min; rightPercent = maleTotalProc + min;

            }

            maleTotalProc = Number( this.model.get('male_ratio') );
            femaleTotalProc = Number( this.model.get('female_ratio') );

            min = Math.min.apply(null, [maleTotalProc, femaleTotalProc]);

            leftPercent = maleTotalProc - min;
            rightPercent = maleTotalProc + min;

            sliderWidth = this.model.get('peoples_ratio');

            this.ui.sexSlider
                .css('background', '-webkit-linear-gradient(left, #24c9f2 '+leftPercent+'%, #f26161 '+rightPercent+'%)')
                .css('background', '-moz-linear-gradient(left, #24c9f2 '+leftPercent+'%, #f26161 '+rightPercent+'%)')
                .css('background', '-o-linear-gradient(left, #24c9f2 '+leftPercent+'%, #f26161 '+rightPercent+'%)')
                .css('background', '-ms-linear-gradient(left, #24c9f2 '+leftPercent+'%, #f26161 '+rightPercent+'%)')
                .css('background', 'linear-gradient(to right, #24c9f2 '+leftPercent+'%, #f26161 '+rightPercent+'%)')
                .css('left', '0%')
                .css('width', sliderWidth+'%');

        },

        /**
         * Helper for template
         */
        templateHelpers: {
            // var self = this;

            // return {
                showNotNull: function(val){
                    var output = '';

                    if (val != null) 
                        output = val;

                    return output;
                },
                showDateRange: function(){
                    var output = '';
                    Moment.lang('ru');
                    var start = Moment( this.start_date );
                    var end = Moment( this.end_date );

                    if ( start.format('M') == end.format('M') ) {
                        if ( start.format('D') == end.format('D') )
                            output = start.format('D MMMM');
                        else
                            output = start.format('D')+" &ndash; "+end.format('D MMMM');
                    } else {
                        output = start.format('D MMMM')+" &ndash; "+end.format('D MMMM');
                    }

                    return output;
                },
                showTripType: function(){
                    var output = '';

                    switch (this.price_type) {
                        case "comm": 
                            output = "Коммерческая поездка";
                            break;
                        case "noncom": 
                            output = "Некоммерческая поездка";
                            break;
                    }

                    return output;
                },
                showSexMajority: function(){
                    var output = '',
                        maleTotal = 0,
                        femaleTotal = 0,
                        maleTotalPercent = 0,
                        femaleTotalPercent = 0,
                        
                        factTotal = 0,
                        minTotal = this.people_count,
                        maxTotal = this.people_max_count;

                    factTotal = this.people.length;
                    maleTotal = _.where(this.people, {gender: "male"}).length;
                    femaleTotal = _.where(this.people, {gender: "female"}).length;

                    // @TODO
                    // if (factTotal > maxTotal) maxTotal = factTotal;

                    // var sliderWidth = 0;
                    // sliderWidth = (100 / maxTotal) * factTotal;

                    // ui.sexSlider
                    // .css('background', '-webkit-linear-gradient(left, #24c9f2 20%, #f26161 90%)')
                    // .css('background', '-moz-linear-gradient(left, #24c9f2 20%, #f26161 90%)')
                    // .css('background', '-o-linear-gradient(left, #24c9f2 20%, #f26161 90%)')
                    // .css('background', '-ms-linear-gradient(left, #24c9f2 20%, #f26161 90%)')
                    // .css('background', 'linear-gradient(to right, #24c9f2 20%, #f26161 90%)')
                    // .css('left', '0%')
                    // .css('width', sliderWidth+'%');
                    // this.buildSexSlider(20,20,34);


                    // console.log(maleTotal, femaleTotal);

                    if (factTotal) {
                        maleTotalPercent = maleTotal * 100 / factTotal;
                        femaleTotalPercent = femaleTotal * 100 / factTotal;
                    }

                    if ( maleTotal === 0 && femaleTotal === 0 ) {
                        output = 'Будь первым!';
                    } else if ( maleTotalPercent >= 40 && maleTotalPercent <= 60 ) {
                        output = "Поровну";
                    } else if ( maleTotal < femaleTotal && femaleTotalPercent > 90 ) {
                        output = "Только девушки";
                    } else if ( maleTotal > femaleTotal && maleTotalPercent > 90 ) {
                        output = "Только мужчины";
                    } else if ( maleTotal < femaleTotal && femaleTotalPercent > 55 ) {
                        output = "Преимущественно девушки";
                    } else if ( maleTotal > femaleTotal && maleTotalPercent > 55 ) {
                        output = "Преимущественно мужчины";
                    } else {
                        output = "Равенство полов";
                    }

                    return output;
                },
                showOccup: function(){
                    var output = '',
                        factTotal = 0,
                        minTotal = this.people_count,
                        maxTotal = this.people_max_count;

                    factTotal = this.people.length;
                    
                    // @TODO
                    if (factTotal > minTotal) minTotal = factTotal;

                    if ( minTotal < factTotal ) {
                        output = "Переполнение!";
                    } else {
                        output = "Набрано "+factTotal+" из "+minTotal+" человек";
                    }

                    return output;
                },
                showPlaceName: function(){
                    var output = '',
                        city = this.city.name || '',
                        country = this.city.country.name || '';

                    if ( city.length > 0 && city.length > 0 ) {
                        // output = "<span>"+city+"</span>"+
                        // "<i> → </i>"+
                        // "<span>"+country+"</span>";
                        output = "<span>"+city+"</span>"+
                        "&nbsp;"+
                        "<span>("+country+")</span>";
                    }

                    return output;
                },
                showButtonText: function(type){
                    var output = '';

                    if(type == 'service') {
                        output = 'отправить сообщение';
                    } else {
                        output = 'сделать заказ';
                    }

                    return output;
                },
                showExist: function(val){
                    var output = '';

                    if(val) {
                        output = '<span class="item-exists">В наличии</span>';
                    }

                    return output;
                },
                showPrice: function(price, discount, light){
                    light = light || false;
                    var output = '';

                    if(discount) {
                        var new_price = price / 100 * (100 - discount);
                        new_price = Number(new_price).toFixed(2);

                        output = (!light) ?
                            '<div class="item-price"><s>' + price + '&nbsp;руб.</s></div>' +
                                '&nbsp;скидка: ' + discount + '% ' + new_price + '&nbsp;руб.' :
                            '<div class="item-price"><s>' + price + '&nbsp;руб.</s></div>' +
                                '&nbsp;' + new_price + '&nbsp;руб.';

                    } else {
                        output = '<div class="item-price">' + price + '&nbsp;руб.</div>';
                    }

                    return output;
                }
            // }
        }

    });


    View.EmptyView = Marionette.CompositeView.extend({
        template: Templates.emptyTrips
    });


    View.CollectionView = Marionette.CollectionView.extend({
        itemView: View.ItemView,

        emptyView: View.EmptyView,

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
