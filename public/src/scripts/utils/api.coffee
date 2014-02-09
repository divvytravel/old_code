apiUrl = "/api/v1"
$ = require "jquery"

module.exports.get = (type, params, callback) ->
  xhr = $.get "#{apiUrl}/#{type}?format=json", params
  xhr.success (data) -> callback data
  xhr.error -> console.log "Ошибка получения данных с сервера"

module.exports.post = (type, data, callback) ->
  $.ajax
    type: "POST"
    url: "#{apiUrl}/#{type}/"
    data: data
    dataType: "json"
    contentType: "application/json"
    success: callback