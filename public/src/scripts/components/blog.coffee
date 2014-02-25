`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"
api = require "api"
require "moment"

Blog = React.createClass
  getInitialState: ->
    loaded: false
    posts: []
    meta: {}

  componentWillMount: ->
    api.get "post", limit: 3, order_by: "-created", (data) =>
      @setState
        loaded: true
        posts: data.objects
        meta: data.meta

  renderPosts: ->
    @state.posts.map (post) ->
      console.log post
      return `(
        <div className="blog-post">
          <div>
            <a className="blog-post-title" href="#">{post.title}</a>
          </div>
          <div className="blog-post-created">
            {moment(post.created).format("DD MMMM YYYY")}
          </div>
          <div className="blog-post-text">
            {post.text}
          </div>
        </div>
      )`

  render: ->
    return `(<div/>)` unless @state.loaded

    `(
      <div className="blog">
        <div className="blog-container">
          <div className="blog-title title">Блог</div>
          <div className="blog-posts">
            {this.renderPosts()}
          </div>
        </div>
      </div>
    )`

module.exports = Blog
