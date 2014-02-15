`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
api = require "api"

Select = require "select"
Slider = require "slider"

TripsTravellerFilter = React.createClass
  render: ->
    `(
      <div className="trips-filter trips-traveller-filter">
        <div className="title">Компания и попутчики</div>
        <div className="trips-filter-container">
          <div className="trips-filter-container-column">
            <div><Select className="selectize-type--button"/></div>
          </div>
          <div className="trips-filter-container-column">
            <div><Slider label="ВОЗРАСТ" min="20" max="60"/></div>
          </div>
          <div className="trips-filter-container-column">
            <div><Slider label="ПОЛ" min="0" max="0"/></div>
          </div>
        </div>
      </div>
    )`

module.exports = TripsTravellerFilter
