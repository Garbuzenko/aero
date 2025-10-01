<?php defined('DOMAIN') or exit(header('Location: /'));

// фильтры для карты
if (isset($_POST['form_id']) && $_POST['form_id'] == 'form_jsShowMapFilters') {

    
    $regionStats = array();
    $maxValue = 0;
    $minValue = 0;
    $month = null;
    $quarter = null;
    
    $year = intval($_POST['year']);
    
    $startDate = $year.'-01-01';
    $endDate = $year.'-12-31';
    
    if (!empty($_POST['month'])) {
        $month = intval($_POST['month']);
        
        if ($month < 10) {
            $month = '0'.$month;
        }
        
        $d = $year.'-'.$month;
        
        $startDate = $year.'-'.$month.'-01';
        $endDate = $d.'-'.date('t', strtotime($d));
    }
    
    if (!empty($_POST['quarter'])) {
        $quarter = intval($_POST['quarter']);
        list($startDate,$endDate) = quarterDates($quarter,$year);
    }
    
    if (!empty($_POST['dates'])) {
        $d = explode('—', $_POST['dates']);
        $startDate = date('Y-m-d', strtotime($d[0]));
        $endDate = date('Y-m-d', strtotime($d[1]));
    }
    

    $stat = db_query("SELECT * 
    FROM region_stats 
    WHERE date >= '".$startDate."' 
    AND date <= '".$endDate."'");
    
    if ($stat == false) {
        $html = popup_window('Нет данных за выбранный период','Что-то не так...');
        exit($html);
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
        $html = popup_window('Таблица с регионами пуста','Что-то не так...');
        exit($html);
     }
     
     foreach($regList as $k=>$v) {
        
        $flag = DOMAIN.'/img/regions/0.jpg';
        
        if (!empty($v['img_flag'])) {
            if ( file_exists($_SERVER['DOCUMENT_ROOT'].'/img/flags/'.$v['img_flag'])) {
              $flag = DOMAIN.'/img/flags/'.$v['img_flag'];
            }
        }
        
        $keys = array_keys($regColorsData);
        $position = array_search($v['id'], $keys) + 1;
        
        $regions[] = array(
          'total_flights' => $regionStats[ $v['id'] ]['total_flights'],
          'id' => $v['id'],
          'name' => $v['name'],
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

    ob_start();
    include $_SERVER['DOCUMENT_ROOT'] .'/modules/main/components/map/includes/map.inc.php';
    $map = ob_get_clean();

    exit($map);
}

if (isset($_POST['form_id']) && $_POST['form_id'] == 'form_jsShowRegionData') {
    //exit( print_r($_POST) );
    
    $region_id = intval($_POST['region_id']);
    $start_date = clearData($_POST['start_date'],'date');
    $end_date = clearData($_POST['end_date'],'date');
    
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
    
    // достаём название региона
    $r = db_query("SELECT name, img_flag FROM regions WHERE id=".$region_id." LIMIT 1");
    
    if ($r != false) {
        
        // типы беспилотников
        $typeArr = array();
        $airTypesJson = null;
        $airTypesCountJson = null;
        
        $types = db_query("SELECT 
        aircraft_type,
        COUNT(*) as type_count
        FROM processed_flights 
        WHERE region_id = '".$region_id."'
        AND dof_date >= '".$start_date."' 
        AND dof_date <= '".$end_date."'
        GROUP BY aircraft_type
        ORDER BY type_count DESC");
        
        if ($types != false) {
            
            $typeName = db_query("SELECT type, name 
            FROM aircraft_type");
        
            if ($typeName != false) {
              foreach($typeName as $k=>$v) {
                $typeArr[ $v['type'] ] = $v['name'];
              } 
            }
            
            foreach($types as $k=>$v) {
                
                $at = $v['aircraft_type'];
                
                if (!empty($typeArr[ $v['aircraft_type'] ])) {
                    $at = $typeArr[ $v['aircraft_type'] ].' ('.$v['aircraft_type'].')';
                }
                
                $stat['air_types'][] = $at;
                $stat['air_types_count'][] = $v['type_count'];
            }
            
            $airTypesJson = json_encode($stat['air_types']);
            $airTypesCountJson = str_replace('"','', json_encode($stat['air_types_count']) ); 
            
            // считаем количество беспилотников по месяцам
            $colTypes = db_query("SELECT id, dof_date
            FROM processed_flights 
            WHERE region_id = '".$region_id."'
            AND dof_date >= '".$start_date."' 
            AND dof_date <= '".$end_date."' 
            ORDER BY dof_date");
            
            foreach($colTypes as $k=>$v) {
                
                if (!empty($v['dof_date'])) {
                  $mt = substr($v['dof_date'],0,7);
                
                  if (empty($countMonthBla[ $mt ])) {
                     $countMonthBla[ $mt ] = 1;
                  }
                
                  else {
                     $countMonthBla[ $mt ] += 1;
                  }
                }
            }
            $countMonthBlaJson = array_values($countMonthBla);
            $countMonthBlaJson = json_encode($countMonthBlaJson);
            // ---------------------------------------------------------------------
            
        }
        
        else {
            $html = popup_window('По этому региону нет данных за выбранный период','Нет данных :('); 
            exit($html);
        }
        // -------------------------------------------------------------------------
        
        // статистика из regions_stat
        $totalFlightsJson = null;
        $timeOfDay = array();
        

        $timeOfDaySettings = array(
           'morning' => array(
           'name' => 'Утренние', 
           'bar' => 'bg-gradient-info', 
           'icon' => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-sunrise"><path d="M17 18a5 5 0 0 0-10 0"></path><line x1="12" y1="2" x2="12" y2="9"></line><line x1="4.22" y1="10.22" x2="5.64" y2="11.64"></line><line x1="1" y1="18" x2="3" y2="18"></line><line x1="21" y1="18" x2="23" y2="18"></line><line x1="18.36" y1="11.64" x2="19.78" y2="10.22"></line><line x1="23" y1="22" x2="1" y2="22"></line><polyline points="8 6 12 2 16 6"></polyline></svg>'
         ),
           'day' => array(
           'name' => 'Дневные', 
           'bar' => 'bg-gradient-primary',
           'icon' => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-sun"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>'
         ),
           'evening' => array(
           'name' => 'Вечерние', 
           'bar' => 'bg-gradient-warning',
           'icon' => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-sunset"><path d="M17 18a5 5 0 0 0-10 0"></path><line x1="12" y1="9" x2="12" y2="2"></line><line x1="4.22" y1="10.22" x2="5.64" y2="11.64"></line><line x1="1" y1="18" x2="3" y2="18"></line><line x1="21" y1="18" x2="23" y2="18"></line><line x1="18.36" y1="11.64" x2="19.78" y2="10.22"></line><line x1="23" y1="22" x2="1" y2="22"></line><polyline points="16 5 12 9 8 5"></polyline></svg>'
         ),
           'night' => array(
           'name' => 'Ночные', 
           'bar' => 'bg-gradient-dark', 
           'icon' => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-moon"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>'
         )
        );

        $rStat = db_query("SELECT * 
        FROM region_stats 
        WHERE region_id = '".$region_id."'
        AND date >= '".$start_date."' 
        AND date <= '".$end_date."'
        ORDER BY date");
        
        if ($rStat != false) {
            foreach($rStat as $k=>$v) {
                
                // считаем количество полётов по месяцам
                $mt = substr($v['date'],0,7);
                
                if (empty($countMonthFl[ $mt ])) {
                    $countMonthFl[ $mt ] = $v['total_flights'];
                }
                
                else {
                    $countMonthFl[ $mt ] += $v['total_flights'];
                }
                // -------------------------------------------------------
                
                // общее количество полётов за период
                if (empty($stat['total_flights'])) {
                    $stat['total_flights'] = $v['total_flights'];
                }
                
                else {
                    $stat['total_flights'] += $v['total_flights'];
                }
                // -------------------------------------------------------
                
                // сумируем значение число на 1000 км2
                $stat['flight_density'] += $v['flight_density'];
                
                // средняя длительность полёта в минутах
                $stat['avg_duration_min'] += $v['avg_duration_min'];
                
                // количество полётов по дням 
                $stat['total_flights_list'][] = $v['total_flights'];
                // -------------------------------------------------------
                
                // считаем дни без полёта
                if ($v['total_flights'] == 0) {
                    $stat['zero_days']++;
                }
                // -------------------------------------------------------
                
                // Прогресс бары - полёты по времени суток
                if (empty($timeOfDay['morning']['flights'])) {
                    $timeOfDay['morning']['flights'] = $v['morning_flights'];
                }
                
                else {
                    $timeOfDay['morning']['flights'] += $v['morning_flights'];
                }
                
                if (empty($timeOfDay['day']['flights'])) {
                    $timeOfDay['day']['flights'] = $v['afternoon_flights'];
                }
                
                else {
                    $timeOfDay['day']['flights'] += $v['afternoon_flights'];
                }
                
                if (empty($timeOfDay['evening']['flights'])) {
                    $timeOfDay['evening']['flights'] = $v['evening_flights'];
                }
                
                else {
                    $timeOfDay['evening']['flights'] += $v['evening_flights'];
                }
                
                if (empty($timeOfDay['night']['flights'])) {
                    $timeOfDay['night']['flights'] = $v['night_flights'];
                }
                
                else {
                    $timeOfDay['night']['flights'] += $v['night_flights'];
                }
                // -------------------------------------------------------
        
            }
            
        
            // количество полётов за каждый день, а соответственно и количество дней в периоде
            if (!empty($stat['total_flights_list'])) {
                
                $countDays = count($stat['total_flights_list']);
                
                // день с максимальным количеством полётов за период
                $stat['peak_load'] = max($stat['total_flights_list']);
                
                // среднее количество полётов за день
                $stat['median_daily_flights'] = round( $stat['total_flights'] / $countDays ); 
                
                // средняя длительность полёта
                $stat['avg_flight_duration'] = round( $stat['avg_duration_min'] / $countDays );
                $stat['avg_flight_duration'] = minutesToHoursMinutes($stat['avg_flight_duration']);
                
                // плотность полётов на 1000 км2
                $stat['flight_density'] = $stat['flight_density'] / $countDays; 
                $stat['flight_density'] = round( $stat['flight_density'], 2 );
                
                $totalFlightsJson = str_replace('"','', json_encode($stat['total_flights_list']) ); 
            }
            
            if (!empty($stat['total_flights'])) {
                
               $timeOfDay['morning']['percent'] = ($timeOfDay['morning']['flights'] / $stat['total_flights']) * 100;
               $timeOfDay['day']['percent'] = ($timeOfDay['day']['flights'] / $stat['total_flights']) * 100;
               $timeOfDay['evening']['percent'] = ($timeOfDay['evening']['flights'] / $stat['total_flights']) * 100;   
               $timeOfDay['night']['percent'] = ($timeOfDay['night']['flights'] / $stat['total_flights']) * 100;
               
               $timeOfDay['morning']['percent'] = round($timeOfDay['morning']['percent']);
               $timeOfDay['day']['percent'] = round($timeOfDay['day']['percent']);
               $timeOfDay['evening']['percent'] = round($timeOfDay['evening']['percent']);   
               $timeOfDay['night']['percent'] = round($timeOfDay['night']['percent']);
               
               $stat['total_flights'] = number_format($stat['total_flights'],0,'',' ');
               
            }
            
            $countMonthFlJson = array_values($countMonthFl);
            $countMonthFlJson = json_encode($countMonthFlJson);
            $cm = array_keys($countMonthFl);
            $cArr = array();
            
            foreach($cm as $k=>$v) {
                $cArr[] = dateRussianMonthShort(strtotime($v.'-01'));
            }
            
            $countMonthFlLabelsJson = json_encode($cArr);
            
        }
        // -------------------------------------------------------------------------
        
        $flag = DOMAIN.'/img/flags/'.$r[0]['img_flag'];
        
        $btnTitle = $r[0]['name'].' ('.date('d.m.Y',strtotime($start_date)).' - '.date('d.m.Y',strtotime($end_date)).')';
        $btnDownload = '&nbsp;&nbsp; <button class="btn btn-success" onclick="captureFullPage(\'jsContent\',\'#060818\',\''.$btnTitle.'\')">Скачать графики</button>';
        
        $title = '<img src="'.$flag.'" height="30" /> &nbsp;'.$btnTitle.$btnDownload;
        
        // достаём шаблон дашборда
        ob_start();
        include $_SERVER['DOCUMENT_ROOT'].'/modules/main/components/map/includes/regionStat.inc.php';
        $html = ob_get_clean();
        
        $arr = array(
        0 => 'popupBottom',
        1 => $html,
        2 => $title,
        3 => '100%',
        4 => '100%',
        5 => 10000000);

        $arr = json_encode($arr);

        exit($arr);
    }

    

}
