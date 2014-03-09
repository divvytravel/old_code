`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
moment = require "moment"
api = require "api"
uri = require "uri"

require "scrollTo"

TripsFilter = require "trips-filter"
TripsCategory = require "trips-category"
TripsTravellerFilter = require "trips-traveller-filter"
TravellersList = require "travellers-list"
Spinner = require "spinner"
Help = require "help"

Trips = React.createClass
  getDefaultProps: ->
    onTravellersChange: ->
    active: null

  getInitialState: ->
    loaded: false
    trips: []
    meta: {}
    tag: null

  componentWillMount: (domNode) ->
    api.get "trip", limit: 4, (data) =>
      @setState
        loaded: true
        trips: data.objects
        meta: data.meta

  componentDidUpdate: (props, state, domNode) ->
    if @state.trips and @state.trips isnt state.trips
      travellers = @extractTravellers()
      if @props.onTravellersChange
        @props.onTravellersChange travellers

    #if @props.active isnt props.active

  extractTravellers: ->
    ids = []
    travellers = []
    for trip in @state.trips
      for traveller in trip.people
        if ids.indexOf(traveller.id) is -1
          travellers.push traveller
          ids.push traveller.id
    travellers

  load: ->
    offset = new uri(@state.meta.next).getQueryParamValue('offset') 
    api.get "trip", limit: 5, offset: offset, (data) =>
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

  onFilterChange: (filters) ->
    @setState loaded: false
    api.get "trip", filters, (data) =>
      @setState
        loaded: true
        trips: data.objects
        meta: data.meta

  getTripByCount: (count) ->
    trips = ["путешествие", "путешествия", "путешествий"]
    cases = [2, 0, 1, 1, 1, 2]
    if count % 100 > 4 and count % 100 < 20
      return trips[2]
    else
      return trips[cases[if count % 10 < 5 then count % 10 else 5]]

  createTagClickHandler: (tag) ->
    (event) =>
      event.preventDefault()
      @setState tag: tag.name
      $.scrollTo $(@refs.tags.getDOMNode()), duration: 600
      setTimeout =>
        @onFilterChange tag: tag.id
      , 500

  renderTrips: ->
    @state.trips.map (trip) =>
      renderTags = @renderTags
      renderTripInfo = @renderTripInfo
      
      classes = ["trips-item"]

      advised = null
      if trip.recommended
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
            <a href="/static/trip/nonprofit/detail.html#id=#{trip.id}">{trip.title}</a>
            <span className="trips-item-title-star"></span>
          </div>
          <div className="trips-item-tour">
            {trip.country}<i> → </i>{trip.city}
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
    clickHandler = this.createTagClickHandler
    tags.map (tag) ->
      return `(
        <a href={"/" + tag.slug} className="tag" onClick={clickHandler(tag)}>{tag.name}</a>
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
    offset = new uri(@state.meta.next).getQueryParamValue('offset') 
    if @state.meta.total_count - offset < 5
      count = @state.meta.total_count - offset 
    else
      count = 5

    return `(
      <div className="trips-next">
        <a onClick={this.load} className="button button--color-blue">
          {["Показать еще", count, this.getTripByCount(count)].join(" ")}
        </a>
      </div>
    )` if @state.meta.next

  renderNotFound: ->
    `(
      <div className="trips-not-found">
        <span className="trips-not-found-icon"></span>
        <br/>
        <span>
          Ничего не найдено :-(
        </span>
      </div>
    )`

  renderTripsBlock: ->
    return `(<Spinner/>)` unless @state.loaded
    return this.renderNotFound() if @state.trips.length is 0

    `(
      <div className="trips">
        <div className="trips-count">
          {["Подходит", this.state.meta.total_count, this.getTripByCount(this.state.meta.total_count)].join(" ")}
        </div>
        {this.renderTrips()}
        {this.renderLoadNextButton()}
      </div>
    )`

  render: ->
    `(
      <div>
        <TripsFilter onChange={this.onFilterChange} maxPrice={this.state.meta.max_price} minPrice={this.state.meta.min_price}/>
        <TripsCategory onChange={this.onFilterChange} checked={this.state.tag} ref="tags"/>
        <TripsTravellerFilter/>
        {this.renderTripsBlock()}
      </div>
    )`

module.exports = Trips
