(function($)  {
  'use strict'

    var AJAX_LOADER_SMALL = $("<img class='ajax-loader-small' src='/static/img/loading_small.gif'/>");
    var AJAX_LOADER_BIG = $("<img class='ajax-loader-big' src='/static/img/loading.gif'/>");
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

    function show_success(messages){
        for (var i=0; i<messages.length; i++){
        $(".container:last").prepend(
'<div class="alert alert-dismissable fade in alert-success">\
  <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>\
  <p>{0}</p>\
</div>'.format(messages[i]));
        }
    }


    function showRequest(formData, jqForm, options) { 
        $(".modal-footer").prepend(AJAX_LOADER_SMALL);
        AJAX_LOADER_SMALL.show();
        $("#modal_send").attr('disabled', 'disabled');
        // formData is an array; here we use $.param to convert it to a string to display it 
        // but the form plugin does this for you automatically when it submits the data 
        // var queryString = $.param(formData); 
     
        // // jqForm is a jQuery object encapsulating the form element.  To access the 
        // // DOM element for the form do this: 
        // // var formElement = jqForm[0]; 
     
        // alert('About to submit: \n\n' + queryString); 
     
        // here we could return false to prevent the form from being submitted; 
        // returning anything other than false will allow the form submit to continue 
        return true; 
    } 


    function showResponse(responseText, statusText, xhr, $form)  {
        AJAX_LOADER_SMALL.hide();
        $("#modal_send").removeAttr('disabled');
        var resp = JSON.parse(responseText);
        var frm = $('#myModal');
        if (resp.result == 'success'){
        //     clearErr(frm);
            show_success(resp.messages);
            frm.modal('toggle');
        } else {
        //     clearErr(frm);
        //     for (var err in resp.errors){
        //         if (err == 'avatar'){
        //             $('#addPhoto').addClass("err");
        //         } else {
        //             var fail_elem = frm.find('[name=' + err + ']');
        //             fail_elem.addClass("err");
        //         }
        //     }
        } 
    } 

    $.fn.ajax_send_message = function(){
        // require <script src="http://malsup.github.com/jquery.form.js"></script>
        var options = { 
            // target:        '#output1',   // target element(s) to be updated with server response 
            beforeSubmit:  showRequest,  // pre-submit callback 
            success:       showResponse  // post-submit callback 
     
            // other available options: 
            //url:       url         // override for form's 'action' attribute 
            //type:      type        // 'get' or 'post', override for form's 'method' attribute 
            //dataType:  null        // 'xml', 'script', or 'json' (expected server response type) 
            //clearForm: true        // clear all form fields after successful submit 
            //resetForm: true        // reset the form after successful submit 
     
            // $.ajax options can be used here too, for example: 
            //timeout:   3000 
        };
        return this.each(function() {
            $(this).ajaxForm(options);
            return false;
          })
    }

})(jQuery);

