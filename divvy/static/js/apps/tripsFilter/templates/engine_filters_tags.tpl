<% _.each(tags, function(tag) { %>

  <a href="javascript:void(0)" class="tag tag-radio" data-id="<%= tag.id %>">
    <input class="hide" type="radio" name="tag_radio" value="<%= tag.id %>" />
    <%= tag.name %>
  </a>

<% }); %>
