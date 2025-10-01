<?foreach($regions as $k=>$v):?>
  <div id="card_<?=$v['id'];?>" class="col-xxl-6 col-xl-6 col-lg-12 col-md-12 layout-spacing">
    <div class="statbox widget box box-shadow">
      <div class="widget-content widget-content-area">
         <div class="row">
           <div class="col-xxl-10 col-xl-12 col-lg-10 col-md-10 col-sm-10 mx-auto">
             <a class="card style-7" href="<?=$v['url'];?>" target="_blank">
               <img src="<?=$v['img'];?>" class="card-img-top" alt="">
               <div class="card-footer">
                 <h6 class="card-title mb-0"><?=$v['name'];?></h6>
                 <?if(!empty($regionStats[ $v['id'] ])):?>
                 <p class="card-text">Количество полётов: <?=$regionStats[ $v['id'] ]['total_flights'];?><br />
                 Средняя длительность полёта: <?=$regionStats[ $v['id'] ]['avg_flight_duration'];?><br />
                 Пиковая нагрузка за день: <?=$regionStats[ $v['id'] ]['peak_load'];?><br />
                 Плотность полётов на 1000 км<sup style="font-size: 7px;">2</sup>: <?=$regionStats[ $v['id'] ]['flight_density'];?><br />
                 Дней без полёта: <?=$regionStats[ $v['id'] ]['zero_days'];?>
                 </p>
                 <?endif;?>
               </div>
              </a>                               
            </div>                              
           </div>
        </div>
      </div>
   </div>
  <?endforeach;?>