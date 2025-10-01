<style>
.text-wrap-table {
  table-layout: fixed;
  border-collapse: collapse;
  margin: 0 auto;
}
.text-wrap-table thead {
  background-color: #1b2e4b; /* Светло-серый фон */
}
.text-wrap-table thead th {
  border-bottom: 2px solid #191e3a; /* Более толстая граница для заголовков */
  font-weight: 600;
  color: #bfc9d4;
}
.text-wrap-table th,
.text-wrap-table td {
  word-wrap: break-word;
  word-break: break-all;
  white-space: normal;
  overflow-wrap: break-word;
  hyphens: auto;
  padding: 12px 4px;
  vertical-align: top;
  border-bottom: 1px solid #191e3a;
}

.text-wrap-table td {
    background-color: #0e1726 !important;
}

.text-wrap-table col:nth-child(1) { width: 3%; }
.text-wrap-table col:nth-child(2) { width: 27%; }
.text-wrap-table col:nth-child(3) { width: 12%; }
.text-wrap-table col:nth-child(4) { width: 14%; }
.text-wrap-table col:nth-child(5) { width: 15%; }
.text-wrap-table col:nth-child(6) { width: 13%; }
.text-wrap-table col:nth-child(7) { width: 16%; }
</style>


<div class="row layout-top-spacing">

  <img src="<?=DOMAIN;?>/img/map.png" style="width: 880px; margin: 20px auto;" />
  <div class="col-xl-12 col-lg-12 col-sm-12  layout-spacing">
    <div class="widget-content widget-content-area br-8">
        <h5 class="text-center mb-3">Период с <?=formatDateToRussian2($start_date,'genitive');?> по <?=formatDateToRussian2($end_date,'genitive');?></h5>
        <table class="text-wrap-table" style="width: 800px; table-layout: fixed;">
          
          <thead>
            <tr>
              <th class="text-center">#</th>
              <th>Регион</th>
              <th>Число полётов</th>
              <th>В среднем за день</th>
              <th>Среднее время полёта</th>
              <th>Пиковая нагрузка</th>
              <th>Плотность на 1000 км<sup style="font-size: 7px;">2</sup></th>
              
            </tr>
          </thead>
          <tbody>
          <?$i=1; foreach($regions as $key=>$val):?>
          <tr>
            <td class="text-center"><?=$i;?></td>
            <td><span class="fw-bold"><?=$val['name'];?></span></td>
            <td><?=number_format($regionStats[ $val['id'] ]['total_flights'],0,'',' ');?></td>
            <td><?=$regionStats[ $val['id'] ]['median_daily_flights'];?></td>
            <td><?=minutesToHoursMinutes($regionStats[ $val['id'] ]['avg_flight_duration']);?></td>
            <td><?=$regionStats[ $val['id'] ]['max_peak_load'];?></td>
            <td><?=$regionStats[ $val['id'] ]['flight_density'];?></td>
            
          </tr>
          <?$i++; endforeach;?>
          </tbody>
        </table>
    </div>
</div>  
</div>