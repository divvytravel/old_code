`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"

MyComponent = React.createClass
  render: ->
    `(
      <div>sdjflksjdf</div>
    )`

module.exports = MyComponent
