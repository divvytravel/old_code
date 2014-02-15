`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
$ = require "jquery"

Help = React.createClass
  getInitialState: ->
    showTooltip: false

  getDefaultProps: ->
    message: ""

  componentDidMount: ->
    #$(@refs.icon.getDOMNode()).tooltip
    #  tooltipClass: "help-tooltip"
    #  content: @props.message
    #  items: "i"

  handleHelpEnter: ->
    @setState showTooltip: true

  handleHelpLeave: ->
    @setState showTooltip: false

  render: ->
    tooltip
    if @state.showTooltip
      tooltip = `(
        <span className="help-tooltip" dangerouslySetInnerHTML={{__html: this.props.message}}/>
      )`;

    `(
      <span className="help">
        <i ref="icon" className="help-icon" onMouseEnter={this.handleHelpEnter} onMouseLeave={this.handleHelpLeave}>?</i>
        {tooltip}
      </span>
    )`

module.exports = Help
