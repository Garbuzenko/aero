<?php defined('DOMAIN') or exit(header('Location: /'));

$component = clearData($_GET['com']);

$modArr = array(
 'overpass' => array(
   'title' => 'Overpass API',
   'breadcrumbs' => 'Overpass API',
   'h1' => 'Overpass API',
   'descr' => 'Для загрузки границ регионов из OpenStreetMap',
   'baseUrl' => 'https://overpass-api.de/api/interpreter',
   'query' => 'https://overpass-api.de/api/interpreter'
   
 ),
 'opensky' => array(
   'title' => 'Opensky API',
   'breadcrumbs' => 'Opensky API',
   'h1' => 'Открытые данные Самолёты в реальном времени',
   'descr' => 'тут краткое описание',
   'baseUrl' => 'https://opensky-network.org/api',
   'query' => 'https://opensky-network.org/api/states/all'
 ),
 'skyarc' => array(
   'title' => 'Skyarc API',
   'breadcrumbs' => 'Skyarc API',
   'h1' => 'Открытые данные Небосвод',
   'descr' => 'Получение точек воздушной инфраструктуры и воздушных зон',
   'baseUrl' => 'https://skyarc.ru/features/atpoint',
   'query' => 'https://skyarc.ru/features/atpoint?lat=80&lng=80'
 )
);

$xc['bread_crumbs'] = array(
  0 => array('anchor' => $modArr[$component]['breadcrumbs'], 'url' => '', 'status' => 1)
);

$title = $modArr[$component]['title'];