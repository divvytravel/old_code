`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
api = require "api"
uri = require "uri"

NonprofitDetail = require "nonprofit-detail"

TripDetail = React.createClass
  getDefaultProps: ->
    type: "nonprofit"

  getInitialState: ->
    trip: null

  componentWillMount: ->
    id = null
    fragments = (new uri(location.href)).anchor().split("&")
    for index, fragment of fragments
      c = fragment.split("=")
      id = c[1] if c[0] is "id"
    
    return unless id
    
    api.get "trip/#{id}", {}, (data) =>
      @setState trip: data

  render: ->
    return `(<div/>)` unless @state.trip

    if @props.type is "nonprofit"
      return `(<NonprofitDetail trip={this.state.trip}/>)`

module.exports = TripDetail
