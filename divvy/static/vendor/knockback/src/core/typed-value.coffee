{_, ko} = kb = require './kb'

# @nodoc
module.exports = class TypedValue
  constructor: (@create_options) ->
    @_vo = ko.observable(null) # create a value observable for the first dependency

  destroy: ->
    @__kb_released = true
    kb.release(@__kb_value); @__kb_value = null

  value: -> ko.utils.unwrapObservable(@_vo())
  rawValue: -> return @__kb_value

  valueType: (model, key) ->
    new_value = kb.getValue(model, key)
    @value_type or @_updateValueObservable(new_value) # create so we can check the type
    return @value_type

  update: (new_value) ->
    return if @__kb_released # destroyed, nothing to do

    # determine the new type
    (new_value isnt undefined) or (new_value = null) # ensure null instead of undefined
    new_type = kb.utils.valueType(new_value)

    # SHARED NULL MODEL - update reference
    if not @__kb_value or (@__kb_value.__kb_released or (@__kb_value.__kb_null and new_value))
      @__kb_value = undefined
      @value_type = undefined
    value = @__kb_value

    switch @value_type
      when kb.TYPE_COLLECTION
        return value(new_value) if @value_type is kb.TYPE_COLLECTION and new_type is kb.TYPE_ARRAY
        if new_type is kb.TYPE_COLLECTION or _.isNull(new_value)
          if _.isFunction(value.collection)
            value.collection(new_value) if kb.peek(value.collection) isnt new_value
            return

      when kb.TYPE_MODEL
        if new_type is kb.TYPE_MODEL or _.isNull(new_value)
          if _.isFunction(value.model)
            value.model(new_value) if kb.peek(value.model) isnt new_value
          else
            @_updateValueObservable(new_value) if kb.utils.wrappedObject(value) isnt new_value
          return

    if @value_type is new_type and not _.isUndefined(@value_type)
      value(new_value) if kb.peek(value) isnt new_value
    else
      @_updateValueObservable(new_value) if kb.peek(value) isnt new_value

  _updateValueObservable: (new_value) ->
    create_options = @create_options
    creator = create_options.creator = kb.utils.inferCreator(new_value, create_options.factory, create_options.path)
    @value_type = kb.TYPE_UNKNOWN

    # release the previous value
    previous_value = @__kb_value; @__kb_value = undefined
    kb.release(previous_value) if previous_value # release previous

    # found a creator
    if creator
      # have the store, use it to create
      if create_options.store
        value = create_options.store.findOrCreate(new_value, create_options)

      # create manually
      else
        if creator.models_only
          value = new_value
          @value_type = kb.TYPE_SIMPLE
        else if creator.create
          value = creator.create(new_value, create_options)
        else
          value = new creator(new_value, create_options)

    # create and cache the type
    else
      if _.isArray(new_value)
        @value_type = kb.TYPE_ARRAY
        value = ko.observableArray(new_value)
      else
        @value_type = kb.TYPE_SIMPLE
        value = ko.observable(new_value)

    # determine the type
    if @value_type is kb.TYPE_UNKNOWN
      if not ko.isObservable(value) # a view model, recognize view_models as non-observable
        @value_type = kb.TYPE_MODEL
        if typeof(value.model) isnt 'function' # manually cache the model to check for changes later
          kb.utils.wrappedObject(value, new_value)
      else if value.__kb_is_co
        @value_type = kb.TYPE_COLLECTION
      else
        @value_type = kb.TYPE_SIMPLE

    # store the value
    @__kb_value = value
    @_vo(value)
