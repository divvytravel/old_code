
var substringMatcher = function(strs) {
  return function findMatches(q, cb) {
    var matches, substringRegex;
 
    // an array that will be populated with substring matches
    matches = [];
 
    // regex used to determine if a string contains the substring `q`
    substrRegex = new RegExp(q, 'i');
 
    // iterate through the pool of strings and for any string that
    // contains the substring `q`, add it to the `matches` array
    $.each(strs, function(i, str) {
      // console.log("op - ",str);
      if (substrRegex.test(str.value)) {
        // the typeahead jQuery plugin expects suggestions to a
        // JavaScript object, refer to typeahead docs for more info
        matches.push(str);
      }
    });
 
    cb(matches);
  };
};

$(function() {

  $( "#fPrice" ).slider({
    range: true,
    min: 100,
    max: 4000,
    values: [ 100, 3000 ],
    slide: function( event, ui ) {
      $( "#amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
    }
  });

  $( "#fAge" ).slider({
    range: true,
    min: 20,
    max: 40,
    values: [ 20, 40 ]
  });

  $( "#fGender" ).slider({
    // range: true,
    min: 0,
    max: 100,
    value: 50
  });

  // $( "#fDate" ).datepicker( {
  //   format: "mm-yyyy",
  //   viewMode: "months", 
  //   minViewMode: "months",
  //   language: "ru"
  // });

  var states = [
    {'value':'Москва','country':'Россия'},
    {'value':'Паттайя','country':'Тайланд'},
    {'value':'Пицунда','country':'Абхазия'},
    {'value':'Мосул','country':'Ирак'}
  ];

  $('#fPlaceTo').typeahead({
    hint: true,
    highlight: true,
    minLength: 1
  },
  {
    name: 'states',
    displayKey: 'value',
    source: substringMatcher(states),
    templates: {
      suggestion: Handlebars.compile('<p class="name-part">{{value}}</p> <p class="addition-part">{{country}}</p>')
    }
  });

  $('#fPlaceFrom').typeahead({
    hint: true,
    highlight: true,
    minLength: 1
  },
  {
    name: 'states',
    displayKey: 'value',
    source: substringMatcher(states),
    templates: {
      suggestion: Handlebars.compile('<p class="name-part">{{value}}</p> <p class="addition-part">{{country}}</p>')
    }
  });

  // $( "#fPlaceTo" ).select2({
  //   minimumResultsForSearch: -1
  // });

  // $( "#fPlaceFrom" ).select2({
  //   minimumResultsForSearch: -1
  // });

  $('.godown a').click(function(){
      var speed = 500;
      var to = $('.main-page').offset().top;
      
      $('html, body').animate({scrollTop: to}, speed);
      
      return false;
  });

  $( "#amount" ).val( "$" + $( "#fPrice" ).slider( "values", 0 ) +
    " - $" + $( "#fPrice" ).slider( "values", 1 ) );

});
