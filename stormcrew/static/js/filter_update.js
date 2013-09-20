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

  var AJAX_TIMEOUT = 0;
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

  $.fn.apply_image_picker_carousel = function(){
    return this.each(function() {
      var this_elem = $(this);
        this_elem.imagepicker({
          hide_select : true,
          show_label  : false,
          initialized: function(){
            $('.thumbnails').hide();
            $('.image_picker_image').load(function(){
                $('.thumbnails').show();
                $('.thumbnails').carouFredSel({
                    circular: false,
                    infinite: false,
                    auto    : false,
                    width   : "100%",
                    align   : "center",
                    prev    : {
                        button  : "#foo2_prev",
                        key     : "left"
                    },
                    next    : {
                        button  : "#foo2_next",
                        key     : "right"
                    },
                    // pagination  : "#foo2_pag"
                });
            });
          },
          clicked: function(){
            $(this).post_form_on_change();
          }
        })
      }
    )
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
      }
  }

  function render_users(user_list_elem, users, selected_users){
    $('.caroufredsel_wrapper').remove();
    var user_select = user_list_elem.find('select');
    user_select.find('option').remove();
    user_select.append("<option></option>");

    for (var k=0; k<users.length; k++){
      var selected = "";
      for (var j=0; j<selected_users.length; j++){
        if (users[k].pk == selected_users[j].pk){
          selected = ' selected="selected"';
          break;
        }
      }
      user_select.append(
        '<option data-img-src="{0}" value="{1}"{3}>{2}</option>'.format(
            users[k].get_avatar_url,
            users[k].pk,
            users[k].get_full_name,
            selected
          )
      );
    }
    user_select.apply_image_picker_carousel();
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
              trip_list.find('tr').remove();
              // var trips = JSON.parse(data.trips);
              render_trips(trip_list, data.trips);
              render_users(user_list, data.users, data.selected_users);
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
})(jQuery);