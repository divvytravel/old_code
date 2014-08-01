require([
    'jquery',
    'rivets',
    'dataProvider',
    'fotorama'
], function ($,Rivets,DataProvider) {

    // Rivets.adapters[':'] = {
    //     subscribe: function(obj, keypath, callback) {
    //         obj.on('change:' + keypath, callback)
    //     },
    //     unsubscribe: function(obj, keypath, callback) {
    //         obj.off('change:' + keypath, callback)
    //     },
    //     read: function(obj, keypath) {
    //         return obj.get(keypath)
    //     },
    //     publish: function(obj, keypath, value) {
    //         obj.set(keypath, value)
    //     }
    // }

    // ///////////   Modify the Soruce Code for Rivets //////////
    // Rivets.config.handler = function (context, ev, binding) {
    //     console.log(binding.model.constructor);
    //     if (binding.model instanceof binding.model.__theSecrectLinkForClass__) {
    //         return this.call(binding.model, ev, context); //Event Target !!
    //     } else {
    //         return this.call(context, ev, binding.view.models);
    //     }
    // };
    ///====== Skip This Part, this is configuration =============
    Rivets.config.handler = function (context, ev, binding) {
        if (binding.model instanceof binding.model.____) {
            return this.call(binding.model, ev, context); // Event Target !!
        } else {
            return this.call(context, ev, binding.view.models);
        }
    };

    var RequestClass = function (data) {
        this.id = data.get('tripId') || 0;
        this.resource_uri = "/api/v1/trip/"+this.id+"/";
        this.requestSend = true;
        this.requestCons = false;
        this.____ = RequestClass;
    };
    RequestClass.prototype = {
        send: function (Event, TargetEle) {
            var self = this;
            console.log(this);
            $.ajax({
                type: "POST",
                url: "/api/v1/triprequest/",
                // data: {trip: self.resource_uri},
                // data: JSON.stringify( {trip: self.resource_uri} ),
                data: JSON.stringify({ "trip": "/api/v1/trip/19/" }),
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    console.log('Success',data);
                    self.requestSend = false;
                    self.requestCons = true;
                },
                error: function(data) {
                    console.log('Error',data);
                }
            }).then(function(data) {
                console.log('Deferred promise',data);
            });
        },
        test: function () {
            console.log('TEST Rivets');
        }
    };

    var dataProvider = new DataProvider( window.DDATA );
    var scope = new RequestClass( dataProvider );

    Rivets.bind($('body'), { scope: scope });

    // Fotorama is not AMD yet
    $('.fotorama').fotorama({
        // width: 700,
        // maxwidth: '100%',
        // ratio: 16/9,
        nav: 'thumbs',
        thumbheight: '60px',
        transition: 'dissolve',
        arrows: true,
        fit: 'cover',
        allowfullscreen: false
    });

});
