<?php defined('DOMAIN') or exit(header('Location: /'));

$xc['bread_crumbs'] = array(
  0 => array('anchor' => 'Отчёты', 'url' => '', 'status' => 1)
);

$reports = array();

$list = db_query("SELECT r.*, 
 users.login,
 users.first_name,
 users.last_name 
 FROM reports AS r
 LEFT JOIN users ON r.user_id = users.id 
 ORDER BY r.id DESC");
 
 if ($list != false) {
    foreach($list as $k=>$v) {
        
        $title = $v['title'];
        
        if (!empty($v['start_date']) && !empty($v['end_date'])) {
            $title .= '<br>за период с '.date('d.m.Y',strtotime($v['start_date'])).' по '.date('d.m.Y',strtotime($v['end_date']));
        }
        
        $userName = $v['login'];
        
        if (!empty($v['first_name'])) {
            $userName = $v['first_name'];
        }
        
        if (!empty($v['last_name'])) {
            if (empty($userName)) {
                $userName = $v['last_name'];
            }
            
            else {
                $userName .= ' '.$v['last_name'];
            }
        }
        
        $timestamp = strtotime($v['created_at']); 
        
        $time = date("H:i",$timestamp);
        $date = date('d.m.Y',$timestamp);
        //$date = formatDateToRussian2($date, $case = 'genitive');
        
        $fileUrl = null;
        
        if (!empty($v['filepath']) && file_exists($_SERVER['DOCUMENT_ROOT'].$v['filepath'])) {
            $fileUrl = DOMAIN.$v['filepath'];
        }
        
        
        $reports[] = array(
           'id' => $v['id'],
           'title' => $title,
           'user' => $userName,
           'date' => $date.' в '.$time,
           'file' => $fileUrl
        );
    }
 }
 
 //exit(print_r($reports));