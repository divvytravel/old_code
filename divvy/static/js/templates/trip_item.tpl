<div class="item clearfix">
  <div class="title">
    <a href="#"><%= title %></a>
    <span class="title-star"></span>
  </div>
  <div class="tour">
    <span>Россия</span>
    <i> → </i>
    <span>Москва</span>
  </div>

  <div class="tags">
    <% _.each(tags, function(tag) { %>
      <a href="#" class="tag"><%= tag.name %></a>
    <% }); %>
  </div>

  <div class="content">
    <div class="preview">
      <img class="img-rounded" src="<%= image %>">
    </div>

    <div class="info">
      <div class="title">
        <span class="calendar-black"></span>
        <span>08 – 16 февраля</span>
      </div>
      <div class="detail">
        <div class="price"><%= price %> евро</div>
        <div class="type">
          <span>Некоммерческая</span>
          <span> поездка </span>
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
            <div class="ui-slider-range ui-widget-header ui-corner-all" style="left:0%;width:50%;"></div>
          </div>
          <span class="help">
            <i class="help-icon help-tooltip">?</i>
          </span>
        </div>
        <div class="ratio">
          <div>
            <span>Набрано <%= people_count %> из <%= people_max_count %> человек </span>
          </div>
          <div>
            <span>Преимущественно девушки</span>
          </div>
        </div>
        <div class="list">
          <div class="items">
            
              <% _.each(people, function(user) { %>

                <div class="item-icon traveller-item" data-url="<%= user.avatar_url %>" data-name="<%= user.first_name %> <%= user.last_name %>">
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