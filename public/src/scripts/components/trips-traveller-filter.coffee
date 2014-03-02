`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
api = require "api"

Select = require "select"
Slider = require "slider"
Highlight = require "highlight"

TripsTravellerFilter = React.createClass
  render: ->
    `(
      <div className="trips-filter trips-traveller-filter">
        <div className="title">
          Компания и 
          <Highlight className="link--style-red" color="#f2555d" target="promo-travellers"> попутчики</Highlight>
        </div>
        <div className="trips-filter-container">
          <div className="trips-filter-container-column">
            <div><Select className="selectize-type--button"/></div>
          </div>
          <div className="trips-filter-container-column">
            <div>
              <Slider
                label="ВОЗРАСТ"
                  values={[20,50]}
                  min="20"
                  max="60"/>
              </div>
          </div>
          <div className="trips-filter-container-column trips-filter-container-column-color">
            <div>
              <Slider
                value={50}
                int={false}
                label="ПОЛ"
                min="M"
                max="Ж"/>
            </div>
          </div>
        </div>
      </div>
    )`

module.exports = TripsTravellerFilter
