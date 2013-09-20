(function($)  {
  'use strict'

  // Set CSRF
  function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) == (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');

  function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
      crossDomain: false, // obviates need for sameOrigin test
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type)) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  })
  // End of set CSRF

  var AJAX_TIMEOUT = 10000;
  var DELAY_BEFORE_HIDE = 1000;
  var answerForm = null;
  var currentThreadId = null;
  var currentPostId = null;
  var currentPageApprovedValue = null;
  var status;
  var ajaxLoaderImg = "<img class='ajax-loader' src='/static/img/loading.gif'/>"
  var ajaxLoaderImgUsers = "<img class='ajax-loader loader-users' src='/static/img/loading.gif'/>"
  var ajaxLoaderImgTrips = "<img class='ajax-loader loader-trips' src='/static/img/loading.gif'/>"
  var ajaxFade = "<div class='fade-elem'></div>"

  // First, checks if it isn't implemented yet.
  if (!String.prototype.format) {
    String.prototype.format = function() {
      var args = arguments;
      return this.replace(/{(\d+)}/g, function(match, number) {
        return typeof args[number] != 'undefined'
          ? args[number]
          : match
        ;
      });
    };
  }

  function validateEmail(addr) {
      return /.@./.test(addr)
  }

  function getAllCommentElems(commentButtonElem){
    var comment_row = commentButtonElem.closest('tr')
    return comment_row;
  }

  function submitForm(e) {
    e.preventDefault();
    var form = $(this);
    var data = {thread_id: currentThreadId, post_id: currentPostId};


      var required = [
        'author',
        'author_email',
        'content',
        'csrfmiddlewaretoken'
      ],
          valid = true

      var elements = form.get(0).elements
      valid = required.every(function (name) {
          var el = elements[name],
              value = el && el.value
          if (el && !value) {
              alert("Поле "+name+" не заполнено")
              return false
          }
          if ('author_email' === name) {
              if (!validateEmail(value)) {
                  alert("Поле E-mail заполнено неверно")
                  return false
              }
          }
          data[name] = value
          return true
      })

      if (valid){
        var ajaxLoaderElem=$(ajaxLoaderImg);
        form.closest('ul').after(ajaxLoaderElem);
        $.ajax({
          async: true,
          data: data,
          traditional: true,
          dataType: 'json',
          timeout: AJAX_TIMEOUT,
          error: function(XHR, textStatus, errorThrown)   {
            status = true;
          },
          success: function(data, textStatus) {
            if (!data.error){
              answerForm.hide();
              var answerConfirmed = "<div class='ajax-action-message'>";
              if (currentPageApprovedValue == 0 && data.approved == 1){
                answerConfirmed += "Комментарий одобрен. ";
              }
              answerConfirmed += "Ответ сохранен.</div>";
              var answerConfirmedElem = $(answerConfirmed);
              answerForm.after(answerConfirmedElem);

              var elemToHide;
              if (currentPageApprovedValue != data.approved){
                elemToHide = getAllCommentElems(answerForm);
              } else {
                elemToHide = answerConfirmedElem;
              }
              elemToHide.delay(DELAY_BEFORE_HIDE).fadeOut('slow');
            } else {
              /* TODO */
            }
          },
          complete: ajaxLoaderElem.remove(),
          type: form.attr('method'),
          url: form.attr('action')
        });
      } else {
        /* Nothing to do */
      }

    return false;

  }

  function cleanContent(){
    if (answerForm){
      answerForm.find('form').get(0).reset()
    }
  }

  function cancelForm(e){
    answerForm.hide();
  }


  function show_answer_form(link){
    currentThreadId = link.data('thread_id');
    currentPostId = link.data('post_id');
    link.after(answerForm);
    answerForm.show();
  }

  function render_trips(trip_list_elem, trips){
      for (var k=0; k<trips.length; k++){
        var count_gender = ""
        if (trips[k].count_male || trips[k].count_female){
          count_gender += "(";
            if (trips[k].count_male){
              count_gender += trips[k].count_male + "м";
              if (trips[k].count_female){
                count_gender += " "
              }
            }
            if (trips[k].count_female){
              count_gender += trips[k].count_female + "ж";
            }
          count_gender += ")"
        }
        trip_list_elem.append('\
<tr>\
  <td>\
      <a href="{0}">{1} - {2}</a>\
  </td>\
  <td>\
      <a href="{0}">{3}</a>\
  </td>\
  <td>\
      <a href="{0}">{4}</a>\
  </td>\
  <td>\
      {5} {6}\
  </td>\
  <td>{7} человек {8}</td>\
</tr>\
'.format(
          trips[k].get_absolute_url,
          trips[k].start_date_format,
          trips[k].end_date_format,
          trips[k].city,
          trips[k].title,
          trips[k].price,
          trips[k].get_currency_display,
          trips[k].count_all_people,
          count_gender
          ));
        console.log(trips[k]);
      }
  }

  $.fn.post_form_on_change = function(given_date){
    var ajaxFadeElemUsers = $(ajaxFade);
    var user_list = $('.users-list');
    user_list.prepend(ajaxFadeElemUsers);
    var ajaxLoaderElemUsers=$(ajaxLoaderImgUsers);
    user_list.prepend(ajaxLoaderElemUsers);

    var trip_list = $('.trip-list tbody');
    var ajaxFadeElemTrips = $(ajaxFade);
    trip_list.prepend(ajaxFadeElemTrips);
    var ajaxLoaderElemTrips=$(ajaxLoaderImgTrips);
    trip_list.prepend(ajaxLoaderElemTrips);

    return this.each(function() {
      var this_elem = $(this)
        var this_form = this_elem.closest('form');
        var date;
        if (typeof given_date === "undefined"){
          date = this_form.find('input[name="month_year"]').val()
        } else {
          date = given_date;
        }
        var form_data = {
          'month_year': date,
          'country': this_form.find('select[name="country"]').val(),
          'gender': this_form.find('select[name="gender"]').val(),
          'age_from': this_form.find('select[name="age_from"]').val(),
          'age_to': this_form.find('select[name="age_to"]').val(),
        }
        var users = this_form.find('select[name="users"]').val()
        if (users !== null){
          form_data['users'] = users;
        }
        $.ajax({
          async: true,
          data: form_data,
          traditional: true,
          dataType: 'json',
          timeout: AJAX_TIMEOUT,
          error: function(XHR, textStatus, errorThrown)   {
            status = true;
          },
          success: function(data, textStatus) {
            if (!data.error || data.error.length==0){
              console.log("ajax success")
              console.log(data)
              trip_list.find('tr').remove();
              // var trips = JSON.parse(data.trips);
              render_trips(trip_list, data.trips);
            } else {
              alert("Произошла ошибка: "+data.error)
            }
          },
          complete: function(){
            ajaxLoaderElemUsers.remove();
            ajaxFadeElemUsers.remove();
            ajaxLoaderElemTrips.remove();
            ajaxFadeElemTrips.remove();
          },
          type: 'POST',
          url: this_form.attr('action')
        });
      // })
    })
  }

// $( "#searchForm" ).submit(function( event ) {

//   // Stop form from submitting normally
//   event.preventDefault();

//   // Get some values from elements on the page:
//   var $form = $( this ),
//     term = $form.find( "input[name='s']" ).val(),
//     url = $form.attr( "action" );

//   // Send the data using post
//   var posting = $.post( url, { s: term } );

//   // Put the results in a div
//   posting.done(function( data ) {
//     var content = $( data ).find( "#content" );
//     $( "#result" ).empty().append( content );
//   });
// });


  //       if (dataElem.data('reply') == 1){
  //         if (answerForm!=null){
  //           cleanContent();
  //           show_answer_form(dataElem);
  //         } else {
  //           var ajaxLoaderElem=$(ajaxLoaderImg);
  //           dataElem.after(ajaxLoaderElem);
  //           $.ajax({
  //             async: true,
  //             data: {},
  //             traditional: true,
  //             dataType: 'json',
  //             timeout: AJAX_TIMEOUT,
  //             error: function(XHR, textStatus, errorThrown)   {
  //               status = true;
  //             },
  //             success: function(data, textStatus) {
  //               if (!data.error || data.error.length==0){
  //                 answerForm = $(data.form);
  //                 answerForm.find('form').submit(submitForm);
  //                 show_answer_form(dataElem);
  //                 $('#cancel-reply').click(cancelForm);
  //               } else {
  //                 alert("Произошла ошибка: "+data.error)
  //               }
  //             },
  //             complete: ajaxLoaderElem.remove(),
  //             type: 'POST',
  //             url: this_link.attr('href')
  //           });
  //         }
  //       } else {
  //         alert("Для данного комментария превышена глубина ответов");
  //       }
  //       return false;
  //     });
  //   });
  // };


})(jQuery);
