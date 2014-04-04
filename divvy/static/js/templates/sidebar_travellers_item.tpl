<div class="item traveller-radio">

  <input class="hide" type="radio" name="traveller_radio" data-id="<%= id %>" value="<%= id %>" />

  <div class="userpic pull-left">
    <a href="javascript:void(0)"><img src="<%= avatar_url %>"></a>
  </div>
  <div class="info">
    <div class="info-wrap">
      <span class="info-wrap-align">
        <a href="javascript:void(0)"><%= first_name %> <%= last_name %></a>
        <span><%= age %>, 

          <% if (city != null) { %>
            <span><%= city %></span>
          <% } %>
          
        </span>

        <% if (career != null) { %>
          <span><%= career %></span>
        <% } %>

      </span>
    </div>
  </div>
</div>
