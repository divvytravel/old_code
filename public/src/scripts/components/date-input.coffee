`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
$ = require "jquery"

require "jquery.ui.datepicker"

DateInput = React.createClass
  getInitialState: ->
    show: false

  componentDidMount: ->
    $(@refs.datepicker.getDOMNode()).datepicker()

  handleShow: ->
    @setState show: not @state.show

  render: ->
    styles =
      display: if @state.show then "block" else "none"

    `(
      <span className="date-input">
        <a className="button button--type-action" onClick={this.handleShow}>
          Кнопка
          <i className="button-picker icon-calendar-blue"></i>
        </a>
        <span ref="datepicker" style={styles} className="date-input--datepicker"></span>
      </span>
    )`

module.exports = DateInput
