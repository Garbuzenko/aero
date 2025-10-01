<?php defined('DOMAIN') or exit(header('Location: /'));?>
<div class="row layout-top-spacing">

<?if($regList!=false):?>
<div class="mb-3 col-md-6">
  <select class="form-control mb-3" name="region_id" id="jsSearchSelect" data-title="Поиск региона">
  <?foreach($regions as $k=>$v):?>
  <option value="<?=$v['id'];?>"><?=$v['name'];?></option>
  <?endforeach;?>
  </select>
</div>

<div class="mb-3 col-md-6">
<?if($m!=false):?>
<form method="post" action="" id="form_jsGetRegionMonth">
  <select name="month" class="form-select jsChangeSelect" data-btn="jsGetRegionMonth" data-clear="jsSearchSelectObjId">
    <?foreach($m as $k=>$v):?>
    <option value="<?=$v['month'];?>"><?=formatDateToRussian($v['month']);?></option>
    <?endforeach;?>
  </select> 
   <input type="hidden" name="module" value="regions" />
   <input type="hidden" name="component" value="" />
   <input type="hidden" name="ajaxLoad" value="jsSearchSelectResult" />
   <input type="hidden" name="opaco" value="1" />
   <input type="hidden" name="alert" value="" />
   <button class="send_form hidden" id="jsGetRegionMonth"></button>
</form>
<?endif;?>
</div>

<div class="row" id="jsSearchSelectResult">
<?=$regionsList;?>  
</div>

<?endif;?>

</div>