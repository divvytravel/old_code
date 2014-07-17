
define([
    'backbone',
    'moment'
], function (Backbone, Moment) {
    'use strict';

    var Form = {};

    Form.chipinItem = Backbone.Model.extend({
        defaults: {
            'title'       : '',
            'description' : '',
            'price'       : '',
            'currency'    : 'eur',
            'link'        : '',
        },
        initialize : function(){
            // this.valId = this.get('id');
            // this.valName = this.get('name');
        }
    });

    Form.chipinItems = Backbone.Collection.extend({ model : Form.chipinItem });

    Form.mainForm = Backbone.Model.extend({

        urlRoot: '/api/v1/trip/',

        defaults: {
            'includes'     : "test",
            'people_count' : 7,
            'chipinItems'  : [{}]
            // 'city'         : "/api/v1/city/1/",
        },

        initialize : function(){
            // this.chipinItems = new Form.chipinItems(this.get('chipinItems'));
            // this.chipinItems = new Form.chipinItems( [{'title':'title name'}] );
            this.set('chipinItems', new Form.chipinItems( this.get('chipinItems') ));
        },

        // blacklist: ['chipinItems'],

        // toJSON: function(options) {
        //     var attr = this.attributes || {};
        //     if (attr.start_date) {
        //         // console.log('Date', attr.start_date, Moment(attr.start_date, "DD-MM-YYYY"));
        //         // attr.start_date =  Moment(attr.start_date, "DD-MM-YYYY").format('YYYY-MM-DD');
        //     }
        //     return _.omit(attr, this.blacklist);
        // },

        addChipinItem: function (e,obj) {
            console.log('Add Chip In', e, obj);
            // obj.model.get('chipinItems').add({});
        }

    });

    return Form.mainForm;
});
