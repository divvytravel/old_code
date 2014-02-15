`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
api = require "api"

Checkbox = require "checkbox"
CheckGroup = require "check-group"
DateInput = require "date-input"
Select = require "select"
Slider = require "slider"

TripsFilter = React.createClass
  getDefaultProps: ->
    groups: [{
      text: "3–10 человек"
      value: "3-10"
    }, {
      text: "10–30 человек",
      value: "10-30"
    }, {
      text: "> 30",
      value: "30"
    }]

  render: ->
    `(
      <div className="trips-filter">
        <div className="title">Путешествие</div>
        <div className="trips-filter-container">
          <div className="trips-filter-container-column">
            <div><DateInput/></div>
            <div className="trips-filter-or-separator">или...</div>
            <div><Select className="selectize-type--button"/></div>
          </div>
          <div className="trips-filter-container-column">
            <div><Slider label="СТОИМОСТЬ" min="100 $" max="4000 $"/></div>
            <div className="trips-filter-flight">
              <Checkbox checked="true"  label="С перелетом из "/>
            </div>
          </div>
          <div className="trips-filter-container-column">
            <div className="trips-filter-groups-title">ГРУППЫ</div>
            <div className="trips-filter-groups">
              <CheckGroup options={this.props.groups}/>
            </div>
          </div>
        </div>
      </div>
    )`

module.exports = TripsFilter
