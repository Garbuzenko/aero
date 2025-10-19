<script>
// Асинхронная инициализация карты
async function initMap() {
    // Ждем загрузки основных модулей API
    await ymaps3.ready;

    // Импортируем необходимые классы из глобального объекта ymaps3
    const {YMap, YMapDefaultSchemeLayer, YMapDefaultFeaturesLayer, YMapFeatureDataSource, YMapLayer, YMapFeature, YMapListener} = ymaps3;

    // Создаем экземпляр карты
    const map = new YMap(
        document.getElementById('map'),
        {
            location: {
                center: [37.6173, 55.7558],
                zoom: 4
            },
            theme: 'dark'
        }
    );

    // Добавляем основные слои
    map.addChild(new YMapDefaultSchemeLayer());
    map.addChild(new YMapDefaultFeaturesLayer({zIndex: 1800}));

    const myPolygonsData = <?=$myPolygonsDataJson;?>;

// 1. Создаем источник данных для геообъектов
const dataSource = new ymaps3.YMapFeatureDataSource({
    id: 'my-polygon-source'
});

// 2. Добавляем источник на карту
map.addChild(dataSource);

// 3. Создаем слой, который будет отображать объекты из нашего источника
const layer = new ymaps3.YMapLayer({
    source: 'my-polygon-source', // ID нашего источника
    type: 'features', // Тип слоя - для отображения геообъектов
    zIndex: 1900 // Порядок отображения (может потребовать подбора)
});


map.addChild(layer);


// 4. Для каждого полигона в массиве данных создаем и добавляем объект на карту
myPolygonsData.forEach(polygonData => {
    const feature = new ymaps3.YMapFeature({
        id: polygonData[0].id,
        source: 'my-polygon-source',
        geometry: {
            type: 'Polygon',
            coordinates: polygonData[0].coordinates
        },
        style: {
            stroke: [{
                width: 2,
                color: '#FFFFFF'
            }],
            fill: polygonData[0].fillColor
        
        },
        properties: {
            originalData: polygonData[0],
            name: polygonData[0].name || 'Полигон ' + polygonData[0].id,
            startDate: polygonData[0].startDate,
            endDate: polygonData[0].endDate
        }
    });
    
    // Добавляем объект (фичу) на карту
    map.addChild(feature);
});

// Создаем элемент для tooltip
const mapContainer = document.getElementById('map');         
const tooltip = document.getElementById('jsTooltip');

let isOverFeature = false;
let currentFeatureData = null;

// Функция для отображения tooltip
function showTooltip(properties) {
  if (properties && properties.name) {
    $('#jsTooltip').html('<img class="mb-2" src="'+properties.flag+'" /><br><strong>'+properties.name+'</strong><br>В рейтинге № '+properties.rating+'<br>Количество полётов: '+properties.totalFlights+'<br>Количество БПЛА: '+properties.totalBla+'<br>Среднее время полёта: '+properties.avgFlightDuration+'<br>Среднее количество полётов за день: '+properties.medianDailyFlights+'<br><span>для более подробной статистики кликните на регион</span>').removeClass('hidden');
  }
}

// Функция для скрытия tooltip
function hideTooltip() {
  $('#jsTooltip').html('').addClass('hidden');
}
            
// Обновляем позицию tooltip при движении мыши
mapContainer.addEventListener('mousemove', (e) => {
  if (isOverFeature && currentFeatureData) {
    tooltip.style.left = e.clientX + 'px';
    tooltip.style.top = e.clientY + 'px';
  }
});
            
mapContainer.addEventListener('mouseleave', () => {
  hideTooltip();
  isOverFeature = false;
  currentFeatureData = null; 
});

// Создаем слушатель для наведения мыши
const hoverListener = new ymaps3.YMapListener({
  layer: 'any',
  onPointerMove: (object, event) => {
                    
  if (event && event.coordinates) {
    // Если курсор проходит над полигоном
    if (object && object.type === 'feature' && object.entity) {
    
    // Пробуем получить properties через публичное свойство
    const properties = object.entity.properties;
                   
    // Если properties нет, пробуем через _props
    const originalData = properties ? properties.originalData : (object.entity._props && object.entity._props.properties ? object.entity._props.properties.originalData : null);
       if (originalData) {
         showTooltip(originalData.properties);
         isOverFeature = true;
         currentFeatureData = originalData;
         return;
       } 
    }
            
    else {
      hideTooltip();
      isOverFeature = false;
      currentFeatureData = null; 
    }         
   }                                
  },
  
  onPointerLeave: () => {
    hideTooltip();
    isOverFeature = false;
    currentFeatureData = null;
  }
});

// Добавляем слушатель наведения на карту
map.addChild(hoverListener);

// обработчик кликов
const mapListener = new ymaps3.YMapListener({
    layer: 'any',
    onClick: (object, event) => {
        if (event && event.coordinates) {
            // Если кликнули по объекту (фиче)
            if (object && object.type === 'feature' && object.entity) {
                // Пробуем получить properties через публичное свойство
                const properties = object.entity.properties;
                // Если properties нет, пробуем через _props
                const originalData = properties ? properties.originalData : (object.entity._props && object.entity._props.properties ? object.entity._props.properties.originalData : null);
                if (originalData) {
                    const polygonId = originalData.id;
                    $('#jsMapRegionId').val(polygonId);
                    $('#jsMapStartDate').val(originalData.properties.startDate);
                    $('#jsMapEndDate').val(originalData.properties.endDate);
                    $('#jsShowRegionData').click();
                    
                }
            }
        }
    }
});

// Добавляем слушатель на карту
map.addChild(mapListener);

function calculateBounds(polygonsArray) {
  // Инициализируем переменные минимальными и максимальными значениями
  let minLon = Infinity, maxLon = -Infinity, minLat = Infinity, maxLat = -Infinity;

  polygonsArray.forEach(polygonData => {
    // Предполагается, что координаты находятся в polygonData[0].coordinates
    const coordinates = polygonData[0].coordinates[0]; // Берем первое (внешнее) кольцо полигона
    coordinates.forEach(coord => {
      const [longitude, latitude] = coord;
      minLon = Math.min(minLon, longitude);
      maxLon = Math.max(maxLon, longitude);
      minLat = Math.min(minLat, latitude);
      maxLat = Math.max(maxLat, latitude);
    });
  });

  return [[minLon, minLat], [maxLon, maxLat]]; // Формат: [юго-запад, северо-восток]
}

// Получаем границы для массива полигонов myPolygonsData
const mapBounds = calculateBounds(myPolygonsData);

// Устанавливаем вычисленные границы для карты
map.setLocation({ bounds: mapBounds });
}

// Запускаем инициализацию
initMap().catch(console.error);
</script>