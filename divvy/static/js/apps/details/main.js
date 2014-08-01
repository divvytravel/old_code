require([
    'jquery',
    'rivets',
    'dataProvider',
    'fotorama'
], function ($,Rivets,DataProvider) {

    var RequestClass = function (data) {
        this.id = data.get('tripId') || 0;
        this.resource_uri = '/api/v1/trip/'+this.id+'/';
    };
    RequestClass.prototype = {
        send: function () {
            var self = this;

            $.ajax({
                type: "POST",
                url: "/api/v1/triprequest/",
                data: {"trip": self.resource_uri},
                dataType:"json",
                contentType:"application/json; charset=utf-8",
                success: function(data) {
                    console.log('Success',data);
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
    }

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
