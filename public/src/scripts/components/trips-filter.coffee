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
      value: "3,10"
    }, {
      text: "10–30 человек",
      value: "10,30"
    }, {
      text: "> 30",
      value: "30,9999"
    }]

  getInitialState: ->
    filters: {},
    countries: []

  componentWillMount: ->
    api.get "trip", {}, (data) =>
      countries = []
      for trip in data.objects
        if countries.indexOf(trip.country) is -1
          countries.push
            text: trip.country 
            value: trip.country
      @setState countries: countries

  handleFilterChange: (filter, value) ->
    value = value.toString() if typeof(value) is "object"
    filters = @state.filters
    filters[filter] = value
    @setState filters: filters
    @props.onChange filters if @props.onChange

  render: ->
    `(
      <div className="trips-filter" id="promo-filters">
        <div className="title">Путешествие</div>
        <div className="trips-filter-container">
          <div className="trips-filter-container-column">
            <div><DateInput onChange={this.handleFilterChange.bind(this, 'start_date__gt')}/></div>
            <div className="trips-filter-or-separator">или...</div>
            <div>
              <Select
                placeholder="Куда"
                className="selectize-type--button"
                options={this.state.countries}
                multiple={false}
                onChange={this.handleFilterChange.bind(this, 'country')}
              />
            </div>
          </div>
          <div className="trips-filter-container-column">
            <div>
              <Slider
                label="СТОИМОСТЬ"
                min="100"
                max="4000"
                unit="$"
                values={[100, 3000]}
                onChange={this.handleFilterChange.bind(this, 'price__range')}
              />
            </div>
            <div className="trips-filter-flight">
              <Checkbox checked="true"  label="С перелетом из "/>
            </div>
          </div>
          <div className="trips-filter-container-column">
            <div className="trips-filter-groups-title">ГРУППЫ</div>
            <div className="trips-filter-groups">
              <CheckGroup
                options={this.props.groups}
                onChange={this.handleFilterChange.bind(this, 'people_count__range')}/>
            </div>
          </div>
        </div>
      </div>
    )`

module.exports = TripsFilter
