`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
moment = require "moment"
api = require "api"
uri = require "uri"

Travellers = React.createClass
  getInitialState: ->
    loaded: false
    travellers: []
    meta: {}
    active: null

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

  createActiveHandler: (traveller) ->
    => @setState active: traveller.id

  renderTravellers: ->
    createActiveHandler = @createActiveHandler
    active = @state.active

    @state.travellers.map (traveller) ->
      return `(
        <div className={traveller.id === active ? "travellers-item travellers-item-active" : "travellers-item"} onClick={createActiveHandler(traveller)}>
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

  renderLoadNextButton: ->
    #next = @state.meta.total_count - (@state.meta.offset + @state.travellers.length)
    return `(
      <a onClick={this.load} className="button button--color-blue">
        Ещё 10 путешественников
      </a>
    )` if @state.meta.next

  render: ->
    `(
      <div className="travellers">
        <div>
          {this.renderTravellers()}
        </div>
        <div className="travellers-next">
          {this.renderLoadNextButton()}
        </div>
      </div>
    )`

module.exports = Travellers
