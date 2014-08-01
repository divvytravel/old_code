require([
    'jquery',
    'rivets',
    'dataProvider',
    'fotorama'
], function ($,Rivets,DataProvider) {

    // Configuration for rivets
    Rivets.config.handler = function (context, ev, binding) {
        if (binding.model instanceof binding.model.____) {
            return this.call(binding.model, ev, context); // Event Target!
        } else {
            return this.call(context, ev, binding.view.models);
        }
    };

    // Rivets.binders.checked = {
    //     publishes: true,
    //     bind: function(el) {
    //       return Rivets.Util.bindEvent(el, 'change', this.publish);
    //     },
    //     unbind: function(el) {
    //       return Rivets.Util.unbindEvent(el, 'change', this.publish);
    //     },
    //     routine: function(el, value) {
    //       var _ref1;
    //       if (el.type === 'radio') {
    //         return el.checked = ((_ref1 = el.value) != null ? _ref1.toString() : void 0) === (value != null ? value.toString() : void 0);
    //       } else {
    //         return el.checked = !!value;
    //       }
    //     }
    //   };

    console.log( Rivets );

    // Rivets.binders.stepshow = {
    //     // publishes: true,
    //     bind: function(el) {
    //       return Rivets._.Util.bindEvent(el, 'change', this.publish);
    //     },
    //     unbind: function(el) {
    //       return Rivets._.Util.unbindEvent(el, 'change', this.publish);
    //     },

    //     routine: function(el, value) {
    //         if ( $(el).data('type') == value )
    //             $(el).show();
    //         else 
    //             $(el).hide();
    //     },
    //     update: function(models) {
    //         console.log( 'Op Op',models );
    //     }
    // };

    // Rivets.binders.stepshow = function(el, value) {
    //     if ( $(el).data('type') == value )
    //         $(el).show(100);
    //     else 
    //         $(el).hide(100);
    // }

    Rivets.binders['stepshow-*'] = function(el, value){
        // el.style.setProperty(this.args[0], value);
        console.log('Op',this.args[0] );
        if ( this.args[0] == value )
            $(el).show();
        else 
            $(el).hide();
    };

    var RequestClass = function (data) {
        this.id = data.get('tripId') || 0;
        this.resource_uri = "/api/v1/trip/"+this.id+"/";
        this.requestSend = true;
        this.requestCons = false;
        this.requestStep = 'send';
        this.____ = RequestClass;
    };
    RequestClass.prototype = {
        send: function (Event, TargetEle) {
            var self = this;
            $.ajax({
                type: "POST",
                url: "/api/v1/triprequest/",
                data: JSON.stringify({ "trip": self.resource_uri }),
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    console.log('Success',data);
                    self.requestStep = 'cons';
                },
                error: function(data) {
                    console.log('Error',data);
                }
            }).then(function(data) {
                console.log('Deferred promise',data);
            });
        },
        goSend: function (Event, TargetEle) {
            var self = this;
            console.log('goSend');
            self.requestStep = 'send-approve';
        },
        currentStep: function (Event, TargetEle) {
            console.log(Event, TargetEle);
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
