`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
$ = require "jquery"

Highlight = React.createClass
  getDefaultProps: ->
    target: null
    color: "#2aa1bf"

  clickHandler: ->
      event.preventDefault()
      targetNode = $ "##{@props.target}" unless targetNode
      highlight = @createHighlight $ event.target
      $(@getDOMNode()).parent().append highlight
      @animateTo highlight, targetNode

  createHighlight: (el) ->
    highlight = $ "<div>"
    highlight.css
      width: el.width()
      height: el.height()
      position: "absolute"
      background: @props.color
      "z-index": 999999
      opacity: 0.6
      top: el.offset().top
      left: el.offset().left

  animateTo: (highlight, target) ->
    highlight.animate
      left: target.offset().left
      top: target.offset().top
      width: target.outerWidth()
      height: target.outerHeight()
    , "slow", ->
        highlight.animate
          opacity: 0
        , 1000, ->
          highlight.remove()

  render: ->
    @transferPropsTo(
      `(
        <a href="#" onClick={this.clickHandler}>
          {this.props.children}
        </a>
      )`
    )

module.exports = Highlight
