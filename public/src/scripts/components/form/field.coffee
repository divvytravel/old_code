`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
api = require "api"


Field = React.createClass
  render: ->
    @transferPropsTo(
      `(
        <div className="field">{this.props.children}</div>
      )`
    )

module.exports = Field
