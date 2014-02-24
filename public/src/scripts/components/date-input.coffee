`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
$ = require "jquery"

require "jquery.ui.datepicker"
require "moment"

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
