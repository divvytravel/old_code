
<div class="general-block main-block border-b">
  <div class="title">Главное</div>
  <div class="form-part-block">

    <!-- <pre class="log" rv-text-="out"></pre> -->
    
    <div class="clearfix">
      <div class="general-form-left">
        <label>Название путешествия</label>
      </div>
      <div class="general-form-right">
        <div class="input-item clearfix">
          <input placeholder="" class="set-alert" data-alert-id="title" rv-live-value="model:title"/>
        </div>
      </div>
    </div>

    <div class="clearfix">
      <div class="general-form-left">
        <label>Даты</label>
      </div>
      <div class="general-form-right">
        <div class="input-item clearfix">
          <input id="startDate" type="text" class="input-date set-alert" data-alert-id="start_date" placeholder="Начало" rv-value="model:start_date">
        </div>
        <div class="input-item clearfix">
          <input id="endDate" type="text" class="input-date" placeholder="Окончание" rv-value="model:end_date">
        </div>
        <div class="input-item clearfix">
          <input id="endRequestDate" type="text" class="input-date" placeholder="Принимать заявки до..." rv-value="model:end_people_date">
        </div>
      </div>
    </div>

    <div class="clearfix">
      <div class="general-form-left">
        <label>Город</label>
      </div>
      <div class="general-form-right email-input">
        <div class="input-item clearfix">
          <input class="mini-input set-alert" placeholder="" rv-value="model:city"/>
        </div>
      </div>
    </div>

  </div>
</div>

<!-- +++ -->

<script id="previewMainPhotoTpl" type="text/html">
  <div class="dz-preview dz-file-preview">
    <div class="dz-details">
      <img data-dz-thumbnail />
    </div>
    <div class="dz-progress"><span class="dz-upload" data-dz-uploadprogress></span></div>
    <div class="dz-error-message"><span data-dz-errormessage></span></div>
  </div>
</script>

<script id="previewAdditionPhotoTpl" type="text/html">
  <div class="dz-preview dz-file-preview">
    <div class="dz-details">
      <img data-dz-thumbnail />
    </div>
    <div class="dz-progress"><span class="dz-upload" data-dz-uploadprogress></span></div>
    <div class="dz-error-message"><span data-dz-errormessage></span></div>
  </div>
</script>

<div class="general-block photo-block border-b">
  <div class="photo-part-block ">
    <div class="main-photo-part clearfix">
      <div class="title">Основная фотография</div>
      <a href="javascript:void(0)" class="upload-link">Загрузите или перетащите сюда фотографию</a>

      <div class="progress progress-striped active total-progress" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" style="opacity: 0;">
        <div class="progress-bar progress-bar-success" style="width: 0%;" data-dz-uploadprogress=""></div>
      </div>

      <div class="preview-container"></div>
    </div>
    <div class="addition-photo-part clearfix">
      <div class="title">Дополнительные фото</div>
      <a href="javascript:void(0)" class="upload-link">Загрузите или перетащите сюда другие фото</a>

      <div class="progress progress-striped active total-progress" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" style="opacity: 0;">
        <div class="progress-bar progress-bar-success" style="width: 0%;" data-dz-uploadprogress=""></div>
      </div>

      <div class="preview-container"></div>
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
          <textarea name="description" class="set-alert" placeholder="Подробно расскажите о путешествии" rv-value="model:descr_main"></textarea>
        </div>
      </div>
    </div>

    <!-- <div class="subtitle">Ссылки</div>
    <div class="subtitle-desc">Не обязательно</div> -->

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
          <input class="set-alert" placeholder="" rv-value="model:people_max_count"/>
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
          <textarea name="text" class="set-alert" placeholder="Расскажите, кому понравится путешествие" rv-value="model:descr_company"></textarea>
        </div>
      </div>
    </div>

    <div class="clearfix">
      <div class="general-form-left">
        <label>Приватность</label>
      </div>
      <div class="general-form-right email-input">
        <div class="select-item clearfix">
          <select name="priv" data-alert-id="trip_type" id="selectPriv" style="opacity: 0;" class="set-alert" placeholder="Выберите из списка..." rv-value="model:trip_type">
            <option value="">Выберите из списка...</option>
            <option value="open">Открытое участие</option>
            <option value="invite">Участие после одобрения создателя поездки</option>
            <option value="closed">Участие после одобрения всех участников поездки</option>
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
    
    <div class="chipin-item" rv-each-item="model:chipinItems">
      <div class="clearfix">
        <div class="general-form-left">
          <label>&nbsp;</label>
        </div>
        <div class="general-form-right">
          <div class="mini-select-item clearfix">
            <select name="priv" style="opacity: 0;" class="set-alert chipin-select" placeholder="Начните вводить..."></select>
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

    <div class="chipin-add">
      <div class="clearfix">
        <div class="general-form-left">
          <label>Еще скидываемся на...</label>
        </div>
        <div class="general-form-right">
          <div class="input-item clearfix-">
            <input placeholder="Начните вводить..." class="mini-input action-add-chipin-item" rv-on-click-="model.addChipinItem"/>
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
          <textarea name="text" class="set-alert" placeholder="Напишите, сколько брать с собой денег, например, на сувениры" rv-value="model:descr_additional"></textarea>
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
    <!-- <div class="left-button">
      <a class="button-general button-default" href="javascript:void(0)">
        <span>Предварительный просмотр</span>
      </a>
    </div> -->
    <div class="right-button">
      <a class="button-general button-green action-create" href="javascript:void(0)">
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


