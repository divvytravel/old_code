`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
$ = require "jquery"
require "iCheck"

Checkbox = React.createClass
  getDefaultProps: ->
    label: null
    type: "normal"

  componentDidMount: (domNode) ->
    $(domNode).iCheck
      checkboxClass: "checkbox-input"

    $(domNode).iCheck "check" if @props.checked

  render: ->
    classes = ["checkbox"]
    classes.push "checkbox-thin" if @props.type is "thin"

    `(
      <div className={classes.join(" ")}>
        <label>
          <input type="checkbox"></input>
          <span className="checkbox-label">{this.props.label}</span>
        </label>
      </div>
    )`

module.exports = Checkbox
