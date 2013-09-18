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
  var ajaxLoaderImg = "<img style='float:right;' src='/static/img/ajax-loader.gif'/>"

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

  $.fn.post_form_on_change = function(){
    return this.each(function() {
      var this_elem = $(this)
      // this_elem.click(function(){
        var this_form = this_elem.closest('form');
        var form_data = {
          'date': this_form.find('input[name="date"]').val(),
          'where': this_form.find('input[name="where"]').val(),
          'gender': this_form.find('select[name="gender"]').val(),
          'age_from': this_form.find('input[name="age_from"]').val(),
          'age_to': this_form.find('input[name="age_to"]').val(),
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
              console.log("data")
              console.log(data)
            } else {
              alert("Произошла ошибка: "+data.error)
            }
          },
          // complete: ajaxLoaderElem.remove(),
          complete: console.log("ajax done"),
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
