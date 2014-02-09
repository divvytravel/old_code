`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"

Input = React.createClass
  getDefaultProps: ->
    type: "text"
    message: null
    value: null
    picker: null
    disabled: false
    validation: null

  getInitialState: ->
    message: @props.message
    value: @props.value
    valid: null

  handleChange: (event) ->
    if @props.type is "email"
      state =
        value: event.target.value
        valid: @isEmailValid event.target.value
      
      state.message = @props.validMessage if state.valid
      state.message = @props.invalidMessage unless state.valid
      
      @setState state
    else if @props.maxLength
      state =
        value: event.target.value.substr 0, @props.maxLength

      state.message = "Осталось #{@props.maxLength - state.value.length} символов" if @props.maxLength - state.value.length <= 5
      state.message = "Не более #{@props.maxLength} символов" if state.value.length is parseInt @props.maxLength

      @setState state
    else
      @setState value: event.target.value

  isEmailValid: (email) ->
    check = /^[-a-z0-9~!$%^&*_=+}{\'?]+(\.[-a-z0-9~!$%^&*_=+}{\'?]+)*@([a-z0-9_][-a-z0-9_]*(\.[-a-z0-9_]+)*\.(aero|arpa|biz|com|coop|edu|gov|info|int|mil|museum|name|net|org|pro|travel|mobi|[a-z][a-z])|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,5})?$/i
    check.test email

  renderInput: ->
    @transferPropsTo(
      `(<input 
        className="input-element"
        value={this.state.value}
        onChange={this.handleChange}/>)`
    )

  render: ->
    className = ["input"]
    className.push "input-disabled" if @props.disabled
    className.push "input-fadeout" if @props.fadeout
    className.push "input-limit" if @state.value and @state.value.length is parseInt @props.maxLength

    if typeof(@state.valid) is "boolean"
      className.push "input-valid" if @state.valid
      className.push "input-invalid" unless @state.valid

    `(
      <span className={className.join(" ")}>
        {this.renderInput()}
        <span className="input-picker">{this.props.picker}</span>
        <span className="input-message">{this.state.message}</span>
      </span>
    )`

module.exports = Input
