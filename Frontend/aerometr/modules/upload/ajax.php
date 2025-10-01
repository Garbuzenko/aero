<?php defined('DOMAIN') or exit(header('Location: /'));


if (isset($_POST['form_id']) && $_POST['form_id'] == 'form_jsFileUpload') {
   //exit( print_r($_FILES) );
   
   if (empty($_FILES)) {
        $html = popup_window('Вы не выбрали файлы для загрузки','Что-то не так...');
        exit($html);
    }
    
    $arr = array();
    
    foreach ($_FILES as $key => $val) {
       
       $extension = pathinfo($val['name'], PATHINFO_EXTENSION);
       $filename = get_filename(str_replace('.'.$extension,'',$val['name']) ).'.'.$extension;
       $uploaddir = 'files/';
       $errors = null;
    
       $download = save_document($val['name'], $val['tmp_name'], $filename, $uploaddir);     
                
       if ($download == true) {
           $arr[] = $filename;   
           $add = db_query("INSERT INTO processed_files (
           filename,
           processed_at,
           status) VALUES (
           '".$filename."',
           NOW(),
           'new')","i");    
       }
    }
    
    if (!empty($arr)) {
        
        $pf = db_query("SELECT * FROM processed_files ORDER BY id DESC");

         if ($pf != false) {
           ob_start();
           include $_SERVER['DOCUMENT_ROOT'].'/modules/upload/includes/result.inc.php';
           $processedFiles = ob_get_clean();
           
           exit($processedFiles);
         }
        
    }
}