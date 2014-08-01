
define([
    'backbone'
], function (Backbone) {
    'use strict';

    var Props = {};

    Props.PropVal = Backbone.Model.extend({
        defaults: {
            'parent': [{
                'type': 0
            }]
        },
        initialize : function(){
            this.valId = this.get('id');
            this.valName = this.get('name');
        }
    });

    Props.PropVals = Backbone.Collection.extend({ model : Props.PropVal });

    Props.Prop = Backbone.Model.extend({

        initialize : function(){
            this.vals = new Props.PropVals(this.get('vals'));
            this.vals.parent = this;
            this.propId = this.get('id');
            this.propName = this.get('name');
        }
    });

    Props.Props = Backbone.Collection.extend({
        model : Props.Prop,
        url: '/json/props/set.json',
        parse : function(data){
            return data;
        }
    });

    return Props.Props;

});
