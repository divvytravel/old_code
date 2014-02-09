`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
$ = require "jquery"
moment = require "moment"

# Configuration 
moment.lang("ru")

camelize = (string, separator = "-") ->
  string.split(separator).map (piece, i) ->
    piece = piece.charAt(0).toUpperCase() + piece[1..] if i isnt 0
    piece
  .join ""

$ ->
  # wait while all document ready callbacks done
  setTimeout ->
    $("[data-component]").each ->
      props = {}

      for attribute in @attributes
        name = attribute.name
        value = attribute.value

        if name isnt "data-component" and name.match /^data-/
          name = camelize name.replace /^data-/, ""
          props[name] = value

      props.innerHTML = @innerHTML
      @innerHTML = ""

      componentName = @attributes["data-component"].value
      Component = require componentName

      if Component
        #logger.log "init", "component", componentName, props
        React.renderComponent Component(props), @
      #else
        #logger.warn "init", "unknown component", componentName, props
  , 0
