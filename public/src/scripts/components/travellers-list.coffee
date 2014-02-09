`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
$ = require "jquery"

TravellersList = React.createClass
  direction:
    DOWN: "down"
    UP: "up"

  getDefaultProps: ->
    iconSize: 61
    travellers: []

  getInitialState: ->
    position: 0
    maxLines: 0
    direction: false
    containerHeight: 0
    listHeight: 0

  componentDidMount: (domNode) ->
    list = $ @refs.list.getDOMNode()

    @setState
      direction: if @props.travellers.length > 3 then @direction.DOWN else false
      listHeight: list.height()
      containerHeight: list.parent().height()

  next: ->
    direction = @state.direction
    position = @state.position
    position -= @props.iconSize

    if (@state.listHeight + position) < @state.containerHeight
      position = @state.containerHeight - @state.listHeight
      direction = @direction.UP

    $(@refs.list.getDOMNode()).animate top: position

    @setState position: position, direction: direction

  prev: ->
    direction = @state.direction
    position = @state.position
    position += @props.iconSize

    if position > 0
      position = 0
      direction = @direction.DOWN

    $(@refs.list.getDOMNode()).animate top: position

    @setState position: position, direction: direction

  renderTravellers: ->
    @props.travellers.map (traveller) ->
      return `(
        <div className="travellers-list-item-icon">
          <a href={traveller.resource_uri}>
            <img src={traveller.avatar_url}/>
          </a>
        </div>
      )`

  renderNextButton: ->
    return unless @state.direction is @direction.DOWN
    `(
      <div className="travellers-list-next" onClick={this.next}>
        <i className="arrow-down"/>
      </div>
    )`

  renderPrevButton: ->
    return unless @state.direction is @direction.UP
    `(
      <div className="travellers-list-prev" onClick={this.prev}>
        <i className="arrow-up"/>
      </div>
    )`

  render: ->
    `(
      <div className="travellers-list">
        {this.renderPrevButton()}
        <div ref="list" className="travellers-list-items">
          {this.renderTravellers()}
        </div>
        {this.renderNextButton()}
      </div>
    )`

module.exports = TravellersList
