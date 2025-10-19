<?php defined('DOMAIN') or exit(header('Location: /'));

$module = clearData($_GET['mod'], 'get');
$component = clearData($_GET['com'], 'get');

$region = db_query("SELECT * 
 FROM regions 
 WHERE pagename='" . $component . "' 
 LIMIT 1");

if ($region == false) {
    header('HTTP/1.0 404 not found');
    require_once $_SERVER['DOCUMENT_ROOT'] . '/tmp/404.inc.php';
    exit();
}

// метатеги
$title = $region[0]['name'];

$region_id = intval($region[0]['id']);
$start_date = '2025-01-01';
$end_date = '2025-07-31';

if (!empty($xc['url']['start_date']) && !empty($xc['url']['end_date'])) {
    $start_date = clearData($xc['url']['start_date'], 'date');
    $end_date = clearData($xc['url']['end_date'], 'date');
}


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
        FROM " . $xc['processed_flights'] . " 
        WHERE prediction='download'
        AND departure_actual_date >= '" . $start_date . "' 
        AND departure_actual_date <= '" . $end_date . "' 
        AND region_id='" . $region_id . "'");

if ($flights != false) {
    $flightsStat = countFlightsData($flights);
    $totalAllFlights = count($flights);

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

}
// -------------------------------------------------------------------------

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

        $timeOfDay['morning']['percent'] = ($timeOfDay['morning']['flights'] / $stat['total_flights']) * 100;
        $timeOfDay['day']['percent'] = ($timeOfDay['day']['flights'] / $stat['total_flights']) * 100;
        $timeOfDay['evening']['percent'] = ($timeOfDay['evening']['flights'] / $stat['total_flights']) * 100;
        $timeOfDay['night']['percent'] = ($timeOfDay['night']['flights'] / $stat['total_flights']) * 100;

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
$stat['flight_density'] = (count($flights) / $region[0]['area_sq_km']) * 1000;
$stat['flight_density'] = round($stat['flight_density'], 2);
        
// среднее количество полётов за день
$stat['median_daily_flights'] = round( count($flights) / $countDays);

// средняя длительность полёта
$stat['avg_flight_duration'] = minutesToHoursMinutes($flightsStat['avgFlightsDuration']);
        
// -------------------------------------------------------------------------


$title = $region[0]['name'] . '. Статистика с ' . date('d.m.Y', strtotime($start_date)) . ' по ' . date('d.m.Y', strtotime($end_date));
$btnTitle = $title;

$period =  'с '.date('d.m.Y', strtotime($start_date)) . ' по ' . date('d.m.Y', strtotime($end_date));

$regionImg = null;
        
if (file_exists($_SERVER['DOCUMENT_ROOT'].'/img/regions/'.$region[0]['id'].'.jpg')) {
   $regionImg = DOMAIN.'/img/regions/'.$region[0]['id'].'.jpg';
}

// достаём шаблон дашборда
ob_start();
include $_SERVER['DOCUMENT_ROOT'] . '/modules/main/components/map/includes/regionStat.inc.php';
$regionStat = ob_get_clean();

$xc['bread_crumbs'] = array(0 => array(
        'anchor' => 'Регионы',
        'url' => DOMAIN . '/regions',
        'status' => 0), 1 => array(
        'anchor' => $title,
        'url' => '',
        'status' => 1));
