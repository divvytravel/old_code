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

  $.fn.apply_carousel = function(wait_to_load){
    return this.each(function() {
      var this_elem = $(this);
      if (wait_to_load){
        this_elem.hide();
      }
      function apply_c(){
        this_elem.show();
        this_elem.carouFredSel({
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
      }
      if (wait_to_load){
        $('.image_picker_image').load(function(){
          apply_c();
        });
      } else {
        apply_c();
      }
    })
  }

  $.fn.apply_image_picker_carousel = function(){
    return this.each(function() {
      var this_elem = $(this);
        this_elem.imagepicker({
          hide_select : true,
          show_label  : false,
          initialized: function(){
            $('.thumbnails').apply_carousel(true);
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
  <td>{9}</td>\
  <td>{10}</td>\
  <td>{11}</td>\
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
          count_gender,
          trips[k].show_price_type,
          trips[k].end_people_date_format,
          trips[k].show_people_places_left
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

  function render_trip_categories(trip_category_elem, trip_categories, selected_category){
    trip_category_elem.find('option').slice(1).remove();
    // trip_category_elem.append("<option>выберите категорию</option>");
    var selected = "";
    for (var k=0; k<trip_categories.length; k++){
      if (selected_category !== undefined && selected_category == trip_categories[k].pk){
        selected = 'selected="selected"';
      } else {
        selected = '';
      }
      trip_category_elem.append(
        '<option value="{0}" {1}>{2}</option>'.format(
            trip_categories[k].pk,
            selected,
            trip_categories[k].title
          )
      );
    }
  }

  $.fn.post_form_on_change = function(options){
    // default values for supported options
    var opts = {}
    if (typeof options === 'undefined'){
      opts.given_date = undefined
      opts.clear_data = undefined
    } else {
      opts.given_date = options.given_date || undefined
      opts.clear_data = options.clear_data || undefined
    }
    // end of options

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

    var trip_category_elem = $('#id_category');

    return this.each(function() {
      var this_elem = $(this)
        var this_form = this_elem.closest('form');
        var form_data;
        if (typeof opts.clear_data === "undefined"){
          var date;
          if (typeof opts.given_date === "undefined"){
            date = this_form.find('input[name="month_year"]').val()
          } else {
            date = opts.given_date;
          }
          form_data = {
            'month_year': date,
            'country': this_form.find('select[name="country"]').val(),
            'price_type': this_form.find('select[name="price_type"]').val(),
            'gender': this_form.find('select[name="gender"]').val(),
            'age_from': this_form.find('select[name="age_from"]').val(),
            'age_to': this_form.find('select[name="age_to"]').val(),
            'category': this_form.find('select[name="category"]').val(),
          }
          var users = this_form.find('select[name="users"]').val()
          if (users !== null){
            form_data['users'] = users;
          } 
        } else {
          form_data = {'clear': true};
          this_form.find('#id_month_year').val('');
          this_form.find('#id_country').val('');
          this_form.find('#id_price_type').val('');
          this_form.find('#id_gender').val('');
          this_form.find('#id_age_from').val(20);
          this_form.find('#id_age_to').val(50);
          this_form.find('#id_category').val('');
          // this_form.reset();
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
              render_trip_categories(trip_category_elem, data.trip_categories,
                data.selected_category)
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
