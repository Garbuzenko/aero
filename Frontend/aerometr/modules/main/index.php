<?php defined('DOMAIN') or exit(header('Location: /'));

$mapVer = 1;
$regionsList = null;
$regionStats = array();
$startDate = null;
$endDate = null;
$minMonth = null;
$regColorsData = array();
$thisYear = date("Y");
$totalAllFlights = 0;

$countMonthFl = array();
$countMonthBla = array();
$countMonthFlJson = null;
$countMonthBlaJson = null;
$countMonthFlLabelsJson = null;

$stat = array();
$stat['zero_days'] = 0;
$stat['peak_load'] = 0;
$stat['median_daily_flights'] = 0;
$stat['flight_density'] = 0;
$stat['avg_duration_min'] = 0;
$stat['avg_flight_duration'] = 0;

$mapVer = 1;

$m = db_query("SELECT month 
  FROM region_stats_month 
  WHERE prediction='download' 
  GROUP BY month 
  ORDER BY month DESC");

if ($m != false) {
    
   $filtersArr = transformMonthsToYearStructureDetailed($m);
   $filtersArrJson = json_encode($filtersArr,true);
    
   // берём ближайший месяц
   $lastMonth = $m[0]['month'];
   $lastYear = date("Y",strtotime($lastMonth.'-01'));
   
   $endDate = $lastMonth.'-'.date('t', strtotime($lastMonth));
   
   // вытаскиваем статистику по регионам за последний год
   $stat1 = db_query("SELECT * 
   FROM region_stats_month 
   WHERE prediction='download'
   AND month LIKE ('".$lastYear."-%')");
   
   if ($stat1 != false) {
     foreach($stat1 as $k=>$v) {
       
        // считаем количество полётов по месяцам
        $mt = $v['month'];

        if (empty($countMonthFl[$mt])) {
            $countMonthFl[$mt] = $v['total_flights'];
        } else {
            $countMonthFl[$mt] += $v['total_flights'];
        }
       // ------------------------------------------------------- 
        
       // общее количество полётов за период
        if (empty($stat['total_flights'])) {
            $stat['total_flights'] = $v['total_flights'];
        } else {
            $stat['total_flights'] += $v['total_flights'];
        }
        // -------------------------------------------------------

       
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
     
     
     // количество дней в выбранном периоде
    $monthArr = array_keys($countMonthFl);
    $countDays = countDaysInMonths($monthArr);
     
     // перебираем массив, нужно посчитать среднее по всем месяцам значение
     // продолжительность полёта в минутах
     // средняя плотность на 1000 км2
     // взять одно максимальное значение полётов за день
     foreach($regionStats as $region_id=>$val) {
         $countMonths = count( $val['months'] );
         
         $regColorsData[ $region_id ] = $val['total_flights'];
         //$totalAllFlights += $val['total_flights'];
         
         if (empty($minMonth)) {
            $minMonth = min($val['months']);
         }

         // форматируем для лучшей читаемости количество полётов
         //$regionStats[ $region_id ]['total_flights'] = number_format($val['total_flights'],0,'',' ');
         
         // средняя арифметическая продолжительность полёта в минутах за выбранное количество месяцев
         $regionStats[ $region_id ]['avg_flight_duration'] = $val['avg_flight_duration'] / $countMonths;
         
         if (!empty( $regionStats[ $region_id ]['avg_flight_duration'] )) {
            //$regionStats[ $region_id ]['avg_flight_duration'] = minutesToHoursMinutes( round($regionStats[ $region_id ]['avg_flight_duration']));
            $regionStats[ $region_id ]['avg_flight_duration'] = minutesToHoursMinutes(round($regionStats[ $region_id ]['avg_flight_duration']));
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
     
     $countMonthFlJson = array_values($countMonthFl);
     $countMonthFlJson = json_encode($countMonthFlJson);
     $cm = array_keys($countMonthFl);
     $cArr = array();

     foreach ($cm as $k => $v) {
        $cArr[] = dateRussianMonthShort(strtotime($v . '-01'));
     }

     $countMonthFlLabelsJson = json_encode($cArr);
     
   }
   //exit( print_r($regColorsData) );
   // вытаскиваем все полёты за выбранный период
   // типы беспилотников
   $typeArr = array();
   $airTypesJson = null;
   $airTypesCountJson = null;

   $typeName = db_query("SELECT type, name FROM aircraft_type");

    if ($typeName != false) {
      foreach ($typeName as $k => $v) {
        $typeArr[$v['type']] = $v['name'];
      }
   }

   $flightsStat = array();
   
   $flights = db_query("SELECT *
   FROM ".$xc['processed_flights']."
   WHERE prediction='download' 
   AND departure_actual_date LIKE ('".$lastYear."-%')");
   
   if ($flights != false) {

      $flightsStat = countFlightsData($flights);
      
      if (!empty($flightsStat['type'])) {
        foreach ($flightsStat['type'] as $airType => $airTypeCount) {
            $stat['air_types'][] = $airType . ' (' . $typeArr[$airType] . ')';
            $stat['air_types_count'][] = $airTypeCount;
        }

        $airTypesJson = json_encode($stat['air_types']);
        $airTypesCountJson = str_replace('"', '', json_encode($stat['air_types_count']));
      }

      if (!empty($flightsStat['months'])) {
        $countMonthBlaJson = array_values($flightsStat['months']);
        $countMonthBlaJson = json_encode($countMonthBlaJson);
      }
      
      $stat['peak_load'] = $flightsStat['dayPeakLoad'];
      
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

$totalAllFlights = count($flights);
$ruAreaSqKm = 0; // будем считать общую площадь всех регионов

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
        
        $ruAreaSqKm += $v['area_sq_km'];
        
        $countBla = 0;
        
        if (!empty($flightsStat['regions'][ $v['id'] ])) {
            $countBla = $flightsStat['regions'][ $v['id'] ];
        }
        
        $keys = array_keys($regColorsData);
        $position = array_search($v['id'], $keys) + 1;
        
        $percentFlights = 0;
        $regionTotalFlights = 0;
        
        $peakLoad = 0;
        $avgFlightDuration = 0;
        $flightDensity = 0;
        $medianDailyFlights = 0;
        
        if (!empty($regionStats[ $v['id'] ]['total_flights'])) {
          $percentFlights = countPercentFlights($totalAllFlights,$regionStats[ $v['id'] ]['total_flights']);
          $regionTotalFlights = $regionStats[ $v['id'] ]['total_flights'];
        }
        
        if (!empty($regionStats[ $v['id'] ])) {
            $peakLoad = $regionStats[ $v['id'] ]['max_peak_load'];
            $avgFlightDuration = $regionStats[ $v['id'] ]['avg_flight_duration'];
            $flightDensity = $regionStats[ $v['id'] ]['flight_density'];
            $medianDailyFlights = $regionStats[ $v['id'] ]['median_daily_flights'];
        }
        
        $regions[] = array(
          'total_flights' => $regionTotalFlights,
          'count_bla' => $countBla,
          'id' => $v['id'],
          'name' => $v['name'],
          'url' => DOMAIN.'/regions/'.$v['pagename'].'?start_date='.$startDate.'&end_date='.$endDate,
          'img' => $img,
          'flag' => $flag,
          'percent' => $percentFlights    
        );
       
        
        // Массив полигонов для карты
          $myPolygonsData[] = array(
            array( 'id' => $v['id'],
             'coordinates' => json_decode($v['polygon_v3'],true),
             'fillColor' => regionColor($colorsReg,$regionTotalFlights,$minValue,$maxValue),
             'properties' => array(
               'name' => $v['name'], 
               'startDate' => $startDate, 
               'endDate' => $endDate,
               'totalFlights' => number_format($regionTotalFlights,0,'',' '),
               'totalBla' => number_format($countBla,0,'',' '),
               'avgFlightDuration' => $avgFlightDuration,
               'maxPeakLoad' => $peakLoad,
               'flightDensity' => $flightDensity,
               'medianDailyFlights' => $medianDailyFlights,
               'rating' => $position,
               'flag' => $flag
             )
            )
           );
    }
    
    arsort($regions);
    
    $myPolygonsDataJson = json_encode($myPolygonsData, true);
}

// плотность полётов на 1000 км2
$stat['flight_density'] = (count($flights) / $ruAreaSqKm) * 1000;
$stat['flight_density'] = round($stat['flight_density'], 2);

// среднее количество полётов за день
$stat['median_daily_flights'] = round( count($flights) / $countDays);

// средняя длительность полёта
$stat['avg_flight_duration'] = minutesToHoursMinutes($flightsStat['avgFlightsDuration']);

// заголовок для скриншотов
$mainTitle = 'Полёты БВС по России. Статистика с ' . date('d.m.Y', strtotime($startDate)) . ' по ' . date('d.m.Y', strtotime($endDate));

?>