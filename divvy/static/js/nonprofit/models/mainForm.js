
define([
    'backbone'
], function (Backbone) {
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

        blacklist: ['chipinItems'],

        toJSON: function(options) {
            return _.omit(this.attributes, this.blacklist);
        },

        addChipinItem: function (e,obj) {
            console.log('Add Chip In', e, obj);
            // obj.model.get('chipinItems').add({});
        }

    });

    return Form.mainForm;
});
