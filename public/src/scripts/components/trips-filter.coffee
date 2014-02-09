`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
api = require "api"

DateInput = require "date-input"

TripsFilter = React.createClass
  render: ->
    `(
      <div className="trips-filter">
        <div className="title">Путешествие</div>
        <div className="trips-filter-container">
          <DateInput/>
        </div>
      </div>
    )`

module.exports = TripsFilter
