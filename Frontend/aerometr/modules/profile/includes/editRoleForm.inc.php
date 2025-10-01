<form method="post" action="" id="form_jsSwitchEditRole">
<div class="btn-group mb-4 w-100" role="group" aria-label="Basic radio toggle button group">
    <input type="radio" class="btn-check" name="userRole" value="1" id="btnradio1" autocomplete="off" <?if($role_id==1):?>checked<?endif;?>>
    <label class="btn btn-outline-secondary w-50" for="btnradio1">Администратор</label>
    
    <input type="radio" class="btn-check" name="userRole" value="2" id="btnradio3" autocomplete="off" <?if($role_id==2):?>checked<?endif;?>>
    <label class="btn btn-outline-secondary w-50" for="btnradio3">Оператор</label>
</div>

<input type="hidden" name="module" value="profile" />
<input type="hidden" name="component" value="" />
<input type="hidden" name="url" value="<?=$url;?>" />
<input type="hidden" name="alert" value="" />
<button id="jsSwitchEditRole" class="send_form btn btn-outline-secondary w-100 mb-2 me-4 _effect--ripple waves-effect waves-light">
Сохранить
</button>
</form>