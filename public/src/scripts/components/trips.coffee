`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
moment = require "moment"
api = require "api"

TripsFilter = require "trips-filter"
TripsCategory = require "trips-category"
TripsTravellerFilter = require "trips-traveller-filter"
TravellersList = require "travellers-list"
Help = require "help"

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

  onFilterChinge: (filters) ->
    api.get "trip", filters, (data) =>
      @setState
        loaded: true
        trips: data.objects
        meta: data.meta

  renderTrips: ->
    @state.trips.map (trip) =>
      renderTags = @renderTags
      renderTripInfo = @renderTripInfo
      
      classes = ["trips-item"]

      advised = null
      if trip.advised or trip.id == 17
        classes.push "trips-item-advised"
        advised = `(
          <div className="trips-item-advised-title">
            рекомендуем  
          </div>
        )`

      return `(
        <div className={classes.join(" ")}>
          {advised}
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
            {this.getLocaleType(trip.price_type)} поездка <Help message="Например, «Яхтинг на Карибах».<p style='padding-top:6px'>Понятный заголовок поможет собрать группу.</p>"/>
          </div>
          <div className="trips-item-info-avia">
            <p>Перелет из <a href="#">Москвы</a></p>
            <p>от 21 000 руб.</p>
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

    styles =
      left: "0%"
      width: "#{(trip.people.length * 100) / trip.people_max_count}%"

    `(
      <div className="trip-item-info-travellers">
        <div className="trip-item-info-travellers-title">
          Компания
        </div>
        <div className="trip-item-info-travellers-slider">
          <div className="ui-slider ui-slider-horizontal ui-widget ui-widget-content ui-corner-all">
            <div className="ui-slider-range ui-widget-header ui-corner-all" style={styles}></div>
          </div>
          <Help message="Например, «Яхтинг на Карибах».<p style='padding-top:6px'>Понятный заголовок поможет собрать группу.</p>"/>
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
        <TripsFilter onChange={this.onFilterChinge}/>
        <TripsCategory/>
        <TripsTravellerFilter/>
        <div className="trips">
          {this.renderTrips()}
          {this.renderLoadNextButton()}
        </div>
      </div>
    )`

module.exports = Trips
