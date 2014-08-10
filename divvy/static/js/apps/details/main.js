require([
    'jquery',
    'rivets',
    'dataProvider',
    'fotorama'
], function ($,Rivets,DataProvider) {

    // Configuration for rivets
    Rivets.config.handler = function (context, ev, binding) {
        console.log(binding);
        if (binding.model instanceof binding.model.____) {
            return this.call(binding.model, ev, context); // Event Target!
        } else {
            return this.call(context, ev, binding.view.models);
        }
    };

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

    Rivets.binders.showalert = function(el, value) {
        if ( $(el).data('type') == value )
            $(el).show(100);
        else 
            $(el).hide(100);
    }

    Rivets.binders['stepshow-*'] = function(el, value){
        // el.style.setProperty(this.args[0], value);
        console.log('Op',this.args[0] );
        if ( this.args[0] == value )
            $(el).show();
        else 
            $(el).hide();
    };

    Rivets.binders['status-*'] = function(el, value){
        // el.style.setProperty(this.args[0], value);
        if ( this.args[0] == value )
            $(el).show();
        else 
            $(el).hide();
    };

    var RequestClass = function (data) {
        this.id = data.get('tripId') || 0;
        this.triprequestStatus = data.get('triprequestStatus') || '';
        this.triprequestId = data.get('triprequestId') || null;
        this.userId = data.get('userId') || null;
        this.resourceUri = "/api/v1/trip/"+this.id+"/";
        this.allowPost = true;
        this.requestSend = true;
        this.requestCons = false;
        this.requestStep = '';
        if (this.triprequestStatus == '') {
            this.requestStep = 'send';
        } else if (this.triprequestStatus == 'cancelled') { 
            this.requestStep = 'send';
        } else if (this.triprequestStatus == 'pending') { 
            this.requestStep = 'cons';
        }
        this.____ = RequestClass;
    };
    RequestClass.prototype = {
        send: function (e, el) {
            var self = this;
            $.ajax({
                type: "POST",
                url: "/api/v1/triprequest/",
                data: JSON.stringify({ "trip": self.resourceUri,"allow_post_fb": self.allowPost }),
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
        cancel: function (e, el) {
            var self = this;
            var url = '/api/v1/triprequest/'+self.triprequestId+'/cancel/';
            $.ajax({
                type: "POST",
                url: url,
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    console.log('Success',data);
                    self.requestStep = 'send';
                },
                error: function(data) {
                    console.log('Error',data);
                    alert('Произошла ошибка!');
                }
            }).then(function(data) {
                console.log('Deferred promise',data);
            });
        },
        goSend: function (e, el) {
            var self = this;
            if (this.userId == null) {
                // alert('Анука авторизуйся немедленно!');
                self.authPopup();
            } else {
                self.requestStep = 'send-approve';
            }
        },
        currentStep: function (e, el) {
            console.log(e, el);
        },
        toggleNext: function (e, el) {
            var className = 'collapse';
            $(el).next().toggleClass( className );
        },
        authPopup: function (e, el) {
            var h = $(document).height();
            $('.fade-alert').height(h);
            $('.fade-alert').fadeIn(300);

            // Скрытие при клике вне области блока
            $('.fade-alert').click(function (e) {
                var itemEl = $('.fade-alert .alert');

                if ( e.target != itemEl[0] && $('.fade-alert .alert').has(e.target).length === 0 ){
                    $('.fade-alert').fadeOut(300);
                }
            });
        },
        getPopup: function (e, el) {
            var h = $(document).height();
            $('.popup-layout').height(h);
            $('.popup-layout').fadeIn(300);

            // Скрытие при клике вне области блока
            $('.popup-layout').click(function (e) {
                var itemEl = $('.popup-layout .popup');

                if ( e.target != itemEl[0] && $('.popup-layout .popup').has(e.target).length === 0 ){
                    $('.popup-layout').fadeOut(300);
                }
            });
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
