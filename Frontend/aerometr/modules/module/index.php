<?php defined('DOMAIN') or exit(header('Location: /'));

$dash = str_replace('/','',$_SERVER['REQUEST_URI']);

$modArr = array(
 'dash-regions' => array(
   'title' => 'Регионы',
   'breadcrumbs' => 'Дашборд регионов',
   'url' => 'https://datalens.yandex/io9bconwz0ne3?_no_controls=1&_theme=dark&_lang=ru',
   'height' => 2200
 ),
 'dash-flights' => array(
   'title' => 'Полёты',
   'breadcrumbs' => 'Полёты',
   'url' => 'https://datalens.yandex/bkameohujq98w?_no_controls=1&_theme=dark&_lang=ru',
   'height' => 3500
 ),
 'platforms-bpla' => array(
   'title' => 'Расположение площадок БПЛА 2030 год',
   'breadcrumbs' => 'Расположение площадок БПЛА 2030 год',
   'url' => 'https://datalens.yandex/6fgrb7lzta6ar?_no_controls=1&_theme=dark&_lang=ru',
   'height' => 1000
 ),
 'dash-honeycombs' => array(
   'title' => 'Гексагоны',
   'breadcrumbs' => 'Гексагоны',
//    'url' => 'https://datalens.ru/embeds/dash#dl_embed_token=eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWJlZElkIjoidTBsYXBkdGhpZzFxZiIsImRsRW1iZWRTZXJ2aWNlIjoiWUNfREFUQUxFTlNfRU1CRURESU5HX1NFUlZJQ0VfTUFSSyIsImlhdCI6MTc1OTM0OTI2NSwiZXhwIjoxNzYyOTQ5MjY1LCJwYXJhbXMiOnt9fQ.MdlBvmiNwf_QDICbXjmtnLeIZm82i6KqXqIJjUA8pX3gVdxKoaNXOgnVpBTc24eksqFXaTv7U_bxEpWuBicSji0Ru_DDXbS-puyRaS0uqFMl22-07rEGfAqTA4Dqlge8HS0WnCg2vsC5f6-A_M61a1tTPIsTb45beaU2K9dJ8sD0ShhzMlLgOkFV9g4392jt1XnFlqFGPk4ZocQ7m5F8w0_Pz4sPY6f0eL2UuN2eyMmKTyN3k4Ylf9e9ujUbfh84R35ihbxsEaX4CWdYKzVh23Mre2W97JZuUY6_WhjUmtdJP3bLy_0P0-WG5W2iYEkM0Lfncwo0gETeydw5g5BCqA',
   'url' => 'https://datalens.yandex/ek578ks9jipqz?_no_controls=1&_lang=ru&_theme=dark',
   'height' => 1870
 ),
 'flight-density' => array(
   'title' => 'Плотность полетов',
   'breadcrumbs' => 'Плотность полетов',
   'url' => 'https://datalens.yandex/lrcefrqf3wyw6?_no_controls=1&_lang=ru&_theme=dark',
   'height' => 1050
 ),
 'dash-clusterization' => array(
   'title' => 'Кластеризация',
   'breadcrumbs' => 'Кластеризация',
   'url' => 'https://datalens.yandex/y4prs40mlxfqj?_no_controls=1&_lang=ru&_theme=dark',
   'height' => 1300
 ),
 'dash-heatmap' => array(
   'title' => 'Тепловая карта',
   'breadcrumbs' => 'Тепловая карта',
   'url' => 'https://datalens.yandex/u0lno04y5gh2f?_no_controls=1&_lang=ru&_theme=dark',
   'height' => 1080
 ),
 'dash-infrastructure' => array(
   'title' => 'Инфраструктура',
   'breadcrumbs' => 'Инфраструктура',
   'url' => 'https://datalens.yandex/7dy01fxsehcgs?_no_controls=1&_theme=dark',
   'height' => 1060
 ),
 'dash-aviation' => array(
   'title' => 'Онлайн авиация',
   'breadcrumbs' => 'Онлайн авиация',
   'url' => 'https://datalens.yandex/dj467kv1w83wy?_no_controls=1&_lang=ru&_theme=dark',
   'height' => 2750
 )
);

$xc['bread_crumbs'] = array(
  0 => array('anchor' => $modArr[$dash]['breadcrumbs'], 'url' => '', 'status' => 1)
);

$title = $modArr[$dash]['title'];