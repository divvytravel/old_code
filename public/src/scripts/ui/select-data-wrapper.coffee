`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
Select = require "select"

SelectDataWrapper = React.createClass
  getDefaultProps: ->
    multiple: false
    singleData: [{
      text: "Жильё",
      value: "estate"
    },{
      text: "Транспорт",
      value: "transport"
    },{
      text: "Экскурсию",
      value: "excursions"
    }]
    multipleData: [{
      text: "Москва",
      desc: "Россия, Москва",
      value: "moscow"
    },{
      text: "Мосул",
      desc: "Ирак",
      value: "mosul"
    }]

  componentWillMount: (domNode) ->
    if @props.multiple
      @setState options: @props.multipleData
    else
      @setState options: @props.singleData

  render: ->
    @transferPropsTo(
      `(
        <Select options={this.state.options}/>
      )`
    )

module.exports = SelectDataWrapper
