
define([
    'backbone'
], function (Backbone) {
    'use strict';

    var Form = {};

    // Form.PropVal = Backbone.Model.extend({
    //     defaults: {
    //         'parent': [{
    //             'type': 0
    //         }]
    //     },
    //     initialize : function(){
    //         this.valId = this.get('id');
    //         this.valName = this.get('name');
    //     }
    // });

    // Form.PropVals = Backbone.Collection.extend({ model : Props.PropVal });

    // Form.Prop = Backbone.Model.extend({

    //     initialize : function(){
    //         this.vals = new Props.PropVals(this.get('vals'));
    //         this.vals.parent = this;
    //         this.propId = this.get('id');
    //         this.propName = this.get('name');
    //     }
    // });

    // Form.Props = Backbone.Collection.extend({
    //     model : Props.Prop,
    //     url: '/json/props/set_'+Emart.current_category+'.json',
    //     parse : function(data){
    //         return data;
    //     }
    // });





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
