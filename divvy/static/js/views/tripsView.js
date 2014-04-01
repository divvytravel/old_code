
define([
    'marionette',
    'templates',
    'bootstrap'
], function (Marionette, Templates) {
    'use strict';

    var View = {};


    View.ItemView = Marionette.ItemView.extend({
        template: Templates.tripItem,

        events: {
            "click .next": "allTravellers",
            "click .traveller-item": "travellerDetails",
            "click .details-wrap-close": "destroyDetails"
        },

        ui: {
            helpTooltip: ".help-tooltip",
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
            if (index > 3) top = top + step;
            // var top = position.top;
            // var left = position.left;
            var details = Templates.travellerDetails({top: top, left: left, data: $(e.currentTarget).data() });
            $(e.currentTarget).parent().append(details);
        },

        destroyDetails: function(e) {
            $(e.currentTarget).parent().parent().remove();
        },

        onRender: function() {
            // this.model.set( 'output', this.getLinks(this.model) );

            this.ui.helpTooltip.tooltip({
                // position: { my: "center top-10", at: "right center" },
                // tooltipClass: "tooltip-proj",
                // content: "Пример текста для подсказки",
                placement: "bottom",
                html: true,
                title: "Пример текста для подсказки"
            });

        },

        /**
         * Helper for template
         */
        templateHelpers: {
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
        }

    });


    // View.EmptyView = Marionette.CompositeView.extend({
    //     template: Templates.emptyTemplate
    // });


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
