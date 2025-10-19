<?php defined('DOMAIN') or exit(header('Location: /'));

$xc['bread_crumbs'] = array(
  0 => array('anchor' => 'Регионы', 'url' => '', 'status' => 1)
);


$regionsList = null;

// достаём уникальные месяцы из таб. region_stats_month
$regionStats = array();

$m = db_query("SELECT month FROM region_stats_month WHERE prediction='download' GROUP BY month");

if ($m != false) {
    // Сортируем по убыванию (от новых к старым)
   usort($m, function($a, $b) {
     return $b['month'] <=> $a['month'];
   });

   // берём ближайший месяц
   $lastMonth = $m[0]['month'];
   
   // вытаскиваем статистику по регионам за этот месяц
   $stat = db_query("SELECT * FROM region_stats_month WHERE prediction='download' AND month='".$lastMonth."'");
   
   if ($stat != false) {
     foreach($stat as $k=>$v) {
        $regionStats[ $v['region_id'] ] = array(
          'total_flights' => $v['total_flights'],
          'avg_flight_duration' => minutesToHoursMinutes( round($v['avg_flight_duration']) ),
          'peak_load' => $v['peak_load'],
          'flight_density' => round($v['flight_density'],2),
          'zero_days' => $v['zero_days']
        );
     }
   }
}

// список регионов
$regions = array();

 $mapPolygonsJson = array(
   "type" => "FeatureCollection",
   "features" => array()
 );

$regionsPolygonList = array();

$regList = db_query("SELECT * FROM regions ORDER BY name ASC");

if ($regList != false) {
    foreach($regList as $k=>$v) {
        $img = DOMAIN.'/img/regions/0.jpg';
        
        if (file_exists($_SERVER['DOCUMENT_ROOT'].'/img/regions/'.$v['id'].'.jpg')) {
            $img = DOMAIN.'/img/regions/'.$v['id'].'.jpg';
        }
        
        $regions[] = array(
          'total_flights' => $regionStats[ $v['id'] ]['total_flights'],
          'id' => $v['id'],
          'name' => $v['name'],
          'img' => $img,
          'url' => DOMAIN.'/regions/'.$v['pagename']
        );

    }
    
    arsort($regions);
    
    ob_start();
    include $_SERVER['DOCUMENT_ROOT'].'/modules/regions/includes/regionsList.inc.php';
    $regionsList = ob_get_clean();
    
}

?>