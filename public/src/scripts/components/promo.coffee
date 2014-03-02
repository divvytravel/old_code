`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
$ = require "jquery"

Highlight = require "highlight"

Promo = React.createClass
  render: ->
    `(
      <span className="promo-content-description">
        Вы можете 
        <Highlight target="promo-create-trip">организовать своё путешествие</Highlight>
        и самостоятельно собрать 
        компанию, или к кому-нибудь присоединиться — 
        <Highlight target="promo-filters"> выбирайте поездку, </Highlight>
        и смотрите, куда собираются 
        <Highlight target="promo-travellers"> интересные вам люди</Highlight>.
      </span>
    )`

module.exports = Promo
