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

if (isset($_POST['form_id']) && $_POST['form_id'] == 'form_jsBackup') {
    
    // Ваши настройки БД
    $backupDb = array(
     'host'=>'localhost', 
     'user'=>'', 
     'pass'=>'', 
     'db'=>''
    );

    $targetDb = array(
     'host'=>'localhost', 
     'user'=>'', 
     'pass'=>'', 
     'db'=>''
    );
  
    $tables = array(
      'aircraft_type',
      'area_bpla',
      'colors',
      'grid_hexagon',
      'grid_square',
      'processed_files',
      'processed_flights',
      'regions',
      'region_stats',
      'region_stats_month',
      'settings'
    );

    $result = copyDatabaseTables($backupDb, $targetDb, $tables);
    exit($result);
    
}