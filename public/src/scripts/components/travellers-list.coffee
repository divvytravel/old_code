`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
$ = require "jquery"
require "moment"

TravellersList = React.createClass
  getDefaultProps: ->
    iconSize: 61
    travellers: []

  getInitialState: ->
    size: if @props.travellers.length > 8 then "small" else "normal"
    expanded: false
    traveller: null
    offset: null

  componentDidMount: (domNode) ->
    @setState offset: $(domNode).offset()

  createClickHandler: (traveller) ->
    (event) =>
      offset = $(event.target).offset()
      event.preventDefault()
      @setState
        traveller:
          avatar_url: traveller.avatar_url
          firstName: traveller.first_name
          lastName: traveller.last_name
          birthday: moment(moment()).diff(traveller.birthday, "years")
          city: "Стамбул"
          activity: "Предприниматель"
          top: offset.top
          left: offset.left

      $("body").on "click", @closeOnBody

  closeOnBody: (event) ->
    details = $ @refs.details.getDOMNode()
    target = $ event.target
    
    return if details.has(target).length > 0
    return if details[0] is target[0]

    @closeDetails()

  closeDetails: ->
    $("body").off "click", @closeOnBody
    @setState traveller: null

  expand: (expanded) ->
    => @setState expanded: expanded, traveller: null

  renderExpandButton: ->
    return `(<div/>)` if @props.travellers.length < 4

    if @state.expanded
      `(
        <div className="travellers-list-prev" onClick={this.expand(false)}>
          <i className="arrow-up"/>
        </div>
      )`
    else
      `(
        <div className="travellers-list-next" onClick={this.expand(true)}>
          <i className="arrow-down"/>
        </div>
      )`

  renderTravellers: ->
    clickHandler = @createClickHandler
    
    classes = """
      travellers-list-item-icon
      travellers-list-item-#{@state.size}-icon
    """
  
    @props.travellers.map (traveller) ->
      return `(
        <div className={classes}>
          <a href={traveller.resource_uri} onClick={clickHandler(traveller)}>
            <img src={traveller.avatar_url}/>
          </a>
        </div>
      )`

  renderTravellerDetails: ->
    return unless @state.traveller
    traveller = @state.traveller

    styles =
      top: traveller.top - @state.offset.top - 9
      left: traveller.left - @state.offset.left - 9

    classes = """
      travellers-list-item-details
      travellers-list-item-details-#{@state.size}
    """

    `(
      <div className={classes} style={styles} ref="details">
        <div className="travellers-list-item-details-wrap">
          <div className="travellers-list-item-details-wrap-close" onClick={this.closeDetails}>
            <img src="/static/img/x-small-blue.png"/>
          </div>
          <div className="travellers-list-item-details-icon">
            <a href="#">
              <img src={this.state.traveller.avatar_url}/>
            </a>
          </div>
          <div className="travellers-list-item-details-info">
            <a href="#">{traveller.firstName}</a>
            <a href="#">{traveller.lastName}</a>
            <span>{[traveller.birthday, traveller.city].join(", ")}</span>
            <span>{traveller.activity}</span>
          </div>
        </div>
      </div>
    )`

  render: ->
    classes = ["travellers-list-items"]
    classes.push "travellers-list-items-expanded" if @state.expanded
  
    `(
      <div className="travellers-list">
        <div ref="list" className={classes.join(" ")}>
          {this.renderTravellers()}
        </div>
        {this.renderExpandButton()}
        {this.renderTravellerDetails()}
      </div>
    )`

module.exports = TravellersList
