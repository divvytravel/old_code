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

  componentDidMount: ->
    @slider = $(this.refs.slider.getDOMNode()).slider
      range: true
      min: parseInt @props.min
      max: parseInt @props.max
      values: [@props.minValue, @props.maxValue]
      slide: ( event, ui ) =>
        return unless @props.onChange
        @props.onChange event: target: values: ui.values
    
  render: ->
    `(
      <div className="slider-container">
        <div className="slider-label">{this.props.label}</div>
        <div ref="slider"></div>
        <div className="slider-limits">
          <span>{this.props.min}</span>
          <span>{this.props.max}</span>
        </div>
      </div>
    )`

module.exports = Slider
