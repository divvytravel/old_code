`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
$ = require "jquery"

require "jquery.ui.datepicker"

DateInput = React.createClass
  componentDidMount: ->
    $(@refs.input.getDOMNode()).datepicker
      showOn: "both"
      buttonImage: "/static/img/calendar-blue.png"
      buttonImageOnly: false

  render: ->
    `(
      <span className="input">
        <input ref="input" className="input-element" placeholder="Когда"></input>
      </span>
    )`

module.exports = DateInput
