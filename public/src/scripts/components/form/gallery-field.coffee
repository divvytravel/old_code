`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
api = require "api"
require "fileupload"

GalleryField = React.createClass
  getInitialState: ->
    main: null
    additional: []

  componentDidMount: ->
    #$(@refs.main.getDOMNode()).fileupload
    #  add: @addToMain

    $(@refs.additional.getDOMNode()).fileupload
      add: @addToAdditional

  addToMain: (event, data) ->
    reader = new FileReader()
    reader.onload = (e) =>
      @setState main:
        file: data.files[0]
        src: e.target.result
    reader.readAsDataURL data.files[0]

  addToAdditional: (event, data) ->
    console.log event
    reader = new FileReader()
    reader.onload = (e) =>
      additional = @state.additional
      additional.push
        file: data.files[data.files.length - 1]
        src: e.target.result
      @setState additional: additional
    reader.readAsDataURL data.files[data.files.length - 1]

  renderMainPhoto: ->
    `(
      <img src={this.state.main.src}/>
    )`

  renderMainContent: ->
    `(
      <div className="gallery-field-main-content">
        <span>Основная фотография</span>
        <a href="#" className="link">Загрузите или перетащите сюда другие фото</a>
      </div>
    )`

  renderMain: ->
    `(
      <div className="gallery-field-main" ref="main">
        {this.state.main ? this.renderMainPhoto() : this.renderMainContent()}
      </div>
    )`

  renderAdditionalPhotos: ->
    @state.additional.map (photo) ->
      `(
        <img src={photo.src}/>
      )`

  renderAdditional: ->
    `(
      <div className="gallery-field-additional" ref="additional">
        <div className="gallery-field-additional-content">
          <span>Дополнительные фото</span>
          <a href="#" className="link">Загрузите или перетащите сюда другие фото</a>
        </div>
        <div className="gallery-field-additional-photos">
          {this.renderAdditionalPhotos()}
        </div>
      </div>
    )`

  render: ->
    @transferPropsTo(
      `(
        <div className="gallery-field">
          {this.renderMain()}
          {this.renderAdditional()}
        </div>
      )`
    )

module.exports = GalleryField
