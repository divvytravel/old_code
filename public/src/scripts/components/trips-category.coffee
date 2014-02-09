`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
api = require "api"

TripsCategory = React.createClass
  render: ->
    `(
      <div className="trips-category">
        
      </div>
    )`

module.exports = TripsCategory
