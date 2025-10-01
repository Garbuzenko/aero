
<form method="post" action="" id="form_jsShowMapFilters" class="mb-3">
<div class="row">
<div class="col-md-3 form-group mb-2">
  <label for="">Любой период:</label>
  <input class="myDateInput form-control flatpickr flatpickr-input active" name="dates" id="dates" type="text" value="" placeholder="Выберите диапазон дат..." />
</div>

<div class="col-md-2 form-group mb-2">
  <label for="year-select">Год:</label>
  <select id="year-select" name="year" class="form-select">
    <?foreach($filtersArr as $year=>$val):?>
    <option value="<?=$year;?>"<?if($year==$thisYear):?> selected=""<?endif;?>><?=$year;?></option>
    <?endforeach?>
  </select>      
</div>
<div class="col-md-2 form-group mb-2">
  <label for="month-select">Месяц:</label>
  <select id="month-select" name="month" class="form-select">
    <option value="">Выбрать</option>
    <?foreach($filtersArr[$thisYear]['months'] as $k=>$v):?>
    <option value="<?=$k;?>"><?=$v;?></option>
    <?endforeach?>
  </select>
</div>

<div class="col-md-2 form-group mb-2">
  <label for="quarter-select">Квартал:</label>
  <select id="quarter-select" name="quarter" class="form-select">
    <option value="">Выбрать</option>
    <?foreach($filtersArr[$thisYear]['quarters'] as $k=>$v):?>
    <option value="<?=$k;?>"><?=$v;?></option>
    <?endforeach?>
  </select>    
</div>

<div class="col-md-3 form-group mb-2">
  <label for="">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label>
  <button type="button" class="send_form btn btn-primary btn-lg w-100" id="jsShowMapFilters">Показать</button>
</div>

</div>

<input type="hidden" name="module" value="main" />
<input type="hidden" name="component" value="map" />
<input type="hidden" name="ajaxLoad" value="jsAjaxLoadMap" />
<input type="hidden" name="opaco" value="1" />
<input type="hidden" name="initAnyPlugin" value="initializeDataTable" />
<input type="hidden" name="alert" value="" />
</form>

<form method="post" action="" id="form_jsShowRegionData" class="hidden">
  <input type="hidden" name="module" value="main" />
  <input type="hidden" name="component" value="map" />
  <input type="hidden" name="region_id" id="jsMapRegionId" value="" />
  <input type="hidden" name="start_date" id="jsMapStartDate" value="" />
  <input type="hidden" name="end_date" id="jsMapEndDate" value="" />
  <input type="hidden" name="opaco" value="1" />
  <input type="hidden" name="alert" value="" />
  <button id="jsShowRegionData" class="send_form"></button>
</form>

<div id="jsAjaxLoadMap">
<?include $_SERVER['DOCUMENT_ROOT'].'/modules/main/components/map/includes/map.inc.php';?>
</div>