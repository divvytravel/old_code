
define([
    'marionette',
    'rivets',
    'templates',
    'vent',
    'dropzone',
    'moment',
    'bootstrap-datepicker',
    'selectize',
    'rivets-adapter',
    'native-trigger',
], function (Marionette, Rivets, Templates, Vent, Dz, Moment) {
    'use strict';

    function triggerEvent(element, eventName) {
        // safari, webkit, gecko
        if (document.createEvent)
        {
        var evt = document.createEvent('HTMLEvents');
        evt.initEvent(eventName, true, true);
     
            return element.dispatchEvent(evt);
        }
     
        // Internet Explorer
        if (element.fireEvent) {
            return element.fireEvent('on' + eventName);
        }
    }
    
    var liveValue = Object.create(Rivets.binders.value);

    liveValue.bind = function (el) {
        console.log('live1', el);
        this.handler = this.handler || this.publish.bind(this);
        el.addEventListener("keyup", this.handler);
    };

    liveValue.unbind = function (el) {
        console.log('live2', el);
        if (this.handler) {
            el.removeEventListener("keyup", this.handler);
        }
    };

    Rivets.binders["live-value"] = liveValue;

    // +++

    var View = Marionette.ItemView.extend({
        template : Templates.mainForm,

        ui: {
            startDate: "#startDate",
            inputDate: ".input-date",
            selectPriv: "#selectPriv",
            tagsInput: "#tagsInput",
            chipinSelect: ".chipin-select",
            mainPhotoPart: ".main-photo-part",
            additionPhotoPart: ".addition-photo-part",
            setAlert: ".set-alert",
            setAlertSelectize: ".set-alert input",
            actionCreate: ".action-create",
            actionAddChipinItem: ".action-add-chipin-item",
        },

        events: {
            "click @ui.actionCreate": "createTrip",
            "click @ui.actionAddChipinItem": "addChipinItem",
        },

        modelEvents: {
            'change': "modelChanged"
        },

        modelChanged: function() {
            // this.render();
            console.log('changed', this.model.toJSON());
            this.bindUIElements();
            this.startChipinSelect(true);
            // this.$el.find('pre').text(this.jsonData());
        },

        errors: {
            isSet: false
        },

        jsonData: function () {
            return JSON.stringify(this.model.toJSON(), null, '    ');
        },

        addChipinItem: function (e) {
            console.log('Add Chip In', this);
            this.model.get('chipinItems').add({});
            this.modelChanged();
        },

        createTrip: function (e) {
            var self = this;
            var _model = this.model.clone();
            _model.set('city', "/api/v1/city/1/");
            var start_date = this.model.get('start_date') || '';
            var end_date = this.model.get('end_date') || '';
            var end_people_date = this.model.get('end_people_date') || '';
            if (start_date.length) {
                _model.set('start_date', Moment(start_date, "DD-MM-YYYY").format('YYYY-MM-DD'));
            }
            if (end_date.length) {
                _model.set('end_date', Moment(end_date, "DD-MM-YYYY").format('YYYY-MM-DD'));
            }
            if (end_people_date.length) {
                _model.set('end_people_date', Moment(end_people_date, "DD-MM-YYYY").format('YYYY-MM-DD'));
            }
            Vent.trigger('global','allReady',false);
            _model.save(null,{
                wait: true,
                success: function(model, response){
                    // Vent.trigger('allReady',true);
                    Vent.trigger('global','allReady',true);
                },
                error: function(){
                    self.errors['isSet'] = true;
                    // Vent.trigger('allReady',true);
                    Vent.trigger('global','allReady',true);
                },
                attrs: _.omit(_model.attributes, ['chipinItems'])
            });
        },

        onRender: function() {
            var self = this;

            this.binder = Rivets.bind(this.el, { model: this.model, errors: this.errors });
            // this.model.set( 'output', this.getLinks(this.model) );
            this.startInputDate();
            this.startSelectPriv();
            this.startTagsInput();
            this.startChipinSelect();
            this.startMainPhotoUploader();
            this.startAdditionPhotoUploader();
            self.startAlerts();

        },

//        render: function() {
//            console.log(this.model);
//            this.$el.html( this.template( this.model.toJSON() ) );
//        }

        startMainPhotoUploader: function() {
            var self = this;

            // mainPhotoPart
            var previewTpl = self.$el.find('#previewMainPhotoTpl').html();
            var myDz = new Dz(self.ui.mainPhotoPart[0], {
                url: '/api/v1/image/',
                paramName: 'image',
                // autoProcessQueue: false,
                thumbnailWidth: 250,
                thumbnailHeight: 175,
                maxFiles: 1,
                maxFilesize: 5,
                uploadMultiple: false,
                previewTemplate: previewTpl,
                previewsContainer: self.$el.find('.preview-container')[0],
                clickable: self.ui.mainPhotoPart.find('.upload-link')[0],
                init: function() {
                    var myDropzone = this;
                    var el = self.ui.mainPhotoPart;

                    this.on("addedfile", function() {
                      if (this.files[1]!=null){
                        this.removeFile(this.files[0]);
                      }
                    });

                    this.on("totaluploadprogress", function(progress) {
                        el.find(".total-progress .progress-bar").width(progress + "%");
                    });

                    this.on("sending", function(file) {
                        el.find(".total-progress").css('opacity', 1);
                    });
                    
                    this.on("queuecomplete", function(progress) {
                        el.find(".total-progress").css('opacity', 0);
                    });

                    this.on("success", function(file, response) {
                        console.log('success', file, response);
                    });

                    this.on("error", function(file, response) {
                        console.log('error', file, response);
                    });
                }
            });
        },

        startAdditionPhotoUploader: function() {
            var self = this;

            // mainPhotoPart
            var previewTpl = self.$el.find('#previewAdditionPhotoTpl').html();
            var myDz = new Dz(self.ui.additionPhotoPart[0], {
                url: '/api/v1/image/',
                paramName: 'image',
                // autoProcessQueue: false,
                resize: function(file) {
                    var w = file.width,
                        h = file.height;
                    var nh = 80,
                        nw = nh * w / h;
                    return {
                        srcX: 0,
                        srcY: 0,
                        srcWidth: w,
                        srcHeight: h,
                        trgX: 0,
                        trgY: 0,
                        trgWidth: nw,
                        trgHeight: nh,
                    }
                },
                maxFiles: 6,
                maxFilesize: 5,
                uploadMultiple: false,
                previewTemplate: previewTpl,
                previewsContainer: self.ui.additionPhotoPart.find('.preview-container')[0],
                clickable: self.ui.additionPhotoPart.find('.upload-link')[0],
                init: function() {
                    var myDropzone = this;
                    var el = self.ui.additionPhotoPart;

                    // $(".dz-remove").on("click", function(e) {
                    //   myDropzone.removeAllFiles();
                    //   self.avatarSet(false);
                    //   self.userUploadedAvatar('');
                    //   self.userUploadedAvatarError('');
                    // });

                    this.on("totaluploadprogress", function(progress) {
                      el.find(".total-progress .progress-bar").width(progress + "%");
                    });

                    this.on("sending", function(file) {
                      el.find(".total-progress").css('opacity', 1);
                    });
                    
                    this.on("queuecomplete", function(progress) {
                      el.find(".total-progress").css('opacity', 0);
                    });

                    this.on("success", function(file, response) {
                        console.log('success', file, response);
                    });

                    this.on("error", function(file, response) {
                        console.log('error', file, response);
                    });
                }
            });
        },

        startInputDate: function() {
            var self = this;

            this.ui.inputDate.datepicker({
                format: "dd-mm-yyyy",
                autoclose: true,
                language: "ru",
                // startDate: start.format('MM-YYYY'),
                // endDate: end.format('MM-YYYY')
            }).on('changeDate', function(e){
                console.log('change val', this);
                $(this).nativeTrigger( "change" );
                // triggerEvent(this, "onchange" );
            });

        },

        startChipinSelect: function(focus) {
            var self = this;
            focus = focus || false;
            
            var chipinData = [
                {
                    id:1,
                    title:"Квартиру",
                    tag:"Шаринг жилья",
                    url:"https://www.airbnb.ru"
                },
                {
                    id:2,
                    title:"Отель",
                    tag:"Шаринг жилья",
                    url:"http://www.booking.com"
                },
                {
                    id:3,
                    title:"Экскурсию",
                    tag:"Экскурсионный тур",
                    url:"http://www.excursiopedia.com/ru"
                },
                {
                    id:4,
                    title:"Авто",
                    tag:"Шаринг авто",
                    url:"https://www.hertz.com/"
                },
                {
                    id:5,
                    title:"Яхту",
                    tag:"Яхтинг",
                    url:"http://www.miramoclub.com"
                },
                {
                    id:6,
                    title:"Шкипера",
                    tag:"Яхтинг",
                    url:""
                },
                {
                    id:7,
                    title:"Языковой тур",
                    tag:"Языки",
                    url:""
                },
                {
                    id:8,
                    title:"Готовый тур от агентства",
                    tag:"Пакетные туры",
                    url:""
                },
                {
                    id:9,
                    title:"Серфинг",
                    tag:"Серф",
                    url:""
                },
                {
                    id:10,
                    title:"Виндсерфинг",
                    tag:"Виндсерфинг",
                    url:""
                },
                {
                    id:11,
                    title:"Гастрономический тур",
                    tag:"Гастро тур",
                    url:""
                },
            ];

            var select, $select;
            var selectEl = this.$('.chipin-block .chipin-item:last select.chipin-select').not('.selectized');
            console.log('sel el', focus, selectEl);
            if (selectEl.length) {
                $select = selectEl.selectize({
                    create: false,
                    dropdownParent: 'body',
                    options: chipinData,
                    valueField: 'id',
                    labelField: 'title',
                    searchField: 'title',
                    sortField: 'id',
                    render: {
                        // item: function(data, escape) {
                        //     return '<div>"' + escape(data.title) + '"</div>';
                        // }
                    },
                    onChange: function(value) {
                        // console.log('Chipin Change', this.$input[0], this, value);
                        var result = this.options[value] || {},
                            el = this.$input.parents(":eq(2)").next().find('.chipin-link');
                            console.log('rrr', $.isEmptyObject(result) );
                        !$.isEmptyObject(result) && result.url.length ? el.html('<a target="_blank" href="'+result.url+'">'+result.url+'</a>') : el.html('');
                    } 
                });

                focus && $select[0].selectize.focus();
            }
            
        },

        startSelectPriv: function() {
            var self = this;

            this.ui.selectPriv.selectize({
                create: false,
                // sortField: {
                //     field: 'text',
                //     direction: 'asc'
                // },
                onChange: function(value) {
                    self.ui.selectPriv.nativeTrigger( "change" );
                },
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

        startAlerts: function() {
            var self = this;

            var alertData = [
                {
                    id:"title",
                    title:"Понятный заголовок",
                    text:"<p>Например, «Яхтинг на Карибах».</p><p>Понятный заголовок поможет вам быстро собрать группу. В заголовке содержится информация о формате и сути путешествия, а не его оценка.</p>"
                },
                {
                    id:"start_date",
                    title:"Дата начала",
                    text:"<p>Дату необходимо вводить так-то и так-то. Обратите внимание на то-то и то-то.</p>"
                },
                {
                    id:"trip_type",
                    title:"Тип поездки",
                    text:"<p>Здесь будет инфа.</p>"
                },
                {
                    id:"",
                    title:"Тестовый балун",
                    text:"<p>Здесь будет инфа.</p>"
                },
            ];

            var alertTpl = _.template('<div class="title"><%= title %></div> <%= text %>');

            this.ui.setAlert.focus(function(e){
                var dataId = $(e.currentTarget).data('alertId') || '';
                var data = _.findWhere(alertData, {id: dataId});

                if (data) {
                    var position = $(e.currentTarget).position();
                    var newTop = position.top - 30;
                    $('.alert-bal').html( alertTpl(data) ).css('top', newTop+'px').stop(true, true).fadeIn(400);
                }
            });

            this.ui.setAlert.blur(function(e){
                $('.alert-bal').stop(true, true).fadeOut(100);
            });

            // this.bindUIElements();

            this.$(this.ui.setAlertSelectize.selector).on('focus', function(e){
                var dataId = $(e.currentTarget).parent().parent().prev().data('alertId') || '';
                var data = _.findWhere(alertData, {id: dataId});

                if (data) {
                    var position = $(e.currentTarget).parent().parent().prev().parent().position();
                    var newTop = position.top - 30;
                    $('.alert-bal').html( alertTpl(data) ).css('top', newTop+'px').stop(true, true).fadeIn(400);
                }
            });

            this.$(this.ui.setAlertSelectize.selector).on('blur', function(e){
                $('.alert-bal').stop(true, true).fadeOut(100);
            });
        },

    });

    return View;

});
