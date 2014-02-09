`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
moment = require "moment"
api = require "api"

TripsFilter = require "trips-filter"
TripsCategory = require "trips-category"
TripsTravellerFilter = require "trips-traveller-filter"
TravellersList = require "travellers-list"

Trips = React.createClass
  getInitialState: ->
    loaded: false
    trips: []
    meta: {}

  componentWillMount: (domNode) ->
    api.get "trip", limit: 3, (data) =>
      @setState
        loaded: true
        trips: data.objects
        meta: data.meta

  load: ->
    api.get "trip", limit: @state.meta.total_count, offset: @state.meta.limit, (data) =>
      @setState
        trips: @state.trips.concat data.objects
        meta: data.meta

  getTripPeriod: (trip) ->
    start = moment(trip.start_date, "YYYY-MM-DD")
    end = moment(trip.end_date, "YYYY-MM-DD")

    if start.month() is end.month()
      period = "#{start.format("DD")} – #{end.format("DD MMMM")}"
    else
      period = "#{start.format("DD MMMM")} – #{end.format("DD MMMM")}"

    period

  getLocaleCurrency: (currency) ->
    currencies = rub: "руб.", euro: "евро", usd: "дол."
    currencies[currency]

  getLocaleType: (type) ->
    types = "noncom": "Некоммерческая", "com": "Коммерческая"
    types[type]

  renderTrips: ->
    @state.trips.map (trip) =>
      renderTags = @renderTags
      renderTripInfo = @renderTripInfo
      return `(
        <div className="trips-item">
          <div className="trips-item-title">
            <a href="#">{trip.title}</a>
            <span className="trips-item-title-star"></span>
          </div>
          <div className="trips-item-tour">
            {[trip.country, trip.city].join(" → ")}
          </div>
          <div className="trips-item-tags">
            {renderTags(trip.tags)}
          </div>
          <div className="trips-item-content">
            <div className="trips-item-preview">
              <img src={trip.image} />
            </div>
            {renderTripInfo(trip)}
          </div>
        </div>
      )`

  renderTags: (tags) ->
    tags.map (tag) ->
      return `(
        <a href={"/" + tag.slug} className="tag">{tag.name}</a>
      )`

  renderTripInfo: (trip) ->
    console.log trip
    `(
      <div className="trips-item-info">
        <div className="trips-item-info-title">
          <span className="calendar-black"></span>
          <span>{this.getTripPeriod(trip)}</span>      
        </div>
        <div className="trips-item-info-detail">
          <div className="trips-item-info-price">
            {trip.price + " " + this.getLocaleCurrency(trip.currency)}
          </div>
          <div className="trips-item-info-type">
            {this.getLocaleType(trip.price_type)} поездка
          </div>
        </div>
        {this.renderTravellers(trip)}
      </div>
    )`

  renderTravellersList: (travellers) ->
    travellers.map (traveller) ->
      `(
        <div className="travellers-item-icon">
          <a href={traveller.resource_uri}>
            <img src={traveller.avatar_url}/>
          </a>
        </div>
      )`

  renderTravellers: (trip) ->
    genders = trip.people.filter (people) -> people.gender

    if genders.length > (trip.people.length - genders.length)
      ratio = "девушки"
    else
      ratio = "парни"

    `(
      <div className="trip-item-info-travellers">
        <div className="trip-item-info-travellers-title">
          Компания
        </div>
        <div className="trip-item-info-travellers-ratio">
          <div>Набрано {trip.people.length} из {trip.people_count} человек</div>
          <div>Преимущественно {ratio}</div>
        </div>
        <TravellersList travellers={trip.people}/>
      </div>
    )`

  renderLoadNextButton: ->
    return `(
      <div className="trips-next">
        <a onClick={this.load} className="button button--color-blue">
          Все {this.state.meta.total_count} путешествия
        </a>
      </div>
    )` if @state.meta.next

  render: ->
    `(
      <div>
        <TripsFilter/>
        <TripsCategory/>
        <TripsTravellerFilter/>
        <div className="trips">
          {this.renderTrips()}
          {this.renderLoadNextButton()}
        </div>
      </div>
    )`

module.exports = Trips
