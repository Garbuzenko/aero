<div id="jsTooltip" class="mapTooltip hidden"></div>

<div style="position: relative;">
  <div style="position: absolute; width: 200px; top: 20px; right: 20px; z-index: 10;">
  <div class="btn-group mb-1 w-100" role="group" aria-label="Basic radio toggle button group">
      <input type="radio" class="btn-check" name="mapVer" value="1" id="btnradioMap1" autocomplete="off" <?if($mapVer==1):?>checked=""<?endif;?>>
      <label class="btn btn-<?if($mapVer==1):?>primary<?else:?>dark<?endif;?> w-50 jsClickBtn" data-id="jsMapVersion" data-value="1" data-btn="jsShowMapFilters" for="btnradio1">Регионы</label>
    
      <input type="radio" class="btn-check" name="mapVer" value="2" id="btnradioMap2" autocomplete="off" <?if($mapVer==2):?>checked=""<?endif;?>>
      <label class="btn btn-<?if($mapVer==2):?>primary<?else:?>dark<?endif;?> w-50 jsClickBtn" data-id="jsMapVersion" data-value="2" data-btn="jsShowMapFilters" for="btnradio3">Трафик</label>
  </div>
</div>
<div id="map" class="mb-3"></div>
</div>

<div class="row">
<div class="col-xl-4 col-lg-6 col-md-6 col-sm-6 layout-spacing">
   <div class="widget widget-t-sales-widget widget-m-sales">
     <div class="media">
       <div class="icon ml-2">
         <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-bar-chart"><line x1="12" y1="20" x2="12" y2="10"></line><line x1="18" y1="20" x2="18" y2="4"></line><line x1="6" y1="20" x2="6" y2="16"></line></svg>
       </div>
       <div class="media-body">
         <p class="widget-text">Полётов</p>
         <p class="widget-numeric-value"><?=number_format($totalAllFlights,0,'',' ');?></p>
       </div>
     </div>  
      <p class="widget-total-stats">Всего полётов за период</p>                        
   </div>
</div>
                        
<div class="col-xl-4 col-lg-6 col-md-6 col-sm-6 layout-spacing">
  <div class="widget widget-t-sales-widget widget-m-orders">
    <div class="media">
      <div class="icon ml-2">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-send"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
      </div>
        <div class="media-body">
          <p class="widget-text">Полётов в день</p>
          <p class="widget-numeric-value"><?=number_format($stat['median_daily_flights'],0,'',' ');?></p>
        </div>
    </div>  
    <p class="widget-total-stats">В среднем за день</p>              
  </div>
</div>
                        
<div class="col-xl-4 col-lg-6 col-md-6 col-sm-6 layout-spacing">
  <div class="widget widget-t-sales-widget widget-m-customers">
     <div class="media">
       <div class="icon ml-2">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-zap"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
       </div>
       <div class="media-body">
         <p class="widget-text">Пиковая нагрузка</p>
         <p class="widget-numeric-value"><?=number_format($stat['peak_load'],0,'',' ');?></p>
       </div>
     </div> 
     <p class="widget-total-stats">Максимум за день</p>                      
  </div>
</div>
                        
<div class="col-xl-4 col-lg-6 col-md-6 col-sm-6 layout-spacing">
  <div class="widget widget-t-sales-widget widget-m-income">
    <div class="media">
      <div class="icon ml-2">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-watch"><circle cx="12" cy="12" r="7"></circle><polyline points="12 9 12 12 13.5 13.5"></polyline><path d="M16.51 17.35l-.35 3.83a2 2 0 0 1-2 1.82H9.83a2 2 0 0 1-2-1.82l-.35-3.83m.01-10.7l.35-3.83A2 2 0 0 1 9.83 1h4.35a2 2 0 0 1 2 1.82l.35 3.83"></path></svg>
      </div>
      <div class="media-body">
        <p class="widget-text">Время полёта</p>
        <p class="widget-numeric-value"><?=$stat['avg_flight_duration'];?></p>
      </div>
    </div>
    <p class="widget-total-stats">Cреднее время полёта</p>
                                
  </div>
</div> 

<div class="col-xl-4 col-lg-6 col-md-6 col-sm-6 layout-spacing">
   <div class="widget widget-t-sales-widget widget-m-sales">
     <div class="media">
       <div class="icon ml-2">
         <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-activity"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
       </div>
       <div class="media-body">
         <p class="widget-text">Высота полёта</p>
         <p class="widget-numeric-value"><?=$flightsStat['altitudeAvg'];?> м.</p>
       </div>
     </div>  
      <p class="widget-total-stats">Средняя высота полёта</p>                        
   </div>
</div>

<div class="col-xl-4 col-lg-6 col-md-6 col-sm-6 layout-spacing">
  <div class="widget widget-t-sales-widget widget-m-orders">
    <div class="media">
      <div class="icon ml-2">
         <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-copy"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
      </div>
        <div class="media-body">
          <p class="widget-text">Плотность трафика</p>
          <p class="widget-numeric-value"><?=$stat['flight_density'];?></p>
        </div>
    </div>  
    <p class="widget-total-stats">Полётов на 1000 км<sup style="font-size: 7px;">2</sup></p>              
  </div>
</div>                     
</div>

<div class="row layout-top-spacing">
  <div class="col-xl-12 col-lg-12 col-sm-12 layout-spacing">
    <div class="widget-content widget-content-area br-8">
        <table id="ecommerce-list" class="table dt-table-hover" style="width:100%">
          <thead>
            <tr>
              <th>#</th>
              <th>Регион</th>
              <th>Число полётов</th>
              <th class="dt-no-sorting">% от общ. количества</th>
              <th>Количество БПЛА</th>
            </tr>
          </thead>
          <tbody>
          <?$i=1; foreach($regions as $key=>$val):?>
          <tr>
            <td><?=$i;?></td>
            <td>
              <div class="d-flex justify-content-left align-items-center">
                <a href="<?=$val['url'];?>" target="_blank">
                <div class="avatar  me-3">
                  <img src="<?=$val['flag'];?>" alt="<?=$val['name'];?>" width="64" height="64">
                </div>
                </a>
                <div class="d-flex flex-column">
                  <a href="<?=$val['url'];?>" target="_blank">
                  <span class="text-truncate fw-bold"><?=$val['name'];?></span>
                  </a>
                </div>
              </div>
            </td>
            <td><?=$regionStats[ $val['id'] ]['total_flights'];?></td>
            <td><?=$val['percent'];?></td>
            <td><?=$val['count_bla'];?></td>
            
          </tr>
          <?$i++; endforeach;?>
          </tbody>
        </table>
    </div>
  </div>
</div>

<?if($mapVer==1):?>
<?include $_SERVER['DOCUMENT_ROOT'] .'/modules/main/components/map/includes/baseMap.inc.php';?>
<?endif;?>
    
<?if($mapVer==2):?>
<?include $_SERVER['DOCUMENT_ROOT'] .'/modules/main/components/map/includes/heatMap.inc.php';?>
<?endif;?>

<div class="row mb-4">
  <div class="col-md-3">
    <a href="<?=DOMAIN;?>/report/download?start_date=<?=$startDate;?>&end_date=<?=$endDate;?>" class="mb-1">
    <div class="btn btn-success">Скачать отчёт</div>
   </a>
  </div>
</div>

<div class="row" id="jsContenMainPage">

<div class="col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12 layout-spacing <?if(count($countMonthFl) < 3):?>hidden<?endif;?>" id="jsStatDownload3GrafikMainPage">
  <div class="widget widget-chart-one">
    <div class="widget-heading">
      <h5 class="">Количество полётов по месяцам</h5>
    </div>
    
    <div class="widget-content">
      <div id="revenueMonthly2"></div>
    </div>
  </div>
</div>

<!-------------- Круговая диаграмма по типам беспилотников ------------------>
<?if(!empty($flightsStat['type'])):?>
<div class="col-xl-4 col-lg-12 col-md-12 col-sm-12 col-12 layout-spacing">
  <div class="widget widget-chart-two">
    <div class="widget-heading">
      <h5 class="">Типы БВС</h5>
    </div>
    <div class="widget-content">
      <div id="chart-2main" class=""></div>
    </div>
  </div>
</div>
<?endif;?>

<!-------------- Остальные параметры в текстовом виде ----------------------->
<div class="col-xl-8 col-lg-6 col-md-6 col-sm-12 col-12 layout-spacing" id="jsStatDownloadMainPage">
   <div class="widget widget-table-one h-100">
     <div class="widget-heading">
       <h5 class="">Аналитика полётов</h5>
    </div>
    
    <div class="widget-content">
      
      <div class="transactions-list t-info">
        <div class="t-item">
          <div class="t-company-name">
          <div class="t-icon">
            <div class="avatar">
              <span class="avatar-title"><?=$stat['peak_load'];?></span>
            </div>
          </div>
          <div class="t-name">
            <h4>Пиковая нагрузка</h4>
            <p class="meta-date">Наибольшее количество полётов за день в выбранном периоде</p>
          </div>
        </div>
        <div class="t-rate rate-inc">
          <p><span><?=lang_function($stat['peak_load'],'полёт');?></span></p>
        </div>
        </div>
      </div>
    
      <div class="transactions-list">
        <div class="t-item">
          <div class="t-company-name">
            <div class="t-icon">
              <div class="avatar">
                <span class="avatar-title"><?=$stat['median_daily_flights'];?></span>
              </div>
            </div>
            <div class="t-name">
              <h4>Среднее число полётов</h4>
              <p class="meta-date">Среднее количество полётов за сутки</p>
            </div>
         </div>
         <div class="t-rate rate-inc">
            <p><span><?=lang_function($stat['median_daily_flights'],'полёт');?></span></p>
         </div>
      </div>
    </div>
    
    <div class="transactions-list t-info">
      <div class="t-item">
        <div class="t-company-name">
          <div class="t-icon">
            <div class="avatar">
              <span class="avatar-title">КМ</span>
            </div>
          </div>
          <div class="t-name">
            <h4>Плотность трафика</h4>
            <p class="meta-date">Количество полётов на 1000 км<sup style="font-size: 7px;">2</sup></p>
          </div>
        </div>
        <div class="t-rate rate-inc">
          <p><span><?=$stat['flight_density'];?></span></p>
        </div>
      </div>
    </div>
    
    <div class="transactions-list">
      <div class="t-item">
        <div class="t-company-name">
          <div class="t-icon">
            <div class="avatar">
               <span class="avatar-title">CР</span>
            </div>
          </div>
          <div class="t-name">
            <h4>Среднее время полёта</h4>
            <p class="meta-date">Cредняя продолжительность полёта</p>
          </div>
    
        </div>
        <div class="t-rate rate-inc">
           <p><span><?=$stat['avg_flight_duration'];?></span></p>
        </div>
      </div>
    </div>
    
    <div class="transactions-list t-info">
      <div class="t-item">
        <div class="t-company-name">
          <div class="t-icon">
            <div class="avatar">
              <span class="avatar-title">КМ</span>
            </div>
          </div>
          <div class="t-name">
            <h4>Средняя высота полёта</h4>
            <p class="meta-date">Средняя высота полёта в метрах</p>
          </div>
        </div>
        <div class="t-rate rate-inc">
          <p><span><?=$flightsStat['altitudeAvg'];?> м.</span></p>
        </div>
      </div>
    </div>

   </div>
  </div>
</div>
<!--------------------------------------------------------------------------->   

<!--------------------- Прогресс бары (по операторам) ----------------------->
<?if(!empty($flightsStat['operators'])):?> 
<div class="col-xl-12 col-lg-6 col-md-6 col-sm-6 col-12 layout-spacing" id="jsStatDownload2MainPage">
<div class="widget widget-three">
  <div class="widget-heading">
    <h5 class="">Топ 10 опрераторов БВС</h5>
  </div>
  <div class="widget-content">
    <div class="order-summary">
      <?foreach($flightsStat['operators'] as $operKey=>$value):?>
      <div class="summary-list">
        <div class="w-summary-details">
                                                
        <div class="w-summary-info">
          <h6><?=$value['name']?></h6>
          <p class="summary-count"><?=$value['percent'];?>% (<?=number_format($value['countFlights'],0,'',' ');?>)</p>
        </div>
    
        <div class="w-summary-stats">
         <div class="progress">
          <div class="progress-bar bg-gradient-primary" role="progressbar" style="width: <?=$value['percent'];?>%" aria-valuenow="<?=$value['percent'];?>" aria-valuemin="0" aria-valuemax="100"></div>
         </div>
       </div>
       
       </div>
      </div>
      <?endforeach;?>                              
      </div>                               
    </div>
</div>
</div>
<?endif;?> 
<!--------------------------------------------------------------------------->  

</div>

<div class="col-md-3">
    <button class="btn btn-success" onclick="captureFullPage('jsContenMainPage','#060818','<?=$mainTitle;?>')">Скачать графики</button>
</div>
<!--------------------------------------------------------------------------->
<script src="<?=$xc['tmp_url'];?>/src/plugins/src/apex/apexcharts.min.js"></script>          
<script>
function simpleInitCharts2() {
    
 getcorkThemeObject = localStorage.getItem("theme");
    getParseObject = JSON.parse(getcorkThemeObject)
    ParsedObject = getParseObject;

    if (ParsedObject.settings.layout.darkMode) {
      
      var Theme = 'dark';
  
      Apex.tooltip = {
          theme: Theme
      }
  
      /**
          ==============================
          |    @Options Charts Script   |
          ==============================
      */
      
      /*
          =============================
              Daily Sales | Options
          =============================
      */
      var d_2options1 = {
        chart: {
            height: 160,
            type: 'bar',
            stacked: true,
            stackType: '100%',
            toolbar: {
                show: false,
            }
        },
        dataLabels: {
            enabled: false,
        },
        stroke: {
            show: true,
            width: [3, 4],
            curve: "smooth",
        },
        colors: ['#e2a03f', '#e0e6ed'],
        series: [{
            name: 'Sales',
            data: [44, 55, 41, 67, 22, 43, 21]
        },{
            name: 'Last Week',
            data: [13, 23, 20, 8, 13, 27, 33]
        }],
        xaxis: {
            labels: {
                show: false,
            },
            categories: ['Sun', 'Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat'],
            crosshairs: {
            show: false
            }
        },
        yaxis: {
            show: false
        },
        fill: {
            opacity: 1
        },
        plotOptions: {
            bar: {
                horizontal: false,
                columnWidth: '25%',
                borderRadius: 8,
            }
        },
        legend: {
            show: false,
        },
        grid: {
            show: false,
            xaxis: {
                lines: {
                    show: false
                }
            },
            padding: {
            top: -20,
            right: 0,
            bottom: -40,
            left: 0
            }, 
        },
        responsive: [
            {
                breakpoint: 575,
                options: {
                    plotOptions: {
                        bar: {
                            borderRadius: 5,
                            columnWidth: '35%'
                        }
                    },
                }
            },
        ],
      }
      
      /*
          =============================
              Total Orders | Options
          =============================
      */
      
      /*
          =================================
              Revenue Monthly | Options
          =================================
      */
      var options1 = {
        chart: {
          fontFamily: 'Nunito, sans-serif',
          height: 365,
          type: 'area',
          zoom: {
              enabled: false
          },
          dropShadow: {
            enabled: true,
            opacity: 0.2,
            blur: 10,
            left: -7,
            top: 22
          },
          toolbar: {
            show: false
          },
        },
        colors: ['#e7515a', '#2196f3'],
        dataLabels: {
            enabled: false
        },
        markers: {
          discrete: [{
          seriesIndex: 0,
          dataPointIndex: 7,
          fillColor: '#000',
          strokeColor: '#000',
          size: 5
        }, {
          seriesIndex: 2,
          dataPointIndex: 11,
          fillColor: '#000',
          strokeColor: '#000',
          size: 4
        }]
        },
        subtitle: {
          text: '<?=number_format($totalAllFlights,0,'',' ');?>',
          align: 'left',
          margin: 0,
          offsetX: 65,
          offsetY: 20,
          floating: false,
          style: {
            fontSize: '18px',
            color:  '#00ab55'
          }
        },
        title: {
          text: 'Всего:',
          align: 'left',
          margin: 0,
          offsetX: -10,
          offsetY: 20,
          floating: false,
          style: {
            fontSize: '18px',
            color:  '#bfc9d4'
          },
        },
        stroke: {
            show: true,
            curve: 'smooth',
            width: 2,
            lineCap: 'square'
        },
        series: [{
            name: 'Полёты',
            data: <?=$countMonthFlJson;?>
        }, {
            name: 'БПЛА',
            data: <?=$countMonthBlaJson;?>
        }],
        labels: <?=$countMonthFlLabelsJson;?>,
        xaxis: {
          axisBorder: {
            show: false
          },
          axisTicks: {
            show: false
          },
          crosshairs: {
            show: true
          },
          labels: {
            offsetX: 0,
            offsetY: 5,
            style: {
                fontSize: '12px',
                fontFamily: 'Nunito, sans-serif',
                cssClass: 'apexcharts-xaxis-title',
            },
          }
        },
        yaxis: {
          labels: {
            formatter: function(value, index) {
              return value
            },
            offsetX: -15,
            offsetY: 0,
            style: {
                fontSize: '12px',
                fontFamily: 'Nunito, sans-serif',
                cssClass: 'apexcharts-yaxis-title',
            },
          }
        },
        grid: {
          borderColor: '#191e3a',
          strokeDashArray: 5,
          xaxis: {
              lines: {
                  show: true
              }
          },   
          yaxis: {
              lines: {
                  show: false,
              }
          },
          padding: {
            top: -50,
            right: 0,
            bottom: 0,
            left: 5
          },
        }, 
        legend: {
          position: 'top',
          horizontalAlign: 'right',
          offsetY: -50,
          fontSize: '16px',
          fontFamily: 'Quicksand, sans-serif',
          markers: {
            width: 10,
            height: 10,
            strokeWidth: 0,
            strokeColor: '#fff',
            fillColors: undefined,
            radius: 12,
            onClick: undefined,
            offsetX: -5,
            offsetY: 0
          },    
          itemMargin: {
            horizontal: 10,
            vertical: 20
          }
          
        },
        tooltip: {
          theme: Theme,
          marker: {
            show: true,
          },
          x: {
            show: false,
          }
        },
        fill: {
            type:"gradient",
            gradient: {
                type: "vertical",
                shadeIntensity: 1,
                inverseColors: !1,
                opacityFrom: .19,
                opacityTo: .05,
                stops: [100, 100]
            }
        },
        responsive: [{
          breakpoint: 575,
          options: {
            legend: {
                offsetY: -50,
            },
          },
        }]
      }
      
      /*
          ==================================
              Sales By Category | Options
          ==================================
      */
      var options = {
          chart: {
              type: 'donut',
              width: 370,
              height: 430
          },
          colors: ['#622bd7', '#e2a03f', '#e7515a', '#e2a03f'],
          dataLabels: {
            enabled: false
          },
          legend: {
              position: 'bottom',
              horizontalAlign: 'center',
              fontSize: '14px',
              markers: {
                width: 10,
                height: 10,
                offsetX: -5,
                offsetY: 0
              },
              itemMargin: {
                horizontal: 10,
                vertical: 30
              }
          },
          plotOptions: {
            pie: {
              donut: {
                size: '75%',
                background: 'transparent',
                labels: {
                  show: true,
                  name: {
                    show: true,
                    fontSize: '29px',
                    fontFamily: 'Nunito, sans-serif',
                    color: undefined,
                    offsetY: -10
                  },
                  value: {
                    show: true,
                    fontSize: '26px',
                    fontFamily: 'Nunito, sans-serif',
                    color: '#bfc9d4',
                    offsetY: 16,
                    formatter: function (val) {
                      return val
                    }
                  },
                  total: {
                    show: true,
                    showAlways: true,
                    label: 'Всего',
                    color: '#888ea8',
                    fontSize: '30px',
                    formatter: function (w) {
                      return w.globals.seriesTotals.reduce( function(a, b) {
                        return a + b
                      }, 0)
                    }
                  }
                }
              }
            }
          },
          stroke: {
            show: true,
            width: 15,
            colors: '#0e1726'
          },
          
          series: <?=$airTypesCountJson;?>,
          labels: <?=$airTypesJson;?>,
    
          responsive: [
            { 
              breakpoint: 1440, options: {
                chart: {
                  width: 325
                },
              }
            },
            { 
              breakpoint: 1199, options: {
                chart: {
                  width: 380
                },
              }
            },
            { 
              breakpoint: 575, options: {
                chart: {
                  width: 320
                },
              }
            },
          ],
      }

    } else {

      var Theme = 'dark';
  
      Apex.tooltip = {
          theme: Theme
      }
  
      /**
          ==============================
          |    @Options Charts Script   |
          ==============================
      */
      
      /*
          =============================
              Daily Sales | Options
          =============================
      */
      var d_2options1 = {
        chart: {
            height: 160,
            type: 'bar',
            stacked: true,
            stackType: '100%',
            toolbar: {
                show: false,
            }
        },
        dataLabels: {
            enabled: false,
        },
        stroke: {
            show: true,
            width: [3, 4],
            curve: "smooth",
        },
        colors: ['#e2a03f', '#e0e6ed'],
        series: [{
            name: 'Sales',
            data: [44, 55, 41, 67, 22, 43, 21]
        },{
            name: 'Last Week',
            data: [13, 23, 20, 8, 13, 27, 33]
        }],
        xaxis: {
            labels: {
                show: false,
            },
            categories: ['Sun', 'Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat'],
            crosshairs: {
            show: false
            }
        },
        yaxis: {
            show: false
        },
        fill: {
            opacity: 1
        },
        plotOptions: {
            bar: {
                horizontal: false,
                columnWidth: '25%',
                borderRadius: 8,
            }
        },
        legend: {
            show: false,
        },
        grid: {
            show: false,
            xaxis: {
                lines: {
                    show: false
                }
            },
            padding: {
            top: -20,
            right: 0,
            bottom: -40,
            left: 0
            }, 
        },
        responsive: [
            {
                breakpoint: 575,
                options: {
                    plotOptions: {
                        bar: {
                            borderRadius: 5,
                            columnWidth: '35%'
                        }
                    },
                }
            },
        ],
      }
      
      /*
          =============================
              Total Orders | Options
          =============================
      */
      var d_2options2 = {
        chart: {
          id: 'sparkline1',
          group: 'sparklines',
          type: 'area',
          height: 290,
          sparkline: {
            enabled: true
          },
        },
        stroke: {
            curve: 'smooth',
            width: 2
        },
        fill: {
          opacity: 1,
          // type:"gradient",
          // gradient: {
          //     type: "vertical",
          //     shadeIntensity: 1,
          //     inverseColors: !1,
          //     opacityFrom: .30,
          //     opacityTo: .05,
          //     stops: [100, 100]
          // }
        },
        series: [{
          name: 'Sales',
          data: [28, 40, 36, 52, 38, 60, 38, 52, 36, 40]
        }],
        labels: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
        yaxis: {
          min: 0
        },
        grid: {
          padding: {
            top: 125,
            right: 0,
            bottom: 0,
            left: 0
          }, 
        },
        tooltip: {
          x: {
            show: false,
          },
          theme: Theme
        },
        colors: ['#00ab55']
      }
      
      /*
          =================================
              Revenue Monthly | Options
          =================================
      */
      var options1 = {
        chart: {
          fontFamily: 'Nunito, sans-serif',
          height: 365,
          type: 'area',
          zoom: {
              enabled: false
          },
          dropShadow: {
            enabled: true,
            opacity: 0.2,
            blur: 10,
            left: -7,
            top: 22
          },
          toolbar: {
            show: false
          },
        },
        colors: ['#1b55e2', '#e7515a'],
        dataLabels: {
            enabled: false
        },
        markers: {
          discrete: [{
          seriesIndex: 0,
          dataPointIndex: 7,
          fillColor: '#000',
          strokeColor: '#000',
          size: 5
        }, {
          seriesIndex: 2,
          dataPointIndex: 11,
          fillColor: '#000',
          strokeColor: '#000',
          size: 4
        }]
        },
        subtitle: {
          text: '$10,840',
          align: 'left',
          margin: 0,
          offsetX: 100,
          offsetY: 20,
          floating: false,
          style: {
            fontSize: '18px',
            color:  '#4361ee'
          }
        },
        title: {
          text: 'Total Profit',
          align: 'left',
          margin: 0,
          offsetX: -10,
          offsetY: 20,
          floating: false,
          style: {
            fontSize: '18px',
            color:  '#0e1726'
          },
        },
        stroke: {
            show: true,
            curve: 'smooth',
            width: 2,
            lineCap: 'square'
        },
        series: [{
            name: 'Expenses',
            data: [16800, 16800, 15500, 14800, 15500, 17000, 21000, 16000, 15000, 17000, 14000, 17000]
        }, {
            name: 'Income',
            data: [16500, 17500, 16200, 17300, 16000, 21500, 16000, 17000, 16000, 19000, 18000, 19000]
        }],
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        xaxis: {
          axisBorder: {
            show: false
          },
          axisTicks: {
            show: false
          },
          crosshairs: {
            show: true
          },
          labels: {
            offsetX: 0,
            offsetY: 5,
            style: {
                fontSize: '12px',
                fontFamily: 'Nunito, sans-serif',
                cssClass: 'apexcharts-xaxis-title',
            },
          }
        },
        yaxis: {
          labels: {
            formatter: function(value, index) {
              return (value / 1000) + 'K'
            },
            offsetX: -15,
            offsetY: 0,
            style: {
                fontSize: '12px',
                fontFamily: 'Nunito, sans-serif',
                cssClass: 'apexcharts-yaxis-title',
            },
          }
        },
        grid: {
          borderColor: '#e0e6ed',
          strokeDashArray: 5,
          xaxis: {
              lines: {
                  show: true
              }
          },   
          yaxis: {
              lines: {
                  show: false,
              }
          },
          padding: {
            top: -50,
            right: 0,
            bottom: 0,
            left: 5
          },
        }, 
        legend: {
          position: 'top',
          horizontalAlign: 'right',
          offsetY: -50,
          fontSize: '16px',
          fontFamily: 'Quicksand, sans-serif',
          markers: {
            width: 10,
            height: 10,
            strokeWidth: 0,
            strokeColor: '#fff',
            fillColors: undefined,
            radius: 12,
            onClick: undefined,
            offsetX: -5,
            offsetY: 0
          },    
          itemMargin: {
            horizontal: 10,
            vertical: 20
          }
          
        },
        tooltip: {
          theme: Theme,
          marker: {
            show: true,
          },
          x: {
            show: false,
          }
        },
        fill: {
            type:"gradient",
            gradient: {
                type: "vertical",
                shadeIntensity: 1,
                inverseColors: !1,
                opacityFrom: .19,
                opacityTo: .05,
                stops: [100, 100]
            }
        },
        responsive: [{
          breakpoint: 575,
          options: {
            legend: {
                offsetY: -50,
            },
          },
        }]
      }
      
      /*
          ==================================
              Sales By Category | Options
          ==================================
      */
      var options = {
          chart: {
              type: 'donut',
              width: 370,
              height: 430
          },
          colors: ['#622bd7', '#e2a03f', '#e7515a', '#e2a03f'],
          dataLabels: {
            enabled: false
          },
          legend: {
              position: 'bottom',
              horizontalAlign: 'center',
              fontSize: '14px',
              markers: {
                width: 10,
                height: 10,
                offsetX: -5,
                offsetY: 0
              },
              itemMargin: {
                horizontal: 10,
                vertical: 30
              }
          },
          plotOptions: {
            pie: {
              donut: {
                size: '75%',
                background: 'transparent',
                labels: {
                  show: true,
                  name: {
                    show: true,
                    fontSize: '29px',
                    fontFamily: 'Nunito, sans-serif',
                    color: undefined,
                    offsetY: -10
                  },
                  value: {
                    show: true,
                    fontSize: '26px',
                    fontFamily: 'Nunito, sans-serif',
                    color: '#0e1726',
                    offsetY: 16,
                    formatter: function (val) {
                      return val
                    }
                  },
                  total: {
                    show: true,
                    showAlways: true,
                    label: 'Total',
                    color: '#888ea8',
                    fontSize: '30px',
                    formatter: function (w) {
                      return w.globals.seriesTotals.reduce( function(a, b) {
                        return a + b
                      }, 0)
                    }
                  }
                }
              }
            }
          },
          stroke: {
            show: true,
            width: 15,
            colors: '#fff'
          },
          series: [985, 737, 270],
          labels: ['Apparel', 'Sports', 'Others'],
    
          responsive: [
            { 
              breakpoint: 1440, options: {
                chart: {
                  width: 325
                },
              }
            },
            { 
              breakpoint: 1199, options: {
                chart: {
                  width: 380
                },
              }
            },
            { 
              breakpoint: 575, options: {
                chart: {
                  width: 320
                },
              }
            },
          ],
      }
    }
    
  
  /**
      ==============================
      |    @Render Charts Script    |
      ==============================
  */
  
  /*
      ================================
          Revenue Monthly | Render
      ================================
  */
  var chart1 = new ApexCharts(
      document.querySelector("#revenueMonthly2"),
      options1
  );
  
  chart1.render();
  
  /*
      =================================
          Sales By Category | Render
      =================================
  */
  var chart = new ApexCharts(
      document.querySelector("#chart-2main"),
      options
  );
  
  chart.render();
  
  /*
      =============================================
          Perfect Scrollbar | Recent Activities
      =============================================
  */
  const ps = new PerfectScrollbar(document.querySelector('.mt-container-ra'));
  
  // const topSellingProduct = new PerfectScrollbar('.widget-table-three .table-scroll table', {
  //   wheelSpeed:.5,
  //   swipeEasing:!0,
  //   minScrollbarLength:40,
  //   maxScrollbarLength:100,
  //   suppressScrollY: true
  
  // });





  /**
     * =================================================================================================
     * |     @Re_Render | Re render all the necessary JS when clicked to switch/toggle theme           |
     * =================================================================================================
     */
  
  document.querySelector('.theme-toggle').addEventListener('click', function() {

    // console.log(localStorage);

    getcorkThemeObject = localStorage.getItem("theme");
    getParseObject = JSON.parse(getcorkThemeObject)
    ParsedObject = getParseObject;

    if (ParsedObject.settings.layout.darkMode) {

      /*
      =================================
          Revenue Monthly | Options
      =================================
    */

      chart1.updateOptions({
        colors: ['#e7515a', '#2196f3'],
        subtitle: {
          style: {
            color:  '#00ab55'
          }
        },
        title: {
          style: {
            color:  '#bfc9d4'
          }
        },
        grid: {
          borderColor: '#191e3a',
        }
      })


      /*
      ==================================
          Sales By Category | Options
      ==================================
      */

      chart.updateOptions({
        stroke: {
          colors: '#0e1726'
        },
        plotOptions: {
          pie: {
            donut: {
              labels: {
                value: {
                  color: '#bfc9d4'
                }
              }
            }
          }
        }
      })


      /*
          =============================
              Total Orders | Options
          =============================
      */

      d_2C_2.updateOptions({
        fill: {
          type:"gradient",
          gradient: {
              type: "vertical",
              shadeIntensity: 1,
              inverseColors: !1,
              opacityFrom: .30,
              opacityTo: .05,
              stops: [100, 100]
          }
        }
      })

    } else {

      /*
      =================================
          Revenue Monthly | Options
      =================================
    */

      chart1.updateOptions({
        colors: ['#1b55e2', '#e7515a'],
        subtitle: {
          style: {
            color:  '#4361ee'
          }
        },
        title: {
          style: {
            color:  '#0e1726'
          }
        },
        grid: {
          borderColor: '#e0e6ed',
        }
      })


      /*
      ==================================
          Sales By Category | Options
      ==================================
      */

      chart.updateOptions({
        stroke: {
          colors: '#fff'
        },
        plotOptions: {
          pie: {
            donut: {
              labels: {
                value: {
                  color: '#0e1726'
                }
              }
            }
          }
        }
      })


      /*
          =============================
              Total Orders | Options
          =============================
      */

      d_2C_2.updateOptions({
        fill: {
          type:"gradient",
          opacity: 0.9,
          gradient: {
              type: "vertical",
              shadeIntensity: 1,
              inverseColors: !1,
              opacityFrom: .45,
              opacityTo: 0.1,
              stops: [100, 100]
          }
        }
      })
      
      
    }

  })
    
}
                   
simpleInitCharts2();

</script>


