<?php defined('DOMAIN') or exit(header('Location: /'));

$dash = str_replace('/','',$_SERVER['REQUEST_URI']);

$modArr = array(
 'dash-regions' => array(
   'title' => 'Регионы',
   'breadcrumbs' => 'Дашборд регионов',
   'url' => 'https://datalens.yandex/io9bconwz0ne3?_no_controls=1&_theme=dark&_lang=ru',
   'height' => 1500
 ),
 'dash-honeycombs' => array(
   'title' => 'Соты',
   'breadcrumbs' => 'Соты',
   'url' => 'https://datalens.yandex/swlfq591h6y2d?_no_controls=1&_lang=ru&_theme=dark',
   'height' => 870
 ),
 'flight-density' => array(
   'title' => 'Среднее время полёта',
   'breadcrumbs' => 'Среднее время полёта',
   'url' => 'https://datalens.yandex/6b5m2dmadeb2r?_no_controls=1&_lang=ru&_theme=dark',
   'height' => 950
 ),
 'dash-clusterization' => array(
   'title' => 'Кластеризация',
   'breadcrumbs' => 'Кластеризация',
   'url' => 'https://datalens.yandex/38vb62bqq1coo?_no_controls=1&_lang=ru&_theme=dark',
   'height' => 1000
 ),
 'dash-heatmap' => array(
   'title' => 'Тепловая карта',
   'breadcrumbs' => 'Тепловая карта',
   'url' => 'https://datalens.yandex/ch4kmvjuy11yx?_no_controls=1&_lang=ru&_theme=dark',
   'height' => 1000
 ),
 'dash-infrastructure' => array(
   'title' => 'Инфраструктура',
   'breadcrumbs' => 'Инфраструктура',
   'url' => 'https://datalens.yandex/jm1woidpcsi44?_no_controls=1&_theme=dark',
   'height' => 1000
 ),
 'dash-aviation' => array(
   'title' => 'Онлайн авиация',
   'breadcrumbs' => 'Онлайн авиация',
   'url' => 'https://datalens.yandex/6byfsmt3tkyyr?_no_controls=1&_lang=ru&_theme=dark',
   'height' => 1000
 )
);

$xc['bread_crumbs'] = array(
  0 => array('anchor' => $modArr[$dash]['breadcrumbs'], 'url' => '', 'status' => 1)
);

$title = $modArr[$dash]['title'];