<?php defined('DOMAIN') or exit(header('Location: /'));

$xc['bread_crumbs'] = array(
  0 => array('anchor' => 'Настройки', 'url' => '', 'status' => 1)
);

// достаём данные из таб. settings
$set = db_query("SELECT * FROM settings");

?>