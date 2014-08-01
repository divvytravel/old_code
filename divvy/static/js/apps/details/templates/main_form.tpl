
<div class="general-block main-block border-b">
  <div class="title">Главное</div>
  <div class="form-part-block">
    
    <div class="clearfix">
      <div class="general-form-left">
        <label>Название путешествия</label>
      </div>
      <div class="general-form-right">
        <div class="input-item clearfix">
          <input placeholder="" class="set-alert"/>
        </div>
      </div>
    </div>

    <div class="clearfix">
      <div class="general-form-left">
        <label>Даты</label>
      </div>
      <div class="general-form-right">
        <div class="input-item clearfix">
          <input id="startDate" type="text" class="input-date set-alert" placeholder="Начало">
        </div>
        <div class="input-item clearfix">
          <input id="endDate" type="text" class="input-date" placeholder="Окончание">
        </div>
        <div class="input-item clearfix">
          <input id="endRequestDate" type="text" class="input-date" placeholder="Принимать заявки до...">
        </div>
      </div>
    </div>

    <div class="clearfix">
      <div class="general-form-left">
        <label>Город</label>
      </div>
      <div class="general-form-right email-input">
        <div class="input-item clearfix">
          <input class="mini-input set-alert" placeholder="" />
        </div>
      </div>
    </div>

  </div>
</div>

<!-- +++ -->

<div class="general-block photo-block border-b">
  <div class="photo-part-block ">
    <div class="main-photo-part clearfix">
      <div class="title">Основная фотография</div>
      <a href="#" class="upload-link">Загрузите или перетащите сюда фотографию</a>
    </div>
    <div class="addition-photo-part clearfix">
      <div class="title">Дополнительные фото</div>
      <a href="#" class="upload-link">Загрузите или перетащите сюда другие фото</a>
    </div>
  </div>
</div>

<!-- +++ -->

<div class="general-block desc-block border-b">
  <div class="title">Описание</div>
  <div class="form-part-block">
    
    <div class="clearfix">
      <div class="general-form-full">
        <div class="textarea-item clearfix">
          <textarea name="description" class="set-alert" placeholder="Подробно расскажите о путешествии"></textarea>
        </div>
      </div>
    </div>

    <div class="subtitle">Ссылки</div>
    <div class="subtitle-desc">Не обязательно</div>

  </div>
</div>

<!-- +++ -->

<div class="general-block company-block border-b">
  <div class="title">Компания</div>
  <div class="form-part-block">
    
    <div class="clearfix">
      <div class="general-form-left">
        <label>Участников</label>
      </div>
      <div class="general-form-right">
        <div class="input-item clearfix">
          <input class="set-alert" placeholder="" />
        </div>
      </div>
    </div>

    <div class="clearfix">
      <div class="general-form-left">
        <label>Пожелания к компании</label>
        <span class="not-req">Не обязательно</span>
      </div>
      <div class="general-form-right email-input">
        <div class="textarea-item clearfix">
          <textarea name="text" class="set-alert" placeholder="Расскажите, кому понравится путешествие"></textarea>
        </div>
      </div>
    </div>

    <div class="clearfix">
      <div class="general-form-left">
        <label>Приватность</label>
      </div>
      <div class="general-form-right email-input">
        <div class="select-item clearfix">
          <select name="priv" id="selectPriv" style="opacity: 0;" class="set-alert" placeholder="Выберите из списка...">
            <option value="">Выберите из списка...</option>
            <option value="1">Я подтверждаю заявки на участие</option>
            <option value="2">Без подтверждения</option>
            <option value="3">Админ аппрувит заявки</option>
          </select>
        </div>
      </div>
    </div>

  </div>

</div>

<!-- +++ -->

<div class="general-block chipin-block border-b">
  <div class="title">Скидываемся на...</div>
  <div class="form-part-block">
    
    <div class="chipin-item">
      <div class="clearfix">
        <div class="general-form-left">
          <label>&nbsp;</label>
        </div>
        <div class="general-form-right">
          <!-- <div class="input-item clearfix">
            <input placeholder="" class="mini-input set-alert"/>
          </div> -->
          <div class="mini-select-item clearfix">
            <select name="priv" style="opacity: 0;" class="set-alert chipin-select" placeholder="Начните вводить...">
              <option value="">Начните вводить...</option>
              <option value="1">Питание</option>
              <option value="2">Аренда скутера</option>
              <option value="3">Аренда яхты</option>
              <option value="4">Ролики</option>
              <option value="5">Воздушный шар</option>
            </select>
          </div>
        </div>
      </div>
      
      <div class="clearfix">
        <div class="general-form-left">
          <label>Ссылка</label>
        </div>
        <div class="general-form-right">
          <div class="input-item clearfix">
            <input placeholder="" class="mini-input set-alert"/>
          </div>
        </div>
      </div>
      
      <div class="clearfix">
        <div class="general-form-left">
          <label>Стоимость</label>
        </div>
        <div class="general-form-right">
          <div class="input-item clearfix">
            <input placeholder="" class="mini-input input-price set-alert"/>
          </div>
        </div>
      </div>

      <div class="clearfix">
        <div class="general-form-left">
          <label>Краткое описание</label>
          <span class="not-req">Не обязательно</span>
        </div>
        <div class="general-form-right email-input">
          <div class="textarea-item clearfix">
            <textarea name="text" class="set-alert" placeholder=""></textarea>
          </div>
        </div>
      </div>
    </div>

  </div>

</div>

<!-- +++ -->

<div class="general-block addition-block border-b">
  <div class="title">Дополнительные расходы</div>
  <div class="form-part-block">
    
    <div class="clearfix">
      <div class="general-form-full">
        <div class="textarea-item clearfix">
          <textarea name="text" class="set-alert" placeholder="Напишите, сколько брать с собой денег, например, на сувениры"></textarea>
        </div>
      </div>
    </div>

  </div>
</div>

<!-- +++ -->

<div class="general-block tags-block border-b">
  <div class="title">Теги</div>
  <div class="title-desc">Не более пяти тегов</div>
  <div class="form-part-block">
    
    <div class="clearfix">
      <div class="general-form-full">
        <div class="tags-item clearfix">
          <input type="text" id="tagsInput" class="set-alert" style="display: none;" placeholder="Выберите из списка...">
        </div>
      </div>
    </div>

  </div>
</div>

<!-- +++ -->

<div class="general-block submit-block clearfix">
  <div class="clearfix">
    <div class="left-button">
      <a class="button-general button-default" href="javascript:void(0)">
        <span>Предварительный просмотр</span>
      </a>
    </div>
    <div class="right-button">
      <a class="button-general button-green" href="javascript:void(0)">
        <span>Создать путешествие</span>
      </a>
    </div>
  </div>
  <div class="checkbox-block pull-right">
    <input type="checkbox" id="post_to_fb_checkox"/>
    <label for="post_to_fb_checkox">Запостить в Фейсбук</label>
  </div>
  
</div>

<!-- +++ -->


