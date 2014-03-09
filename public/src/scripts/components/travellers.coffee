`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
moment = require "moment"
api = require "api"
uri = require "uri"

TravellersNextButton = React.createClass
  getDefaultProps: ->
    count: null

  handleGetNext: ->
    @props.onClick() if @props.onClick
    
  render: ->
    `(
      <div className="travellers-next">
        <a onClick={this.handleGetNext} className="button button--color-blue">
            Ещё {this.props.count} путешественников
        </a>
      </div>
    )`

TravellersList = React.createClass
  getDefaultProps: ->
    travellers: []

  getInitialState: ->
    active: null

  createActiveHandler: (traveller) ->
    =>
      @setState active: traveller.id
      @props.onActiveChange traveller.id if @props.onActiveChange

  renderTravellers: ->
    createActiveHandler = @createActiveHandler
    active = @state.active

    @props.travellers.map (traveller) ->
      return `(
        <div
          className={traveller.id === active ? "travellers-item travellers-item-active" : "travellers-item"}
          onClick={createActiveHandler(traveller)}>
          <div className="travellers-item-icon">
            <a href="javascript:void(0)">
              <img src={traveller.avatar_url}/>
            </a>
          </div>
          <div className="travellers-item-info">
            <div className="travellers-item-info-wrap">
              <span className="travellers-item-info-wrap-align">
                <a href="javascript:void(0)">{[traveller.first_name, traveller.last_name].join(" ")}</a>
                <span>{traveller.birthday && (moment(moment()).diff(traveller.birthday, "years") + ", Стамбул")}</span>
                <span>Предприниматель</span>
              </span>
            </div>
          </div>
        </div>
      )`

  render: ->
    `(
      <div>
        {this.renderTravellers()}
      </div>
    )`

RemoteTravellers = React.createClass
  getDefaultProps: ->
    onActiveChange: ->

  getInitialState: ->
    travellers: []
    meta: {}

  componentWillMount: (domNode) ->
    api.get "user", limit: 6, (data) =>
      @setState
        loaded: true
        travellers: data.objects
        meta: data.meta

  load: ->
    offset = new uri(@state.meta.next).getQueryParamValue('offset')
    api.get "user", limit: 10, offset: offset, (data) =>
      @setState
        travellers: @state.travellers.concat data.objects
        meta: data.meta

  renderNextButton: ->
    if @state.meta.next
      offset = new uri(@state.meta.next).getQueryParamValue('offset') 
      if @state.meta.total_count - offset < 10
        count = @state.meta.total_count - offset 
      else
        count = 10
      `(<TravellersNextButton onClick={this.load} count={count}/>)` 

  render: ->
    `(
      <div>
        <TravellersList travellers={this.state.travellers}  onActiveChange={this.props.onActiveChange}/>
        {this.renderNextButton()}
      </div>
    )`

LocalTravellers = React.createClass
  getDefaultProps: ->
    onActiveChange: ->
    travellers: []

  getInitialState: ->
    travellers: []

  componentWillMount: ->
    @setState
      travellers: @props.travellers.slice 0, 6

  componentDidUpdate: (props, state, domNode) ->
    if @props.travellers isnt props.travellers
      @setState
        travellers: @props.travellers.slice 0, 6

  next: ->
    count = @state.travellers.length
    @setState
      travellers: @props.travellers.slice count, cont + 10 

  renderNextButton: ->
    return if @props.travellers.length is @state.travellers.length
    offset = @props.travellers.length - @state.travellers.length
    `(<TravellersNextButton onClick={this.next} count={offset < 10 ? offset : 10}/>)` 

  render: ->
    `(
      <div>
        <TravellersList travellers={this.state.travellers} onActiveChange={this.props.onActiveChange}/>
        {this.renderNextButton()}
      </div>
    )`

Travellers = React.createClass
  getDefaultProps: ->
    travellers: null

  getInitialState: ->
    loaded: false
    travellers: []
    active: null

  activeChangeHandler: (active) ->
    @props.onActiveChange active if @props.onActiveChange

  renderTravellers: ->
    return unless @props.travellers

    if @props.travellers.length is 0
      `(<RemoteTravellers onActiveChange={this.activeChangeHandler}/>)`
    else
      `(<LocalTravellers travellers={this.props.travellers} onActiveChange={this.activeChangeHandler}/>)`

  render: ->
    `(
      <div className="travellers">
        {this.renderTravellers()}
      </div>
    )`

module.exports = Travellers
