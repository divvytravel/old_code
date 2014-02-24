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
    minValue: 0
    maxValue: 0
    unit: null

  getInitialState: ->
    values: []

  componentDidMount: ->
    @slider = $(this.refs.slider.getDOMNode()).slider
      range: true
      min: parseInt @props.min
      max: parseInt @props.max
      values: [@props.minValue, @props.maxValue]
      change: ( event, ui ) =>
        return unless @props.onChange
        @setState values: ui.values
        @props.onChange ui.values
    
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
