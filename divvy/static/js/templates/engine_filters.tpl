<div class="main">
  <div class="title">
    Путешествие
  </div>
  <div class="filter-container">
    <div class="column">
      <div class="date-picker-proj">
        <input id="fDate" type="text" class="input-proj" placeholder="Когда">
      </div>

      <div class="filter-or-separator">или...</div>

      <div class="select-place-proj">
        <input id="fPlaceTo" class="typeahead input-proj" type="text" placeholder="Куда?">
      </div>

    </div>
    <div class="column">
      <div class="slider-price">
        <div class="slider-label">СТОИМОСТЬ</div>
        
        <!-- <input type="text" id="amount" style="border:0; color:#f6931f; font-weight:bold;"> -->
         
        <div id="fPrice"></div>
        <div class="slider-limits">
          <span><%= price.min %> $</span>
          <span><%= price.max %> $</span>
          <% showPrice() %>
        </div>
      </div>
    </div>
    <div class="column">
      <div class="slider-label">ГРУППА</div>

      <div class="check-group">
        <span class="item">
          <a class="button button-toggle">
            <span class="num-string">3–10</span> человек
          </a>
        </span>
        <span class="item">
          <a class="button button-toggle">
            <span class="num-string">10-30</span> человек
          </a>
        </span>
        <span class="item">
          <a class="button button-toggle">
            <span class="num-string">>&nbsp;30</span> человек
          </a>
        </span>
      </div>

    </div>
  </div>
</div>



<div class="tags">
  
</div>



<div class="companions">
  <div class="title">
    Компания и попутчики
  </div>
  <div class="filter-container">
    <div class="column">
      <div class="select-place-proj">
        <input id="fPlaceFrom" class="typeahead input-proj" type="text" placeholder="Откуда?">
      </div>
    </div>
    <div class="column">
      <div class="slider-label">ВОЗРАСТ</div>
      <div id="fAge"></div>
      <div class="slider-limits">
        <span><%= age.min %></span>
        <span><%= age.max %></span>
      </div>
    </div>
    <div class="column">
      <div class="slider-gender">
        <div class="slider-label">ПОЛ</div>
        <div id="fGender"></div>
        <div class="slider-limits">
          <span>В основном<br> мужчины</span>
          <span>В основном<br> женщины</span>
        </div>
      </div>
    </div>
  </div>
</div>
