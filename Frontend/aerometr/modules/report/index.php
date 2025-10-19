<?php defined('DOMAIN') or exit(header('Location: /'));

$regionsList = null;
$regionStats = array();
$start_date = '2025-01-01';
$end_date = '2025-07-31';
$regColorsData = array();

if (!empty($xc['url']['start_date']) && !empty($xc['url']['end_date'])) {
    $start_date = clearData($xc['url']['start_date'],'date');
    $end_date = clearData($xc['url']['end_date'],'date');
}
   
  $stat = db_query("SELECT * 
    FROM region_stats 
    WHERE prediction='download'
    AND date >= '".$start_date."' 
    AND date <= '".$end_date."'");
    
    if ($stat == false) {
        exit();
    }  
    
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
       if ($v['total_flights'] == 0) {
          if (empty($regionStats[ $v['region_id'] ]['zero_days'])) {
            $regionStats[ $v['region_id'] ]['zero_days'] = 1;
          }
       
          else {
            $regionStats[ $v['region_id'] ]['zero_days']++;
          }
       }
       
       else {
         // собираем все полётные дни, что бы потом выбрать из них максимальный по количетву полётов
         $regionStats[ $v['region_id'] ]['peak_load'][] = $v['total_flights']; 
       }
       // ----------------------------------------------------
       
       $regionStats[ $v['region_id'] ]['days'][] = $v['date']; 
       
       // средняя продолжительность полёта
       if (empty($regionStats[ $v['region_id'] ]['avg_flight_duration'])) {
          $regionStats[ $v['region_id'] ]['avg_flight_duration'] = $v['avg_duration_min'];
       }
       
       else {
          $regionStats[ $v['region_id'] ]['avg_flight_duration'] += $v['avg_duration_min'];
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
    }
    
     //echo '<pre>';print_r($regionStats);echo '</pre>';exit();
    
     // перебираем массив, нужно посчитать среднее по всем дням значение
     // продолжительность полёта в минутах
     // средняя плотность на 1000 км2
     // выбрать максимальное количество полётов за день
     foreach($regionStats as $region_id=>$val) {
         
         $countDays = count( $val['days'] );
         
         $regColorsData[ $region_id ] = $val['total_flights'];
         
         // средняя арифметическая продолжительность полёта в минутах за выбранное количество дней
         $regionStats[ $region_id ]['avg_flight_duration'] = round( $val['avg_flight_duration'] / $countDays );
         
         
         // средняя арифметическая плотность полётов на 1000 км2 за выбранное количество месяцев
         $regionStats[ $region_id ]['flight_density'] = $val['flight_density'] / $countDays;
         
         if (!empty( $regionStats[ $region_id ]['flight_density'])) {
             $regionStats[ $region_id ]['flight_density'] =  round($regionStats[ $region_id ]['flight_density'],2);
         }
         // ----------------------------------------------------
         
         // среднее арифметическое количество полётов за день
         $regionStats[ $region_id ]['median_daily_flights'] = round( $val['total_flights'] / $countDays );
         
         
         // максимальное количество полётов за день в выбранном периоде
         if (!empty($val['peak_load'])) {
            $regionStats[ $region_id ]['max_peak_load'] = max($val['peak_load']);
            unset($regionStats[ $region_id ]['peak_load']);
         }
         
         else {
            $regionStats[ $region_id ]['max_peak_load'] = 0;
         }
         
         unset($regionStats[ $region_id ]['days']);
         
     }
     
     $maxValue = max($regColorsData);
     $minValue = min($regColorsData);
     arsort($regColorsData);
     
     // список регионов
     $regions = array();
     $myPolygonsData = array();
     $myPolygonsDataJson = json_encode( array() );

     $colorsReg = array();
     $colors = db_query("SELECT * FROM colors ORDER BY percent");

     if ($colors != false) {
       foreach($colors as $k=>$v) {
         $colorsReg[ $v['percent'] ] = $v['color'];
       }
     }

     $regList = db_query("SELECT * FROM regions");

     if ($regList == false) {
        exit();
     }
     
     foreach($regList as $k=>$v) {
     
        $keys = array_keys($regColorsData);
        $position = array_search($v['id'], $keys) + 1;
        
        $regions[] = array(
          'total_flights' => $regionStats[ $v['id'] ]['total_flights'],
          'id' => $v['id'],
          'name' => $v['name'],   
        );
       
    }
    
    arsort($regions);

?>