`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
api = require "api"
$ = require "jquery"

TripsCategory = React.createClass
  getDefaultProps: ->
    checked: null

  getInitialState: ->
    showAll: false
    loaded: false
    checked: null
    tags: []
    meta: {}

  componentWillMount: ->
    api.get "tags", main_page: true, (data) =>
      @setState
        loaded: true
        tags: data.objects
        meta: data.meta

  componentDidUpdate: (props) ->
    if @props.checked isnt props.checked
      @setState checked: @props.checked

  showAllHandler: ->
    @setState showAll: not @state.showAll

  getTagIdByName: (name) ->
    for tag in @state.tags
      return tag.id if tag.name is name

  createCheckTagHandler: (tag) ->
    =>
      @setState checked: tag
      id = @getTagIdByName tag
      @props.onChange "tags": id if @props.onChange and id

  renderTag: (tag) ->
    classes = ["button--type-category"]
    classes.push "active" if @state.checked is tag.name

    `(
      <a className={classes.join(" ")} onClick={this.createCheckTagHandler(tag.name)}>{tag.name}</a>
    )`

  renderSubTag: (tag) ->
    classes = ["button--type-category", "button--type-subcategory"]
    classes.push "active" if @state.checked is tag.name

    `(
      <a className={classes.join(" ")} onClick={this.createCheckTagHandler(tag.name)}>{tag.name}</a>
    )`

  renderShowAllButton: ->
    return `(<span/>)` if @state.tags.length < 6

    classes = ["button--type-category", "button--type-open-category"]
    classes.push "opened" if @state.showAll

    `(
      <a className={classes.join(" ")} onClick={this.showAllHandler}>
        Все категории
      </a>)`

  renderTagsColumn: (column) ->
    `(
      <li>
        {column.map(this.renderSubTag)}
      </li>
    )`

  renderAllTags: ->
    return `(<div/>)` unless @state.showAll

    columns = [[], [], [], []]
    tags = @state.tags.slice 0, @state.tags.length

    while tags.length > 0
      for column in columns
        column.push tags.splice(0, 1)[0] if tags.length > 0

    `(
      <div className="trips-filter-category-all sub-category">
        <ul>
          {columns.map(this.renderTagsColumn)}
        </ul>
      </div>
    )`

  render: ->
    return `(<div/>)` unless @state.loaded

    `(
      <div className="trips-filter-category">
        <div>
          {this.state.tags.slice(0, 4).map(this.renderTag)}
          {this.renderShowAllButton()}
        </div>
        {this.renderAllTags()}
      </div>
    )`

module.exports = TripsCategory
