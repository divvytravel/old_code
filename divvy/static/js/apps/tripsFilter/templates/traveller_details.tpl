<div class="details details-normal" style="top: <%= top %>px; left: <%= left %>px;">
  <div class="details-wrap">
    <div class="details-wrap-close">
      <img src="/static/img/x-small-blue.png">
    </div>
    <div class="details-icon">
      <a href="javascript:void(0)">
      <img src="<%= data.url %>">
      </a>
    </div>
    <div class="details-info">
      <a href="#"><%= data.name %></a>
      <span>
        <%= data.age %>, 
        <% if (data.city != null) { %>
          <%= data.city %>
        <% } %>
      </span>
      <% if (data.career != null) { %>
        <span><%= data.career %></span>
      <% } %>
    </div>
  </div>
</div>
