`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"

Trips = require "trips"
Travellers = require "travellers"

MainPage = React.createClass
  getInitialState: ->
    travellers: null
    active: null

  handleTravellersChange: (travellers) ->
    @setState travellers: travellers

  activeChangeHandler: (active) ->
    @setState active: active

  render: ->
    `(
      <div className="container">
        <div id="promo-travellers" className="sidebar">
          <div className="title">
            Посмотрите, <br/>
            куда собираются другие, <br/>
            и путешествуйте вместе
          </div>
          <Travellers travellers={this.state.travellers} onActiveChange={this.activeChangeHandler}/>
        </div>
        <div className="content">
          <Trips onTravellersChange={this.handleTravellersChange} active={this.state.active}/>
        </div>
      </div>
    )`

module.exports = MainPage
