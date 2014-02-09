React = require "React"
$ = require "jquery"

camelize = (string, separator = "-") ->
  string.split(separator).map (piece, i) ->
    piece = piece.charAt(0).toUpperCase() + piece[1..] if i isnt 0
    piece
  .join ""

module.exports.init = ->
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

module.exports.isMSIE = ->
  match = /(msie) ([\w.]+)/i.exec navigator.userAgent
  return if match then parseInt(match[2], 10) else false
