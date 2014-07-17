/**
 * Main App
 */

define(function (require) {
    "use strict";

    var Marionette = require('marionette'),
        Vent = require('vent'),
        Rivets = require('rivets'),

        /** Collections & Models */
        MainFormModel = require('models/mainForm'),

        /** Views */
        MainFormView = require('views/mainFormView');

    var App = new Marionette.Application(),
        mainFormModel = {};

    // Для всяких глобальных штук типа тробберов
    var mainModel = new (Backbone.Model.extend());
    mainModel.set('allReady',false);

    var binder = Rivets.bind($('body'), { mainModel: mainModel });

    App.addRegions({
        mainForm    : '#main_form',
    });

    App.addInitializer(function(){
        mainFormModel = new MainFormModel();
    });

    App.on("initialize:after", function(options){
        App.mainForm.show( new MainFormView({model: mainFormModel}) );
        mainModel.set('allReady',true);
    });

    // Ловим глобальные события
    Vent.on('global',function(name,param) {
        mainModel.set(name,param);
    });

    return App;

});
