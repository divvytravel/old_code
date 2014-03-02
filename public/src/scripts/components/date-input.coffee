`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
$ = require "jquery"

require "jquery.ui.datepicker"
require "moment"

initDatepickerLang = ->
  if not window.datepicker_i18n or window.datepicker_i18n isnt "en"
    $.datepicker.setDefaults
      closeText: "Закрыть"
      prevText: "&#x3c;"
      nextText: "&#x3e;"
      currentText: "Сегодня"
      monthNames: [
        "Январь"
        "Февраль"
        "Март"
        "Апрель"
        "Май"
        "Июнь"
        "Июль"
        "Август"
        "Сентябрь"
        "Октябрь"
        "Ноябрь"
        "Декабрь"
      ]
      monthNamesShort: [
        "Янв"
        "Фев"
        "Мар"
        "Апр"
        "Май"
        "Июн"
        "Июл"
        "Авг"
        "Сен"
        "Окт"
        "Ноя"
        "Дек"
      ]
      dayNames: [
        "воскресенье"
        "понедельник"
        "вторник"
        "среда"
        "четверг"
        "пятница"
        "суббота"
      ]
      dayNamesShort: [
        "вск"
        "пнд"
        "втр"
        "срд"
        "чтв"
        "птн"
        "сбт"
      ]
      dayNamesMin: [
        "Вс"
        "Пн"
        "Вт"
        "Ср"
        "Чт"
        "Пт"
        "Сб"
      ]
      weekHeader: "Не"
      dateFormat: "dd.mm.yy"
      firstDay: 1
      isRTL: false
      showMonthAfterYear: false
      yearSuffix: "",
      #changeYear: true

setTimeout initDatepickerLang, 80

DateInput = React.createClass
  getInitialState: ->
    value: null

  componentDidMount: (domNode) ->
    $(@refs.datepicker.getDOMNode()).datepicker
      dateFormat: "yy-mm-dd"
      onSelect: @handleDateChange

  componentDidUpdate: (prevProps, prevState) ->
    @props.onChange @state.value unless prevState.value is @state.value

  handleDateChange: (date) ->
    @setState value: date

  handleShow: ->
    $(@refs.datepicker.getDOMNode()).datepicker "show"

  render: ->
    `(
      <span className="date-input">
        <a className="button button--type-action" onClick={this.handleShow}>
          <input ref="datepicker" type="text" className="date-input--datepicker"/>
          {this.state.value ? moment(this.state.value, "YYYY-MM-DD").format("DD MMMM YYYY") : 'Когда'}
          <i className="button-picker icon-calendar-blue"></i>
        </a>
      </span>
    )`

module.exports = DateInput
