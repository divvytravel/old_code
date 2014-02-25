`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
$ = require "jquery"
require "placeholder"
require "selectize"

Select = React.createClass
  getDefaultProps: ->
    options: []
    multiple: true

  getInitialState: ->
    value: null

  componentDidMount: (domNode) ->
    params = maxItems: 1
    params.render = @renderOption() if @props.multiple

    $selectize = $(domNode).selectize params
    
    selectize = $selectize[0].selectize
    selectize.addOption @props.options if @props.options
    selectize.refreshOptions false
    
    $selectize.on "change", (event) =>
      @setState value: event.target.value
      @props.onChange event.target.value if @props.onChange

    $selectize.find("input").placeholder()

  componentDidUpdate: (props, state, domNode) ->
    selectize = $(domNode)[0].selectize

    unless @props.options and @props.options.length is props.options.length
      selectize.clearOptions()
      if @props.options
        selectize.addOption @props.options
      selectize.refreshOptions false

  renderOption: ->
    option: (item, escape) ->
      return [
        '<div class="option option-multi">'
        '<div>'
        escape(item.text)
        '</div>'
        '<p>'
        escape(item.desc)
        '</p>'
        '</div>'
      ].join ""

  render: ->
    @transferPropsTo(
      `(
        <select/>
      )`,
      @props.children
    )

module.exports = Select
