<div class="item clearfix">
  <div class="title">
    <a href="#"><%= title %></a>
    <!-- <span class="title-star"></span> -->
  </div>
  <div class="tour">
    <%= showPlaceName() %>
  </div>

  <div class="tags">
    <% _.each(tags, function(tag) { %>
      <a href="javascript:void(0)" class="tag" data-id="<%= tag.id %>"><%= tag.name %></a>
    <% }); %>
  </div>

  <div class="content">
    <div class="preview">
      <% if(recommended) { %>
        <div class="recommended"></div>
      <% } %>
      <img class="img-rounded" src="<%= image %>">
    </div>

    <div class="info">
      <div class="title">
        <span class="calendar-black"></span>
        <span><%= showDateRange() %></span>
      </div>
      <div class="detail">
        <div class="price"><%= price %> &euro;</div>
        <div class="type">
          <span><%= showTripType() %></span>
          <span class="help">
            <i class="help-icon help-tooltip">?</i>
          </span>
        </div>
        <div class="avia">
          <p>
            <span>Перелет из </span>
            <a href="#">Москвы</a>
          </p>
          <p>от 21 000 руб.</p>
        </div>
      </div>

      <div class="travellers">
        <div class="travellers-title">Компания</div>
        <div class="slider">
          <div class="ui-slider ui-slider-horizontal ui-widget ui-widget-content ui-corner-all">
            <div class="ui-slider-range ui-widget-header ui-corner-all sex-slider" style="left:0%;width:50%;"></div>
          </div>
          <span class="help">
            <i class="help-icon help-tooltip">?</i>
          </span>
        </div>
        <div class="ratio">
          <div>
            <span><%= showOccup() %></span>
          </div>
          <div>
            <span><%= showSexMajority() %></span>
          </div>
        </div>
        <div class="list">
          <div class="items">
            
              <% _.each(people, function(user) { %>

                <div class="item-icon traveller-item" data-url="<%= user.avatar_url %>" 
                  data-name="<%= user.first_name %> <%= user.last_name %>"
                  data-age="<% if (user.age != null) { %><%= user.age %><% } else { %><% } %>"
                  data-city="<% if (user.city != null) { %><%= user.city.name %><% } else { %><% } %>"
                  data-career="<% if (user.career != null) { %><%= user.career %><% } else { %><% } %>">
                  <a href="javascript:void(0)">
                    <img src="<%= user.avatar_url %>">
                  </a>
                </div>

              <% }); %>

          </div>

          <% if(people.length > 3) { %>
            <div class="next">
              <i class="arrow-down"></i>
            </div>
          <% } %>
          
        </div>
      </div>
    </div>

  </div>

</div>