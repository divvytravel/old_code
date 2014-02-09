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

  renderTravellers: ->
    @state.travellers.map (traveller) ->
      return `(
        <div className="travellers-item">
          <div className="travellers-item-icon">
            <a href={traveller.resource_uri}>
              <img src={traveller.avatar_url}/>
            </a>
          </div>
          <div className="travellers-item-info">
            <div className="travellers-item-info-wrap">
              <span className="travellers-item-info-wrap-align">
                <a href={traveller.resource_uri}>{[traveller.first_name, traveller.last_name].join(" ")}</a>
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
      <div>
        <div className="travellers">
          {this.renderTravellers()}
        </div>
        {this.renderLoadNextButton()}
      </div>
    )`

module.exports = Travellers
