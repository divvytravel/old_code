`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
api = require "api"

NonprofitDetail = require "nonprofit-detail"
Field = require "field"
FieldLabel = require "field-label"
Input = require "input"
DateInput = require "date-input"
GalleryField = require "gallery-field"
Textarea = require "textarea"
Select = require "select"
Checkbox = require "checkbox"

Nonprofit = React.createClass
  getInitialState: ->
    trip: {}
    preview: false

  showPreview: ->
    @setState preview: true

  createChangeHandler: (field) ->
    (event) =>
      trip = @state.trip
      trip[field] = event.target.value
      @setState trip: trip

  renderMainBlock: ->
    `(
      <div className="trip-block">
        <div className="trip-block-title">Главное</div>
        <Field>
          <FieldLabel>Название путешествия</FieldLabel>
          <Input className="input-element--size-big" onChange={this.createChangeHandler("title")}/>
        </Field>
        <Field>
          <FieldLabel>Даты</FieldLabel>
          <DateInput placeholder="Начало" className="date-input--size-big"  onChange={this.createChangeHandler("start_date")}/>
        </Field>
        <Field>
          <FieldLabel></FieldLabel>
          <DateInput placeholder="Окончание" className="date-input--size-big"  onChange={this.createChangeHandler("end_date")}/>
        </Field>
        <Field>
          <FieldLabel></FieldLabel>
          <DateInput placeholder="Принимать заявки до..." className="date-input--size-big"  onChange={this.createChangeHandler("end_people_date")}/>
        </Field>
        <Field>
          <FieldLabel>Маршрут</FieldLabel>
          <Input placeholder="Город"  onChange={this.createChangeHandler("country")}/>
        </Field>
        <Field>
          <FieldLabel></FieldLabel>
          <Input placeholder="Следующий город" onChange={this.createChangeHandler("city")}/>
        </Field>
      </div>
    )`

  renderGalleryBlock: ->
    `(
      <div className="trip-block">
        <GalleryField onAddMainImage={this.createChangeHandler("image")} onAddImage={this.createChangeHandler("images")}/>
      </div>
    )`

  renderDescriptionBlock: ->
    `(
      <div className="trip-block">
        <div className="trip-block-title">Описание</div>
        <Field>
          <Textarea
            className="textarea-element--size-full textarea-element--height-258"
            placeholder="Подробно расскажите о путешествии"
            onChange={this.createChangeHandler("descr_main")}
          />
        </Field>
      </div>
    )`

  renderCompanyBlock: ->
    `(
      <div className="trip-block">
        <div className="trip-block-title">Компания</div>
        <Field>
          <FieldLabel>Участников</FieldLabel>
          <Input onChange={this.createChangeHandler("people_max_count")}/>
        </Field>
        <Field>
          <FieldLabel className="field-label--align-top">
            Пожелания к компании
            <span className="field-label-info">Не обязательно</span>
          </FieldLabel>
          <Textarea
            className="textarea-element--size-big textarea-element--height-74"
            placeholder="Расскажите, кому понравится путешествие"
            onChange={this.createChangeHandler("descr_company")}
            />
        </Field>
        <Field>
          <FieldLabel>Приватность</FieldLabel>
          <Select className="selectize--size-big"/>
        </Field>
      </div>
    )`

  renderChipBlock: ->
    `(
      <div className="trip-block">
        <div className="trip-block-title">Скидываемся на...</div>
        <Field>
          <FieldLabel></FieldLabel>
          <Input placeholder="Начинайте вводить"/>
        </Field>
        <Field>
          <FieldLabel>Ссылка</FieldLabel>
          <Input/>
        </Field>
        <Field>
          <FieldLabel>Стоимость</FieldLabel>
          <Input picker="$"/>
        </Field>
        <Field>
          <FieldLabel className="field-label--align-top">
            Краткое описание
            <span className="field-label-info">Не обязательно</span>
          </FieldLabel>
          <Textarea className="textarea-element--size-big textarea-element--height-74"/>
        </Field>
      </div>
    )`

  renderAdditionalBlock: ->
    `(
      <div className="trip-block">
        <div className="trip-block-title">Дополнительные расходы</div>
        <Field>
          <Textarea
            className="textarea-element--size-full textarea-element--height-102"
            placeholder="Напишите, сколько брать с собой денег, например, на сувениры"
            onChange={this.createChangeHandler("descr_additional")}
            />
        </Field>
      </div>
    )`

  renderTagsBlock: ->
    `(
      <div className="trip-block">
        <div className="trip-block-title">Теги</div>
      </div>
    )`

  renderButtonsBlock: ->
    `(
      <div className="trip-block">
        <div className="trip-block-success">
          <a className="button button--color-white" onClick={this.showPreview}>
            Предварительный просмотр
          </a>
          <a className="button button--color-green">
            Создать путешествие
          </a>
          <Checkbox label="Запостить в Фейсбук"></Checkbox>
        </div>
      </div>
    )`

  render: ->
    return `(<NonprofitDetail trip={this.state.trip}/>)` if @state.preview

    `(
      <div className="container">
        <div className="content content--type-left">
          <div className="trip">
            <div className="trip-title">
              <div>Новое некоммерческое путешествие</div>
              <a href="#" className="link">Новое коммерческое путешествие</a>
            </div>
            {this.renderMainBlock()}
            {this.renderGalleryBlock()}
            {this.renderDescriptionBlock()}
            {this.renderCompanyBlock()}
            {this.renderChipBlock()}
            {this.renderAdditionalBlock()}
            {this.renderTagsBlock()}
            {this.renderButtonsBlock()}
          </div>
        </div>
      </div>
    )`

module.exports = Nonprofit
