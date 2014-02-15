`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
$ = require "jquery"
require "iCheck"

RadioGroup = React.createClass
  getDefaultProps: ->
    label: null
    type: "normal"
    options: []
    value: null
    name: (new Date()).getTime()

  getInitialState: ->
    value: @props.value

  componentDidMount: (domNode) ->
    $(domNode).iCheck
      radioClass: "radio-group-input"

  renderOptions: ->
    value = @state.value
    name = @props.name

    @props.options.map (option) ->
      `(
        <div className="radio-group-item">
          <label>
            <input type="radio" name={name} checked={value == option.value}></input>
            <span className="radio-group-label">{option.text}</span>
          </label>
        </div>
      )`

  render: ->
    classes = ["radio-group"]
    classes.push "radio-group-thin" if @props.type is "thin"

    `(
      <div className={classes.join(" ")}>
        {this.renderOptions()}
      </div>
    )`

module.exports = RadioGroup
