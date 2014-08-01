
define([
    'marionette',
    'templates',
    'bootstrap-datepicker',
    'selectize'
], function (Marionette, Templates) {
    'use strict';

    /**
     * Helper model
     */
    var bcItem = Backbone.Model.extend({
        // defaults: {
        //     'value': 1,
        //     'link': 1,
        //     'active': 0,
        //     'disabled': 0
        // }
    });

    /**
     * Helper collection
     */
    var bcItems = Backbone.Collection.extend({
        model: bcItem
    });

    var View = Marionette.ItemView.extend({
        template : Templates.mainForm,

        ui: {
            startDate: "#startDate",
            inputDate: ".input-date",
            selectPriv: "#selectPriv",
            tagsInput: "#tagsInput",
            chipinSelect: ".chipin-select",
        },

        modelEvents: {
            'change': "modelChanged"
        },

        modelChanged: function() {
            this.render();
        },

        onRender: function() {
            // this.model.set( 'output', this.getLinks(this.model) );
            this.startInputDate();
            this.startSelectPriv();
            this.startTagsInput();
            this.startChipinSelect();
        },

//        render: function() {
//            console.log(this.model);
//            this.$el.html( this.template( this.model.toJSON() ) );
//        }

        startInputDate: function() {
            var self = this;

            this.ui.inputDate.datepicker({
                format: "dd-mm-yyyy",
                autoclose: true,
                language: "ru",
                // startDate: start.format('MM-YYYY'),
                // endDate: end.format('MM-YYYY')
            });

        },

        startChipinSelect: function() {
            var self = this;

            // var letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUV';
            // var options = [];
            // for (var i = 0; i < 5000; i++) {
            //     var title = [];
            //     for (var j = 0; j < 8; j++) {
            //         title.push(letters.charAt(Math.round((letters.length - 1) * Math.random())));
            //     }
            //     options.push({
            //         id: i,
            //         text: title.join('')
            //     });
            // }

            this.ui.chipinSelect.selectize({
                create: false,
                // maxItems: null,
                // maxOptions: 30,
                // valueField: 'id',
                // labelField: 'title',
                // searchField: 'title',
                // sortField: 'title',
                // options: options,
                dropdownParent: 'body'
            });

        },

        startSelectPriv: function() {
            var self = this;

            this.ui.selectPriv.selectize({
                create: false,
                // sortField: {
                //     field: 'text',
                //     direction: 'asc'
                // },
                dropdownParent: 'body'
            });

        },

        startTagsInput: function() {
            var self = this;

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

            this.ui.tagsInput.selectize({
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

        },

    });

    return View;

});
