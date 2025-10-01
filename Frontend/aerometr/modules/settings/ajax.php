<?php defined('DOMAIN') or exit(header('Location: /'));


if (isset($_POST['form_id']) && $_POST['form_id'] == 'form_jsEditSettings') {
    
    $arr = array();
    
    foreach($_POST as $k=>$v) {
        if (preg_match('/update\-/',$k)) {
            $k = clearData(str_replace('update-','',$k));
            
            $sql = "UPDATE settings 
            SET value='".clearData($v)."' 
            WHERE key_name='".$k."' 
            LIMIT 1";
            
            $upd = db_query($sql,"u");
        }
    }
    
    exit('ok');
}