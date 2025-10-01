<?php
define('DOMAIN', 'https://'.$_SERVER['HTTP_HOST']);
define('YANDEX_API_KEY', '');
define('PASS_STR', '');

$xc = array();

// данные для подключения к БД
$xc['db_host'] = 'localhost';
$xc['db_name'] = '';
$xc['db_user'] = '';
$xc['db_pass'] = '';

$xc['update'] = true; 
$xc['noMainTmp'] = false;

$xc['ya_map'] = false; // яндекс карты
$xc['bottom_popup_window'] = false;
$xc['no_metrika'] = false;

$xc['title'] = '';
$xc['canonical'] = null;

$xc['close'] = true;
$xc['description'] = null;
$xc['tmp_url'] = DOMAIN.'/template/cork';


$xc['yaMapsVer'] = 'v3';

$xc['close_modules'] = array(
  'upload' => 1,
  'settings' => 1
);

$xc['open_modules'] = array(
  'report' => 1
);

$xc['mod_menu'] = array(
  'main' => null,
  'upload' => null,
  'module' => null,
  'reports' => null,
  'regions' => null,
  'settings' => null,
  'video' => null,
  'docs' => null,
  'presentation' => null,
  'dash-regions' => null,
  'dash-honeycombs' => null,
  'dash-clusterization' => null,
  'dash-heatmap' => null,
  'dash-infrastructure' => null,
  'dash-aviation' => null,
  'flight-density' => null
);