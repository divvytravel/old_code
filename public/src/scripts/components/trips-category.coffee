`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
api = require "api"

TripsCategory = React.createClass
  render: ->
    `(
      <div className="trips-filter-category">
        <a className="button--type-category">Активный отдых</a>
        <a className="button--type-category">Концерты</a>
        <a className="button--type-category">Походы</a>
        <a className="button--type-category">Футбол</a>
        <a className="button--type-category">Экскурсии</a>
        <a className="button--type-category button--type-open-category">Все категории</a>
      </div>
    )`

module.exports = TripsCategory
