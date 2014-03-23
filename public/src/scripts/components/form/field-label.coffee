`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
api = require "api"


FieldLabel = React.createClass
  render: ->
    @transferPropsTo(
      `(
        <label className="field-label">{this.props.children}</label>
      )`
    )

module.exports = FieldLabel
