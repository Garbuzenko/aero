<?php defined('DOMAIN') or exit(header('Location: /'));

$regionsList = null;
$regionStats = array();
$startDate = null;
$endDate = null;
$minMonth = null;
$regColorsData = array();
$thisYear = date("Y");

$m = db_query("SELECT month FROM region_stats_month GROUP BY month ORDER BY month DESC");

if ($m != false) {
    
   $filtersArr = transformMonthsToYearStructureDetailed($m);
   $filtersArrJson = json_encode($filtersArr,true);
    
   // берём ближайший месяц
   $lastMonth = $m[0]['month'];
   $lastYear = date("Y",strtotime($lastMonth.'-01'));
   
   $endDate = $lastMonth.'-'.date('t', strtotime($lastMonth));
   
   // вытаскиваем статистику по регионам за последний год
   $stat = db_query("SELECT * 
   FROM region_stats_month 
   WHERE month LIKE ('".$lastYear."-%')");
   
   if ($stat != false) {
     foreach($stat as $k=>$v) {
       // количество полётов 
       if (empty($regionStats[ $v['region_id'] ]['total_flights'])) {
          $regionStats[ $v['region_id'] ]['total_flights'] = $v['total_flights'];
       }
       
       else {
          $regionStats[ $v['region_id'] ]['total_flights'] += $v['total_flights'];
       }
       // ----------------------------------------------------
       
       // дни без полёта
       if (empty($regionStats[ $v['region_id'] ]['zero_days'])) {
          $regionStats[ $v['region_id'] ]['zero_days'] = $v['zero_days'];
       }
       
       else {
          $regionStats[ $v['region_id'] ]['zero_days'] += $v['zero_days'];
       }
       // ----------------------------------------------------
       
       $regionStats[ $v['region_id'] ]['months'][] = $v['month']; 
       
       // средняя продолжительность полёта
       if (empty($regionStats[ $v['region_id'] ]['avg_flight_duration'])) {
          $regionStats[ $v['region_id'] ]['avg_flight_duration'] = $v['avg_flight_duration'];
       }
       
       else {
          $regionStats[ $v['region_id'] ]['avg_flight_duration'] += $v['avg_flight_duration'];
       }
       // ----------------------------------------------------
       
       // среднее количество полётов за день
       if (empty($regionStats[ $v['region_id'] ]['median_daily_flights'])) {
          $regionStats[ $v['region_id'] ]['median_daily_flights'] = $v['median_daily_flights'];
       }
       
       else {
          $regionStats[ $v['region_id'] ]['median_daily_flights'] += $v['median_daily_flights'];
       }
       // ----------------------------------------------------
       
       // плотность на 1000 км2
       if (empty($regionStats[ $v['region_id'] ]['flight_density'])) {
          $regionStats[ $v['region_id'] ]['flight_density'] = $v['flight_density'];
       }
       
       else {
          $regionStats[ $v['region_id'] ]['flight_density'] += $v['flight_density'];
       }
       // ----------------------------------------------------
      
       // максимальное количество за день
       $regionStats[ $v['region_id'] ]['peak_load'][] = $v['peak_load'];
     }
     
     // перебираем массив, нужно посчитать среднее по всем месяцам значение
     // продолжительность полёта в минутах
     // средняя плотность на 1000 км2
     // взять одно максимальное значение полётов за день
     foreach($regionStats as $region_id=>$val) {
         $countMonths = count( $val['months'] );
         
         $regColorsData[ $region_id ] = $val['total_flights'];
         
         if (empty($minMonth)) {
            $minMonth = min($val['months']);
         }
         
         // форматируем для лучшей читаемости количество полётов
         //$regionStats[ $region_id ]['total_flights'] = number_format($val['total_flights'],0,'',' ');
         
         // средняя арифметическая продолжительность полёта в минутах за выбранное количество месяцев
         $regionStats[ $region_id ]['avg_flight_duration'] = $val['avg_flight_duration'] / $countMonths;
         
         if (!empty( $regionStats[ $region_id ]['avg_flight_duration'] )) {
            //$regionStats[ $region_id ]['avg_flight_duration'] = minutesToHoursMinutes( round($regionStats[ $region_id ]['avg_flight_duration']));
            $regionStats[ $region_id ]['avg_flight_duration'] = round($regionStats[ $region_id ]['avg_flight_duration']);
         }
         // ----------------------------------------------------
         
         // средняя арифметическая плотность полётов на 1000 км2 за выбранное количество месяцев
         $regionStats[ $region_id ]['flight_density'] = $val['flight_density'] / $countMonths;
         
         if (!empty( $regionStats[ $region_id ]['flight_density'])) {
             $regionStats[ $region_id ]['flight_density'] =  round($regionStats[ $region_id ]['flight_density'],2);
         }
         // ----------------------------------------------------
         
         // среднее арифметическое количество полётов за день
         $regionStats[ $region_id ]['median_daily_flights'] = $val['median_daily_flights'] / $countMonths;
         
         if (!empty( $regionStats[ $region_id ]['median_daily_flights'])) {
             $regionStats[ $region_id ]['median_daily_flights'] =  round($regionStats[ $region_id ]['median_daily_flights']);
         }
         // ----------------------------------------------------
         
         // максимальное количество полётов за день из всех выбранных месяцев
         $regionStats[ $region_id ]['max_peak_load'] = max($val['peak_load']);
         $regionStats[ $region_id ]['min_peak_load'] = min($val['peak_load']);
         
         unset($regionStats[ $region_id ]['months']);
         unset($regionStats[ $region_id ]['peak_load']);
         
     }
     
     $maxValue = max($regColorsData);
     $minValue = min($regColorsData);
     arsort($regColorsData);
   }
}


//exit( print_r($regColorsData) );

// список регионов
$regions = array();
$myPolygonsData = array();
$myPolygonsDataJson = json_encode( array() );

if (!empty($minMonth)) {
    $startDate = $minMonth.'-01';
}

$colorsReg = array();
$colors = db_query("SELECT * FROM colors ORDER BY percent");

if ($colors != false) {
    foreach($colors as $k=>$v) {
        $colorsReg[ $v['percent'] ] = $v['color'];
    }
}

$regList = db_query("SELECT * FROM regions");

if ($regList != false) {
    foreach($regList as $k=>$v) {
        $img = DOMAIN.'/img/regions/0.jpg';
        $flag = DOMAIN.'/img/regions/0.jpg';
        
        if (!empty($v['img_flag'])) {
            if ( file_exists($_SERVER['DOCUMENT_ROOT'].'/img/flags/'.$v['img_flag'])) {
              $flag = DOMAIN.'/img/flags/'.$v['img_flag'];
            }
        }
        
        if (file_exists($_SERVER['DOCUMENT_ROOT'].'/img/regions/'.$v['id'].'.jpg')) {
            $img = DOMAIN.'/img/regions/'.$v['id'].'.jpg';
        }
        
        $keys = array_keys($regColorsData);
        $position = array_search($v['id'], $keys) + 1;
        
        $regions[] = array(
          'total_flights' => $regionStats[ $v['id'] ]['total_flights'],
          'id' => $v['id'],
          'name' => $v['name'],
          'img' => $img,
          'flag' => $flag,
          'url' => DOMAIN.'/regions/'.$v['pagename']      
        );
       
        
        // Массив полигонов для карты
          $myPolygonsData[] = array(
            array( 'id' => $v['id'],
             'coordinates' => json_decode($v['polygon_v3'],true),
             'fillColor' => regionColor($colorsReg,$regionStats[ $v['id'] ]['total_flights'],$minValue,$maxValue),
             'properties' => array(
               'name' => $v['name'], 
               'startDate' => $startDate, 
               'endDate' => $endDate,
               'totalFlights' => number_format($regionStats[ $v['id'] ]['total_flights'],0,'',' '),
               'avgFlightDuration' => minutesToHoursMinutes($regionStats[ $v['id'] ]['avg_flight_duration']),
               'maxPeakLoad' => $regionStats[ $v['id'] ]['max_peak_load'],
               'flightDensity' => $regionStats[ $v['id'] ]['flight_density'],
               'medianDailyFlights' => $regionStats[ $v['id'] ]['median_daily_flights'],
               'rating' => $position,
               'flag' => $flag
             )
            )
           );
    }
    
    arsort($regions);
    
    $myPolygonsDataJson = json_encode($myPolygonsData, true);
}

?>