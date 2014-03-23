`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
api = require "api"

Nonprofit = require "nonprofit"

Trip = React.createClass
  getDefaultProps: ->
    type: "nonprofit"

  render: ->
    if @props.type is "nonprofit"
      return `(<Nonprofit/>)`

module.exports = Trip
