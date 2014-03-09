`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"

Textarea = React.createClass
  handleChange: (event) ->
    @props.onChange event if @props.onChange

  render: ->
    `(
      <span className="textarea">
        {this.transferPropsTo(
          <textarea className="textarea-element" onChange={this.handleChange}/>
        )}
      </span>
    )`

module.exports = Textarea
