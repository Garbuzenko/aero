<?php defined('DOMAIN') or exit(header('Location: /'));?>

<div class="row layout-top-spacing">

<?if($set!=false):?>
<div class="col-lg-12 layout-spacing">
   <div class="widget-content widget-content-area">
     <div class="table-responsive">
     <form method="post" action="" id="form_jsEditSettings">
     <table class="table table-bordered">
       <thead>
         <tr>
           <th scope="col">Описание</th>
           <th scope="col">Значение</th>
           <th scope="col">Отредактировано</th>
         </tr>
       </thead>
       <tbody>
       <?foreach($set as $val):?>
         <tr>
           <td><?=$val['description'];?></td>
           <td class="p-0">
            <input type="text" name="update-<?=$val['key_name']?>" value="<?=$val['value'];?>" class="w-100 settingsTransparentInput" />
           </td>   
           <td>
            <?=date('H:i d.m.Y',strtotime($val['updated_at']));?>
           </td>                                  
         </tr>
       <?endforeach;?>
       </tbody>
     </table>
     
     <input type="hidden" name="module" value="settings" />
     <input type="hidden" name="component" value="" />
     <input type="hidden" name="ok" value="Настройки сохранены!" />
     <input type="hidden" name="alert" value="" />
     <button class="send_form btn btn-primary mt-2" id="jsEditSettings">Сохранить настройки</button>
     
     </form>
    </div>
   </div>
</div>
<?endif;?>

<div class="col-lg-12 layout-spacing">
<div class="widget-content widget-content-area">
  <div class="table-responsive">
     <form method="post" action="" id="form_jsBackup">
      <input type="hidden" name="module" value="settings" />
      <input type="hidden" name="component" value="" />
      <input type="hidden" name="ajaxLoad" value="jsBackupResult" />
      <input type="hidden" name="opaco" value="1" />
      <input type="hidden" name="alert" value="" />
      <button class="send_form btn btn-primary mt-2" id="jsBackup">Восстановить Бэкап</button>
    </form>

<div class="mt-2" id="jsBackupResult"></div>

  </div>
</div>

</div>


</div>