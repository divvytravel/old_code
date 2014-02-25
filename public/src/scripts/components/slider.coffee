`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
$ = require "jquery"
require "jquery.ui.slider"

Slider = React.createClass
  getDefaultProps: ->
    label: ""
    min: 0
    max: 100
    unit: null
    values: []
    value: null
    int: true

  getInitialState: ->
    values: @props.values
    value: @props.value

  componentDidMount: ->
    options =
      range: if @state.value then false else true
      change: ( event, ui ) =>
        return unless @props.onChange
        @setState values: ui.values
        @props.onChange ui.values

    options.value = @state.value if @state.value
    options.values = @state.values if @state.values.length > 0
    options.min = parseInt @props.min if @props.int
    options.max = parseInt @props.max if @props.int

    @slider = $(this.refs.slider.getDOMNode()).slider options
    
  render: ->
    `(
      <div className="slider-container">
        <div className="slider-label">{this.props.label}</div>
        <div ref="slider"></div>
        <div className="slider-limits">
          <span>{[this.props.min, this.props.unit].join(' ')}</span>
          <span>{[this.props.max, this.props.unit].join(' ')}</span>
        </div>
      </div>
    )`

module.exports = Slider
