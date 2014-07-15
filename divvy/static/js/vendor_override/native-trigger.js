(function($) {

    $.fn.nativeTrigger = function(eventName) {
        return this.each(function() {
            var el = $(this).get(0);
            triggerNativeEvent(el, eventName);
        });
    };

    function triggerNativeEvent(el, eventName){
      if (el.fireEvent) { // < IE9
        (el.fireEvent('on' + eventName));
      } else {
        var evt = document.createEvent('Events');
        evt.initEvent(eventName, true, false);
        el.dispatchEvent(evt);
      }
}

}(jQuery));
