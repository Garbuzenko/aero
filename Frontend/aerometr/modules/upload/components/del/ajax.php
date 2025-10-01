<?php defined('DOMAIN') or exit(header('Location: /'));

if (isset($_POST['form_id']) && $_POST['form_id'] == 'form_jsClearFiles') {
    
    // достаём список файлов
    $list = db_query("SELECT * FROM processed_files");
    
    if ($list != false) {
        foreach($list as $k=>$v) {
            if (file_exists($_SERVER['DOCUMENT_ROOT'].'/files/'.$v['filename'])) {
                unlink($_SERVER['DOCUMENT_ROOT'].'/files/'.$v['filename']);
            }
        }
        
        // очищаем таб. с файлами
        $del = db_query("DELETE FROM `processed_files`","d");
        
        if ($del == true) {
            exit('');
        }
        
    }
    
}