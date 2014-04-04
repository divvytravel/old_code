/* JS */

define([
    'jquery',
    'hb',
    'cookie',
    'bootstrap',
    'jquery-ui',
    'bootstrap-datepicker',
    'typeahead',
    'touch-punch'
], function ($) {
    'use strict';

    // $.cookie.defaults = { domain: '.'+art.domain };

    // $( "#fPlaceTo" ).select2({
    //   minimumResultsForSearch: -1
    // });

    // $( "#fPlaceFrom" ).select2({
    //   minimumResultsForSearch: -1
    // });

    // $('.count-people-radio').button('toggle');

    $(document).mouseup(function (e) {
        var elem = $(".details-normal");
        if ( e.target!=elem[0] && elem.has(e.target).length === 0 ){
            elem.remove();
        }
    });

    $('.godown a').click(function(){
        var speed = 500;
        var to = $('.main-page').offset().top;

        $('html, body').animate({scrollTop: to}, speed);

        return false;
    });

});
