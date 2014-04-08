<div class="item traveller-radio <%= showActive(id) %>" data-id="<%= id %>">

  <input class="hide" type="radio" name="traveller_radio" data-id="<%= id %>" value="<%= id %>" <%= showChecked(id) %> />

  <div class="userpic pull-left">
    <a href="javascript:void(0)"><img src="<%= avatar_url %>"></a>
  </div>
  <div class="info">
    <div class="info-wrap">
      <span class="info-wrap-align">
        <a href="javascript:void(0)"><%= first_name %> <%= last_name %></a>
        <span>

          <span>
          <%= age %>, 
          <% if (city != null) { %>
            <%= city.name %>
          <% } %>
          </span>
          
        </span>

        <% if (career != null) { %>
          <span><%= career %></span>
        <% } %>

      </span>
    </div>
  </div>
</div>
