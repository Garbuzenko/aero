<?php

$a = db_query("SELECT * 
  FROM log 
  WHERE status IS NULL 
  ORDER BY id LIMIT 1");
  
/*
$a = db_query("SELECT * 
  FROM log 
  WHERE status=0 
  ORDER BY id LIMIT 1");
*/
if ($a == false) {
        $arr = array(
         'percent' => 0,
         'terminal' => '',
         'progress' => '0%'
        );
}

else {
    $message = $a[0]['timestamp'].' '.$a[0]['message'].'<br>';

    $arr = array(
     'percent' => $a[0]['procent'],
     'terminal' => $message,
     'progress' => $a[0]['procent'].'%'
    );

    $json = json_encode($arr,true);

    // почаем сообщение, как прочитанное
    $upd = db_query("UPDATE log 
    SET status=1 
    WHERE id=".$a[0]['id']." 
    LIMIT 1","u");
}



exit($json);