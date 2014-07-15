/* JS */

define([
    'jquery',
    'hb',
    'cookie',
    'bootstrap',
    'bootstrap-datepicker',
    'typeahead',
    'selectize'
], function ($) {
    'use strict';

    $('#startDate, #endDate, #endRequestDate').datepicker({
        format: "dd-mm-yyyy",
        // viewMode: "months",
        // minViewMode: "months",
        autoclose: true,
        language: "ru",
        // startDate: start.format('MM-YYYY'),
        // endDate: end.format('MM-YYYY')
    });

    $('#selectPriv').selectize({
        create: false,
        // sortField: {
        //     field: 'text',
        //     direction: 'asc'
        // },
        dropdownParent: 'body'
    });


    // Tags
    var letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUV';
    var options = [];
    for (var i = 0; i < 5000; i++) {
        var title = [];
        for (var j = 0; j < 8; j++) {
            title.push(letters.charAt(Math.round((letters.length - 1) * Math.random())));
        }
        options.push({
            id: i,
            title: title.join('')
        });
    }

    $('#tagsInput').selectize({
        plugins: ['remove_button'],
        persist: false,
        create: true,
        render: {
            item: function(data, escape) {
                return '<div>"' + escape(data.title) + '"</div>';
            },
            option_create: function(data, escape) {
                return '<div class="create">Добавить тег <strong>' + escape(data.input) + '</strong>&hellip;</div>';
            }
        },
        // onDelete: function(values) {
        //     return confirm(values.length > 1 ? 'Are you sure you want to remove these ' + values.length + ' items?' : 'Are you sure you want to remove "' + values[0] + '"?');
        // },
        maxItems: null,
        maxOptions: 50,
        valueField: 'id',
        labelField: 'title',
        searchField: 'title',
        sortField: 'title',
        options: options,
    });

    $(".set-alert").focus(function(e){
        var position = $(e.currentTarget).position();
        var newTop = position.top - 30;
        $('.alert-bal').css('top', newTop+'px').stop(true, true).fadeIn(400);
    });

    $(".set-alert").blur(function(e){
        $('.alert-bal').stop(true, true).fadeOut(100);
    });

    $(".set-alert input").focus(function(e){
        var position = $(e.currentTarget).parent().parent().prev().parent().position();
        var newTop = position.top - 30;
        $('.alert-bal').css('top', newTop+'px').stop(true, true).fadeIn(400);
    });

    $(".set-alert input").blur(function(e){
        $('.alert-bal').stop(true, true).fadeOut(100);
    });

    $("a[href^='#']").click(function(e){
        e.preventDefault();
    });

});
