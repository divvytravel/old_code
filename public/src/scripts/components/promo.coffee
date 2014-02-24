`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
$ = require "jquery"

Promo = React.createClass
  createClickHandler: (target) ->
    targetNode = null
    (event) =>
      event.preventDefault()
      targetNode = $ "##{target}" unless targetNode
      highlight = @createHighlight $ event.target
      $(@refs.root.getDOMNode()).append highlight
      @animateTo highlight, targetNode

  createHighlight: (el) ->
    highlight = $ "<div>"
    highlight.css
      width: el.width()
      height: el.height()
      position: "absolute"
      background: "#2aa1bf"
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
    `(
      <span className="promo-content-description" ref="root">
        Вы можете 
        <a href="#" onClick={this.createClickHandler("promo-create-trip")}>организовать своё путешествие</a>
        и самостоятельно собрать 
        компанию, или к кому-нибудь присоединиться — 
        <a href="#" onClick={this.createClickHandler("promo-filters")}> выбирайте поездку, </a>
        и смотрите, куда собираются 
        <a href="#" onClick={this.createClickHandler("promo-travellers")}> интересные вам люди</a>.
      </span>
    )`

module.exports = Promo
