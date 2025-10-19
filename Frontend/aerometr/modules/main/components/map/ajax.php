<?php defined('DOMAIN') or exit(header('Location: /'));

// фильтры для карты
if (isset($_POST['form_id']) && $_POST['form_id'] == 'form_jsShowMapFilters') {


    $regionStats = array();
    $maxValue = 0;
    $minValue = 0;
    $month = null;
    $quarter = null;
    $pointsArr = array();
    $jsonPoints = null;
    $totalAllFlights = 0;

    $mapVer = intval($_POST['map_ver']);

    $year = intval($_POST['year']);

    $startDate = $year . '-01-01';
    $endDate = $year . '-12-31';
    
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

    if (!empty($_POST['month'])) {
        $month = intval($_POST['month']);

        if ($month < 10) {
            $month = '0' . $month;
        }

        $d = $year . '-' . $month;

        $startDate = $year . '-' . $month . '-01';
        $endDate = $d . '-' . date('t', strtotime($d));
    }

    if (!empty($_POST['quarter'])) {
        $quarter = intval($_POST['quarter']);
        list($startDate, $endDate) = quarterDates($quarter, $year);
    }

    if (!empty($_POST['dates'])) {
        $d = explode('—', $_POST['dates']);
        $startDate = date('Y-m-d', strtotime($d[0]));
        $endDate = date('Y-m-d', strtotime($d[1]));
    }

    // достаём цвета из базы
    $colorsReg = array();
    $colors = db_query("SELECT * FROM colors ORDER BY percent");

    if ($colors != false) {
        foreach ($colors as $k => $v) {
            $colorsReg[$v['percent']] = $v['color'];
        }
    }
    // -----------------------------------------------------------

    // достаём и считаем данные по количеству летательных аппаратов
    $hexagonsData = array();
    $hexagonsDataJson = null;
    $countPointsHex = array();
    
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

    $flights = db_query("SELECT * 
    FROM ".$xc['processed_flights']." 
    WHERE prediction='download'
    AND departure_actual_date >= '" . $startDate . "' 
    AND departure_actual_date <= '" . $endDate . "'");

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


    $stat1 = db_query("SELECT * 
    FROM region_stats 
    WHERE prediction='download' 
    AND date >= '" . $startDate . "' 
    AND date <= '" . $endDate . "'");

    if ($stat1 == false) {
        $html = popup_window('Нет данных за выбранный период', 'Что-то не так...');
        exit($html);
    }

    foreach ($stat1 as $k => $v) {
        
        // считаем количество полётов по месяцам
        $mt = substr($v['date'], 0, 7);

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
        if (empty($regionStats[$v['region_id']]['total_flights'])) {
            $regionStats[$v['region_id']]['total_flights'] = $v['total_flights'];
        } else {
            $regionStats[$v['region_id']]['total_flights'] += $v['total_flights'];
        }
        // ----------------------------------------------------

        // дни без полёта
        if ($v['total_flights'] == 0) {
            if (empty($regionStats[$v['region_id']]['zero_days'])) {
                $regionStats[$v['region_id']]['zero_days'] = 1;
            } else {
                $regionStats[$v['region_id']]['zero_days']++;
            }
        } else {
            // собираем все полётные дни, что бы потом выбрать из них максимальный по количетву полётов
            $regionStats[$v['region_id']]['peak_load'][] = $v['total_flights'];
        }
        // ----------------------------------------------------

        $regionStats[$v['region_id']]['days'][] = $v['date'];

        // средняя продолжительность полёта
        if (empty($regionStats[$v['region_id']]['avg_flight_duration'])) {
            $regionStats[$v['region_id']]['avg_flight_duration'] = $v['avg_duration_min'];
        } else {
            $regionStats[$v['region_id']]['avg_flight_duration'] += $v['avg_duration_min'];
        }
        // ----------------------------------------------------

        // плотность на 1000 км2
        if (empty($regionStats[$v['region_id']]['flight_density'])) {
            $regionStats[$v['region_id']]['flight_density'] = $v['flight_density'];
        } else {
            $regionStats[$v['region_id']]['flight_density'] += $v['flight_density'];
        }
        // ----------------------------------------------------
    }
    
    // перебираем массив, нужно посчитать среднее по всем дням значение
    // продолжительность полёта в минутах
    // средняя плотность на 1000 км2
    // выбрать максимальное количество полётов за день
    foreach ($regionStats as $region_id => $val) {

        $countDays = count($val['days']);

        $regColorsData[$region_id] = $val['total_flights'];
        //$totalAllFlights += $val['total_flights'];

        // средняя арифметическая продолжительность полёта в минутах за выбранное количество дней
        $regionStats[$region_id]['avg_flight_duration'] = $val['avg_flight_duration'] / $countDays;

        if (!empty($regionStats[$region_id]['avg_flight_duration'])) {
            $regionStats[$region_id]['avg_flight_duration'] = round($regionStats[$region_id]['avg_flight_duration']);
        }

        // средняя арифметическая плотность полётов на 1000 км2 за выбранное количество месяцев
        $regionStats[$region_id]['flight_density'] = $val['flight_density'] / $countDays;

        if (!empty($regionStats[$region_id]['flight_density'])) {
            $regionStats[$region_id]['flight_density'] = round($regionStats[$region_id]['flight_density'], 2);
        }
        // ----------------------------------------------------

        // среднее арифметическое количество полётов за день
        $regionStats[$region_id]['median_daily_flights'] = round($val['total_flights'] / $countDays);


        // максимальное количество полётов за день в выбранном периоде
        if (!empty($val['peak_load'])) {
            $regionStats[$region_id]['max_peak_load'] = max($val['peak_load']);
            unset($regionStats[$region_id]['peak_load']);
        } else {
            $regionStats[$region_id]['max_peak_load'] = 0;
        }


        unset($regionStats[$region_id]['days']);

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

    // список регионов
    $regions = array();
    $regNameList = array();
    $myPolygonsData = array();
    $myPolygonsDataJson = json_encode(array());
    $ruAreaSqKm = 0; // будем считать общую площадь всех регионов
    
    $totalAllFlights = count($flights);
    
    $regList = db_query("SELECT * FROM regions");

    if ($regList == false) {
        $html = popup_window('Таблица с регионами пуста', 'Что-то не так...');
        exit($html);
    }

    foreach ($regList as $k => $v) {

        $flag = DOMAIN . '/img/regions/0.jpg';

        if (!empty($v['img_flag'])) {
            if (file_exists($_SERVER['DOCUMENT_ROOT'] . '/img/flags/' . $v['img_flag'])) {
                $flag = DOMAIN . '/img/flags/' . $v['img_flag'];
            }
        }
        
        $ruAreaSqKm += $v['area_sq_km'];

        $keys = array_keys($regColorsData);
        $position = array_search($v['id'], $keys) + 1;

        $countBla = 0;

        if (!empty($flightsStat['regions'][$v['id']])) {
            $countBla = $flightsStat['regions'][$v['id']];
        }
        
        $regNameList[ $v['id'] ] = $v['name'];
        
        $percentFlights = 0;
        
        if (!empty($regionStats[ $v['id'] ]['total_flights'])) {
          $percentFlights = countPercentFlights($totalAllFlights,$regionStats[ $v['id'] ]['total_flights']);
        }

        $regions[] = array(
            'total_flights' => $regionStats[$v['id']]['total_flights'],
            'count_bla' => $countBla,
            'id' => $v['id'],
            'name' => $v['name'],
            'url' => DOMAIN.'/regions/'.$v['pagename'].'?start_date='.$startDate.'&end_date='.$endDate,
            'flag' => $flag,
            'percent' => $percentFlights  
        );


        // Массив полигонов для карты
        $myPolygonsData[] = array(array(
                'id' => $v['id'],
                'coordinates' => json_decode($v['polygon_v3'], true),
                'fillColor' => regionColor($colorsReg, $regionStats[$v['id']]['total_flights'], $minValue, $maxValue),
                'properties' => array(
                    'name' => $v['name'],
                    'startDate' => $startDate,
                    'endDate' => $endDate,
                    'totalFlights' => number_format($regionStats[$v['id']]['total_flights'], 0, '',' '),
                    'totalBla' => number_format($countBla, 0, '', ' '),
                    'avgFlightDuration' => minutesToHoursMinutes($regionStats[$v['id']]['avg_flight_duration']),
                    'maxPeakLoad' => $regionStats[$v['id']]['max_peak_load'],
                    'flightDensity' => $regionStats[$v['id']]['flight_density'],
                    'medianDailyFlights' => $regionStats[$v['id']]['median_daily_flights'],
                    'rating' => $position,
                    'flag' => $flag)));
    }

    arsort($regions);

    $myPolygonsDataJson = json_encode($myPolygonsData, true);

    if ($mapVer == 2) {

        $hexMaxValue = 0;
        $hexMinValue = 0;

        if (!empty($flightsStat['hexagonsFlights'])) {
            $hexMaxValue = max($flightsStat['hexagonsFlights']);
            $hexMinValue = min($flightsStat['hexagonsFlights']);


            // достаём из базы гексагоны
            $hex = db_query("SELECT id, region_id, polygon_v3 FROM grid_hexagon");

            if ($hex != false) {
                foreach ($hex as $h) {
                    // берём только те гексагоны, в которых есть полёты
                    if (!empty($flightsStat['hexagonsFlights'][$h['id']])) {
                        
                    $countBla = 0; 
                    
                    if (!empty($flightsStat['hexagons'][$h['id']])) {
                        $countBla = $flightsStat['hexagons'][$h['id']];
                    }
                    

                    $hexagonsData[] = array(array(
                      'id' => $h['id'],
                      'coordinates' => json_decode($h['polygon_v3'], true),
                      'fillColor' => regionColor($colorsReg, $flightsStat['hexagonsFlights'][$h['id']], $hexMinValue, $hexMaxValue),
                      'properties' => array(
                        'hexagonId' => $h['id'],
                        'startDate' => $startDate,
                        'endDate' => $endDate,
                        'totalFlights' => number_format($flightsStat['hexagonsFlights'][$h['id']], 0, '',' '),
                        'totalBla' => number_format($countBla, 0, '', ' '),
                        'period' => date('d.m.Y', strtotime($startDate)) . ' - ' . date('d.m.Y', strtotime($endDate)),
                        'region' => $regNameList[ $h['region_id'] ])));

                    }
                }

                $hexagonsDataJson = json_encode($hexagonsData, true);
            }

        }
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

    ob_start();
    include $_SERVER['DOCUMENT_ROOT'] . '/modules/main/components/map/includes/map.inc.php';
    $map = ob_get_clean();

    exit($map);
}

if (isset($_POST['form_id']) && $_POST['form_id'] == 'form_jsShowRegionData') {
    //exit( print_r($_POST) );

    $region_id = intval($_POST['region_id']);
    $start_date = clearData($_POST['start_date'], 'date');
    $end_date = clearData($_POST['end_date'], 'date');

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
    $r = db_query("SELECT id,
    name, 
    img_flag,
    area_sq_km
    FROM regions 
    WHERE id=" . $region_id . " 
    LIMIT 1");

    if ($r != false) {

        // типы беспилотников
        $airTypesJson = null;
        $airTypesCountJson = null;
        $typeArr = array();
        
        $typeName = db_query("SELECT type, name FROM aircraft_type");

        if ($typeName != false) {
           foreach ($typeName as $k => $v) {
              $typeArr[$v['type']] = $v['name'];
           }
        }
        
        $flights = db_query("SELECT * 
        FROM ".$xc['processed_flights']." 
        WHERE prediction='download'
        AND departure_actual_date >= '" . $start_date . "' 
        AND departure_actual_date <= '" . $end_date . "' 
        AND region_id='" . $region_id . "'");

        if ($flights != false) {
          $flightsStat = countFlightsData($flights);
          $totalAllFlights = count($flights);
          
          if (!empty($flightsStat['type'])) {
             foreach($flightsStat['type'] as $airType=>$airTypeCount) {
                $stat['air_types'][] = $airType.' ('.$typeArr[ $airType ].')';
                $stat['air_types_count'][] = $airTypeCount;
             }
             
             $airTypesJson = json_encode($stat['air_types']);
             $airTypesCountJson = str_replace('"', '', json_encode($stat['air_types_count']));
          }
          
          if (!empty($flightsStat['months'])) {
             $countMonthBlaJson = array_values($flightsStat['months']);
             $countMonthBlaJson = json_encode($countMonthBlaJson);
          }
          
        }
        
        else {
            $html = popup_window('По этому региону нет данных за выбранный период', 'Нет данных :(');
            exit($html);
        }
        // --------------------------------------------------------------------------------
        
        // статистика из regions_stat
        $totalFlightsJson = null;
        $timeOfDay = array();


        $timeOfDaySettings = array(
            'morning' => array(
                'name' => 'Утренние',
                'bar' => 'bg-gradient-info',
                'icon' => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-sunrise"><path d="M17 18a5 5 0 0 0-10 0"></path><line x1="12" y1="2" x2="12" y2="9"></line><line x1="4.22" y1="10.22" x2="5.64" y2="11.64"></line><line x1="1" y1="18" x2="3" y2="18"></line><line x1="21" y1="18" x2="23" y2="18"></line><line x1="18.36" y1="11.64" x2="19.78" y2="10.22"></line><line x1="23" y1="22" x2="1" y2="22"></line><polyline points="8 6 12 2 16 6"></polyline></svg>'),
            'day' => array(
                'name' => 'Дневные',
                'bar' => 'bg-gradient-primary',
                'icon' => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-sun"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>'),
            'evening' => array(
                'name' => 'Вечерние',
                'bar' => 'bg-gradient-warning',
                'icon' => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-sunset"><path d="M17 18a5 5 0 0 0-10 0"></path><line x1="12" y1="9" x2="12" y2="2"></line><line x1="4.22" y1="10.22" x2="5.64" y2="11.64"></line><line x1="1" y1="18" x2="3" y2="18"></line><line x1="21" y1="18" x2="23" y2="18"></line><line x1="18.36" y1="11.64" x2="19.78" y2="10.22"></line><line x1="23" y1="22" x2="1" y2="22"></line><polyline points="16 5 12 9 8 5"></polyline></svg>'),
            'night' => array(
                'name' => 'Ночные',
                'bar' => 'bg-gradient-dark',
                'icon' => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-moon"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>'));

        $rStat = db_query("SELECT * 
        FROM region_stats 
        WHERE prediction='download'
        AND region_id = '" . $region_id . "'
        AND date >= '" . $start_date . "' 
        AND date <= '" . $end_date . "'
        ORDER BY date");

        if ($rStat != false) {
            foreach ($rStat as $k => $v) {

                // считаем количество полётов по месяцам
                $mt = substr($v['date'], 0, 7);

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
                } else {
                    $timeOfDay['morning']['flights'] += $v['morning_flights'];
                }

                if (empty($timeOfDay['day']['flights'])) {
                    $timeOfDay['day']['flights'] = $v['afternoon_flights'];
                } else {
                    $timeOfDay['day']['flights'] += $v['afternoon_flights'];
                }

                if (empty($timeOfDay['evening']['flights'])) {
                    $timeOfDay['evening']['flights'] = $v['evening_flights'];
                } else {
                    $timeOfDay['evening']['flights'] += $v['evening_flights'];
                }

                if (empty($timeOfDay['night']['flights'])) {
                    $timeOfDay['night']['flights'] = $v['night_flights'];
                } else {
                    $timeOfDay['night']['flights'] += $v['night_flights'];
                }
                // -------------------------------------------------------

            }

            // количество полётов за каждый день, а соответственно и количество дней в периоде
            if (!empty($stat['total_flights_list'])) {
                $countDays = count($stat['total_flights_list']);
                $totalFlightsJson = str_replace('"', '', json_encode($stat['total_flights_list']));
            }

            if (!empty($stat['total_flights'])) {

                $timeOfDay['morning']['percent'] = ($timeOfDay['morning']['flights'] / $stat['total_flights']) *
                    100;
                $timeOfDay['day']['percent'] = ($timeOfDay['day']['flights'] / $stat['total_flights']) *
                    100;
                $timeOfDay['evening']['percent'] = ($timeOfDay['evening']['flights'] / $stat['total_flights']) *
                    100;
                $timeOfDay['night']['percent'] = ($timeOfDay['night']['flights'] / $stat['total_flights']) *
                    100;

                $timeOfDay['morning']['percent'] = round($timeOfDay['morning']['percent']);
                $timeOfDay['day']['percent'] = round($timeOfDay['day']['percent']);
                $timeOfDay['evening']['percent'] = round($timeOfDay['evening']['percent']);
                $timeOfDay['night']['percent'] = round($timeOfDay['night']['percent']);

                $stat['total_flights'] = number_format($stat['total_flights'], 0, '', ' ');

            }

            $countMonthFlJson = array_values($countMonthFl);
            $countMonthFlJson = json_encode($countMonthFlJson);
            $cm = array_keys($countMonthFl);
            $cArr = array();

            foreach ($cm as $k => $v) {
                $cArr[] = dateRussianMonthShort(strtotime($v . '-01'));
            }

            $countMonthFlLabelsJson = json_encode($cArr);

        }
        // -------------------------------------------------------------------------
        
        
         // плотность полётов на 1000 км2
        $stat['flight_density'] = (count($flights) / $r[0]['area_sq_km']) * 1000;
        $stat['flight_density'] = round($stat['flight_density'], 2);
        
        // среднее количество полётов за день
        $stat['median_daily_flights'] = round( count($flights) / $countDays);

        // средняя длительность полёта
        $stat['avg_flight_duration'] = minutesToHoursMinutes($flightsStat['avgFlightsDuration']);
        
       // -------------------------------------------------------------------------
        
        
        
        $flag = DOMAIN . '/img/flags/' . $r[0]['img_flag'];
        
        $regionImg = null;
        
        if (file_exists($_SERVER['DOCUMENT_ROOT'].'/img/regions/'.$r[0]['id'].'.jpg')) {
            $regionImg = DOMAIN.'/img/regions/'.$r[0]['id'].'.jpg';
        }
        
        $btnTitle = $r[0]['name'] . ' (' . date('d.m.Y', strtotime($start_date)) . ' - ' . date('d.m.Y', strtotime($end_date)) . ')';
        $btnDownload = '&nbsp;&nbsp; <button class="btn btn-success" onclick="captureFullPage(\'jsContent\',\'#060818\',\'' . $btnTitle . '\')">Скачать графики</button>';

        $title = '<img src="' . $flag . '" height="30" /> &nbsp;' . $btnTitle . $btnDownload;

        // достаём шаблон дашборда
        ob_start();
        include $_SERVER['DOCUMENT_ROOT'] . '/modules/main/components/map/includes/regionStat.inc.php';
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
