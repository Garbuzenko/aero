<?php defined('DOMAIN') or exit(header('Location: /'));

if (isset($_POST['form_id']) && $_POST['form_id'] == 'form_jsDelReport') {
    
    $report_id = intval($_POST['report_id']);
    
    $info = db_query("SELECT * FROM reports WHERE id=".$report_id." LIMIT 1");
    
    if ($info == false) {
        exit();
    }
    
    // очищаем таб. с файлами
    $del = db_query("DELETE FROM reports WHERE id=".$report_id." LIMIT 1","d");
    
    if ($del == true) {
        if (!empty($info[0]['filepath']) && file_exists($_SERVER['DOCUMENT_ROOT'].$info[0]['filepath'])) {
            unlink($_SERVER['DOCUMENT_ROOT'].$info[0]['filepath']);
        }
        
        exit('ok');
           
    }
    
}