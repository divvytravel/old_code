`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
RadioGroup = require "radio-group"

RadioGroupDataWrapper = React.createClass
  getDefaultProps: ->
    multiple: false
    options: [{
      text: "Запостить в Фейсбук",
      value: "active"
    },{
      text: "Запостить в Фейсбук",
      value: "nonactive"
    }]

  render: ->
    `(
      <RadioGroup options={this.props.options} value="active"/>
    )`

module.exports = RadioGroupDataWrapper
