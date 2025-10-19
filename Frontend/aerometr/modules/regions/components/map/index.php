<?php defined('DOMAIN') or exit(header('Location: /'));

$start_date = '2025-01-01';
$end_date = '2025-07-31';


if (!empty($xc['url']['region'])) {
    
    $region_id = intval($xc['url']['region']);
    
    if (!empty($xc['url']['start_date']) && !empty($xc['url']['end_date'])) {
        $start_date = clearData($xc['url']['start_date'],'date');
        $end_date = clearData($xc['url']['end_date'],'date');
    }
    
    // достаём информацию о регионе
    $r = db_query("SELECT name, 
    polygon_v3
    FROM regions 
    WHERE id=".$region_id." 
    LIMIT 1");
    
    if ($r == false) {
        exit();
    }
    
    $hexagonsData = array();
    $hexagonsDataJson = null;
    $countPointsHex = array();
    $flightsStat = array();
    
    // достаём информацию о полётах в регионе в заданом периоде
    $flights = db_query("SELECT * 
    FROM ".$xc['processed_flights']."
    WHERE region_id = '".$region_id."'
    AND departure_actual_date >= '".$start_date."' 
    AND departure_actual_date <= '".$end_date."' 
    AND prediction = 'download'");
    
    if ($flights != false) {
        
        $flightsStat = countFlightsData($flights);
        
        foreach($flights as $k=>$v) {
          
          // считаем количество полётов в гексагоне 
          if (empty($countPointsHex[ $v['hexagon_id'] ])) {
            $countPointsHex[ $v['hexagon_id'] ] = 1;
          }
            
          else {
             $countPointsHex[ $v['hexagon_id'] ]++;
          }
          // --------------------------------------------- 
        }
        
        // достаём цвета из базы
        $colorsReg = array();
        $colors = db_query("SELECT * FROM colors ORDER BY percent");

        if ($colors != false) {
           foreach($colors as $k=>$v) {
              $colorsReg[ $v['percent'] ] = $v['color'];
           }
        }
       // -----------------------------------------------------------
       
       
       // максимальное и минимальное количество полётов в гексагонах региона
       $hexMaxValue = max($countPointsHex);
       $hexMinValue = min($countPointsHex);
            
       // достаём из базы гексагоны
       $hex = db_query("SELECT id, polygon_v3 FROM grid_hexagon");
       
       if ($hex != false) {
         foreach($hex as $h) {
            
            // берём только те гексагоны, в которых есть полёты
            if (!empty( $countPointsHex[ $h['id'] ] )) {
                
              $countBla = 0; 
                    
              if (!empty($flightsStat['hexagons'][$h['id']])) {
                 $countBla = $flightsStat['hexagons'][$h['id']];
              }
               
              $hexagonsData[] = array(
                array( 'id' => $h['id'],
                 'coordinates' => json_decode($h['polygon_v3'],true),
                 'fillColor' => regionColor($colorsReg,$countPointsHex[ $h['id'] ],$hexMinValue,$hexMaxValue),
                 'properties' => array(
                   'hexagonId' => $h['id'],
                   'startDate' => $start_date, 
                   'endDate' => $end_date,
                   'totalFlights' => number_format($countPointsHex[ $h['id'] ],0,'',' '),
                   'totalBla' => number_format($countBla, 0, '', ' '),
                   'period' => date('d.m.Y', strtotime($start_date)) . ' - ' . date('d.m.Y', strtotime($end_date)),
                  )
                )
              );   
            }   
          }
           
          $hexagonsDataJson = json_encode($hexagonsData,true);
       }
       // ---------------------------------------------------------------------
       
        // Полигон региона для карты
        $myPolygonsData = array();
        $myPolygonsDataJson = json_encode( array() );
           
        $myPolygonsData[] = array(
            array( 'id' => $region_id,
             'coordinates' => json_decode($r[0]['polygon_v3'],true),
             'properties' => array(
               'name' => $r[0]['name'], 
               'startDate' => $start_date, 
               'endDate' => $end_date
             )
            )
        );
        
        $myPolygonsDataJson = json_encode($myPolygonsData, true);
       
    }
     
}


