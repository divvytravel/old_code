`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"

CheckGroup = React.createClass
  getDefaultProps: ->
    options: []
    value: null

  getInitialState: ->
    value: @props.value

  createChangeHandler: (value) ->
    =>
      @setState value: value
      @props.onChange value if @props.onChange

  renderOptions: ->
    @props.options.map (option) =>
      classNames = ["button", "button--type-action"]
      classNames.push "active" if option.value is @state.value

      handler = @createChangeHandler option.value

      `(
        <a className={classNames.join(" ")} onClick={handler}>
          {option.text}
        </a>
      )`

  render: ->
    `(
      <div className="check-group">
        {this.renderOptions()}
      </div>
    )`

module.exports = CheckGroup