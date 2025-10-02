<?php defined('DOMAIN') or exit(header('Location: /'));?>
<div class="row layout-top-spacing">

<div id="fuMultipleFile" class="col-lg-5 layout-spacing">
  <div class="statbox widget box box-shadow">
    <div class="widget-content widget-content-area" style="height: 290px;">

       <div class="row">
         <div class="col-md-12 mx-auto">
                                            
         <form method="post" action="" id="form_jsFileUpload">
         <div class="multiple-file-upload">
           <input type="file" 
           class="filepond file-upload-multiple"
           name="filepond" 
           multiple 
           data-allow-reorder="true"
           data-max-file-size="20MB"
           data-max-files="3">
         </div>
                                            
         <input type="hidden" name="module" value="upload" />
         <input type="hidden" name="component" value="" />
         <input type="hidden" name="filepondMulti" value="1" />
         <input type="hidden" name="ajaxLoad" value="processedFiles" />
         <input type="hidden" name="showProgress" value="jsEditUploadStatus" />
         <input type="hidden" name="showProgressScript" value="<?=DOMAIN;?>/modules/upload/includes/progress-bar.inc.php" />
         <input type="hidden" name="noBlackout" value="1" />
         <input type="hidden" name="alert" value="" />
         <button class="send_form btn btn-primary mt-2 w-100" id="jsFileUpload">Загрузить</button>
         </form>
         
         <div id="jsEditUploadStatus"></div>
                                            
         </div>
       </div>
    </div>
  </div>
</div>

<div class="col-lg-7 layout-spacing">
  <div class="statbox widget box box-shadow">
    <div class="widget-content widget-content-area">

       <div class="row">
         <div class="col-md-12 mx-auto">
           <div id="uploadTerminal" class="uploadTerminalMainBlock py-2 px-3 border">
             <?if($lastUploads!=false):?>
               <?foreach($reversedArray as $k=>$v):?>
               <?=$v['timestamp'];?>
               <?=$v['message'];?><br />
               <?endforeach;?>
             <?endif;?>
           </div>
          </div>
       </div>
    </div>
  </div>
</div>

<div id="processedFiles">
<?=$processedFiles;?>
</div>
</div>