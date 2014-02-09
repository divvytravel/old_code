`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
utils = require "utils"
config = require "config"
api = require "api"
$ = require "jquery"

FacebookLogin = React.createClass
  getDefaultProps: ->
    typeWhite: false

  getInitialState: ->
    status: null
    key: null

  componentWillMount: ->
    $.ajaxSetup cache: true
    $.getScript "//connect.facebook.net/en_UK/all.js", =>
      FB.init appId: config.FB_APP_ID, status: false
      FB.Event.subscribe "auth.authResponseChange", @register

  login: ->
    FB.getLoginStatus (response) =>
      FB.login() if response.status is "not_authorized"

  register: (response) ->
    data = JSON.stringify
      access_token: response.authResponse.accessToken
      provider: "facebook"
    api.post "registration", data, (response) =>
      @setState key: response.oauth_consumer_key

  render: ->
    `(
      <a className={this.props.typeWhite ? "facebook-button facebook-button-white": "facebook-button"} onClick={this.login}>
        <span className="facebook-button-logo"></span>
        <span>Войти</span>
      </a>
    )`

module.exports = FacebookLogin
