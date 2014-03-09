`/** @jsx React.DOM */`

React = require "React"
api = require "api"

NonprofitDetail = React.createClass
  getDefaultProps: ->
    trip: {}

  getInitialState: ->
    trip: {}

  getTripPeriod: (trip) ->
    start = moment(trip.start_date, "YYYY-MM-DD")
    end = moment(trip.end_date, "YYYY-MM-DD")

    if start.month() is end.month()
      period = "#{start.format("DD")} – #{end.format("DD MMMM")}"
    else
      period = "#{start.format("DD MMMM")} – #{end.format("DD MMMM")}"

    period

  renderTags: (tags) ->
    tags.map (tag) ->
      `(
        <a href="#" className="tag">{tag.name}</a>
      )`

  renderGallery: (trip) ->
    `(
      <div className="trip-detail-gallery">
        <div className="trip-detail-gallery-main">
          <img src={trip.image}/>
        </div>
        <div className="trip-detail-gallery-additional">
          {trip.images.map(function (image) {
            return (<img src={image}/>)
          })}
        </div>
      </div>
    )`

  render: ->
    trip = @props.trip or @state.trip
    console.log trip
    `(
      <div className="container">
        <div className="content content--type-left">
          <div className="trip-detail">
            <div className="trip-detail-title">
              <span>{trip.title}</span>
            </div>
            <div className="trip-detail-tour">
              {trip.country}<i> → </i>{trip.city}
            </div>
            <div className="trip-detail-tags">
              {this.renderTags(trip.tags)}
            </div>
            {this.renderGallery(trip)}
            <div className="trip-detail-description">
              {trip.descr_main}
            </div>
          </div>
        </div>
        <div className="sidebar sidebar--type-right">
          <div className="trip-detail-sidebar">
            <div className="trip-detail-sidebar-block">
              <div className="trip-detail-sidebar-period">
                <span className="calendar-black"></span>
                <span>{this.getTripPeriod(trip)}</span>      
              </div>
              <div className="trip-detail-sidebar-date">
                Заявки принимаются до {moment(trip.end_people_date, "YYYY-MM-DD").format("DD MMMM")}
              </div>
            </div>
          </div>
        </div>
      </div>
    )`

module.exports = NonprofitDetail
