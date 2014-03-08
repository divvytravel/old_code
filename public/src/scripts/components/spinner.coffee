`/** @jsx React.DOM */`
# The above line HAS to be the first line in the file for JSX to know to process it.

React = require "React"

Spinner = React.createClass
  render: ->
    `(
      <span className="spinner">
        <svg version="1.1" xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" viewBox="0 0 512 512" enable-background="new 0 0 512 512">
          <path id="loading-11-icon" d="M286,80.969c0,16.568-13.432,30-30,30s-30-13.432-30-30s13.432-30,30-30S286,64.4,286,80.969zM256,401.031c-16.568,0-30,13.432-30,30s13.432,30,30,30s30-13.432,30-30S272.568,401.031,256,401.031z M369.496,119.418c-8.284,14.349-26.632,19.266-40.98,10.98c-14.349-8.283-19.266-26.632-10.981-40.98s26.633-19.265,40.981-10.98S377.78,105.069,369.496,119.418z M183.485,381.601c-14.349-8.284-32.697-3.368-40.981,10.98s-3.367,32.696,10.981,40.981c14.349,8.283,32.696,3.367,40.98-10.981S197.833,389.885,183.485,381.601z M422.581,194.466c-14.348,8.283-32.696,3.368-40.98-10.981c-8.284-14.348-3.369-32.696,10.98-40.981c14.348-8.283,32.697-3.367,40.98,10.982C441.847,167.833,436.931,186.181,422.581,194.466z M130.399,328.517c-8.285-14.35-26.633-19.266-40.982-10.982c-14.348,8.285-19.264,26.633-10.979,40.982c8.284,14.348,26.632,19.264,40.981,10.98C133.767,361.212,138.683,342.864,130.399,328.517z M431.031,286c-16.566,0-30-13.431-30-30c0-16.567,13.432-30.001,30.001-30.001c16.567,0,30,13.433,29.999,30.002C461.032,272.568,447.602,286,431.031,286z M110.97,256.001c-0.001-16.57-13.433-30.001-30.001-30.002c-16.568,0.001-29.999,13.432-30,30.002c0.001,16.566,13.433,29.998,30.001,30C97.538,285.999,110.969,272.567,110.97,256.001z M392.581,369.496c-14.348-8.283-19.266-26.631-10.98-40.98c8.283-14.348,26.632-19.266,40.981-10.98c14.348,8.283,19.265,26.633,10.979,40.981C425.278,372.865,406.931,377.781,392.581,369.496z M130.398,183.486c8.285-14.352,3.368-32.698-10.98-40.983c-14.349-8.283-32.695-3.367-40.981,10.982c-8.282,14.348-3.366,32.696,10.981,40.981C103.768,202.75,122.115,197.832,130.398,183.486z M317.535,422.58c-8.284-14.347-3.369-32.696,10.98-40.98c14.348-8.284,32.697-3.368,40.981,10.981c8.284,14.348,3.367,32.697-10.982,40.98C344.167,441.847,325.819,436.931,317.535,422.58zM183.483,130.399c14.351-8.286,19.266-26.633,10.982-40.982c-8.285-14.348-26.631-19.264-40.982-10.98c-14.346,8.285-19.264,26.633-10.98,40.982C150.788,133.767,169.136,138.682,183.483,130.399z"></path>
        </svg>
      </span>
    )`

module.exports = Spinner