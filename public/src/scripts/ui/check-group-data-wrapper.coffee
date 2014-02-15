`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
CheckGroup = require "check-group"

CheckGroupDataWrapper = React.createClass
  getDefaultProps: ->
    options: [{
      text: "Кнопка",
      value: "default"
    },{
      text: "Ховер",
      value: "hover"
    },{
      text: "Включ.",
      value: "active"
    },{
      text: "Ховер  на вкл.",
      value: "hover-active"
    }]

  render: ->
    `(
      <CheckGroup options={this.props.options} value="active"/>
    )`

module.exports = CheckGroupDataWrapper
