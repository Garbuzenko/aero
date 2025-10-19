<div id="jsTooltip2" class="mapTooltip hidden"></div>
<div id="regionMap" class="w-100" style="height: 100vh;"></div>
<script>
// Асинхронная инициализация карты
async function initMap() {
    // Ждем загрузки основных модулей API
    await ymaps3.ready;

    // Импортируем необходимые классы из глобального объекта ymaps3
    const {YMap, YMapDefaultSchemeLayer, YMapDefaultFeaturesLayer, YMapFeatureDataSource, YMapLayer, YMapFeature, YMapListener} = ymaps3;

    // Создаем экземпляр карты
    const map = new YMap(
        document.getElementById('regionMap'),
        {
            location: {
                center: [37.6173, 55.7558],
                zoom: 5
            },
            theme: 'dark'
        }
    );

    // Добавляем основные слои
    map.addChild(new YMapDefaultSchemeLayer());
    map.addChild(new YMapDefaultFeaturesLayer({zIndex: 1800}));

    const myPolygonsData = <?=$myPolygonsDataJson;?>;
    const hexagonsData = <?=$hexagonsDataJson;?>;

    // 1. Создаем источник данных для полигонов регионов
    const regionsDataSource = new ymaps3.YMapFeatureDataSource({
        id: 'regions-polygon-source'
    });

    // 2. Создаем источник данных для гексагонов
    const hexagonsDataSource = new ymaps3.YMapFeatureDataSource({
        id: 'hexagons-source'
    });

    // 3. Добавляем источники на карту
    map.addChild(regionsDataSource);
    map.addChild(hexagonsDataSource);

    // 4. Создаем слои для регионов и гексагонов
    const regionsLayer = new ymaps3.YMapLayer({
        source: 'regions-polygon-source',
        type: 'features',
        zIndex: 1900 // Регионы под гексагонами
    });

    const hexagonsLayer = new ymaps3.YMapLayer({
        source: 'hexagons-source',
        type: 'features',
        zIndex: 3000 // Гексагоны поверх регионов
    });

    map.addChild(regionsLayer);
    map.addChild(hexagonsLayer);

    // 5. Добавляем полигоны регионов
    myPolygonsData.forEach(polygonData => {
        const feature = new ymaps3.YMapFeature({
            id: 'region_' + polygonData[0].id,
            source: 'regions-polygon-source',
            geometry: {
                type: 'Polygon',
                coordinates: polygonData[0].coordinates
            },
            style: {
                stroke: [{
                    width: 0,
                    color: '#000000'
                }],
                fill: '#FFFFFF'
            },
            properties: {
                originalData: polygonData[0],
                name: polygonData[0].name || 'Полигон ' + polygonData[0].id,
                startDate: polygonData[0].startDate,
                endDate: polygonData[0].endDate,
                type: 'region'
            },
            // Отключаем взаимодействие для регионов
            interactive: false
        });
        
        map.addChild(feature);
    });
    

    // 6. Добавляем гексагоны поверх регионов
    hexagonsData.forEach((hexagonData, index) => {
        const hexagonFeature = new ymaps3.YMapFeature({
            id: 'hexagon_' + index,
            source: 'hexagons-source',
            geometry: {
                type: 'Polygon',
                coordinates: hexagonData[0].coordinates
            },
            style: {
                stroke: [{
                    width: 1,
                    color: hexagonData[0].fillColor 
                }],
                fill: hexagonData[0].fillColor 
            },
            properties: {
                originalData: hexagonData[0],
                name: 'Гексагон ' + index,
                startDate: hexagonData[0].startDate,
                endDate: hexagonData[0].endDate,
                type: 'hexagon'
            }
        });
        
        map.addChild(hexagonFeature);
    });
    
    // Создаем элемент для tooltip
   const mapContainer = document.getElementById('regionMap');         
   const tooltip = document.getElementById('jsTooltip2');

   let isOverFeature = false;
   let currentFeatureData = null;

   // Функция для отображения tooltip
   function showTooltip(properties) {
    if (properties) {
       $('#jsTooltip2').html('Количество полётов: '+properties.totalFlights+'<br>Количество БПЛА: '+properties.totalBla+'<br>Период: '+properties.period).removeClass('hidden'); 
    }
   }

   // Функция для скрытия tooltip
   function hideTooltip() {
     $('#jsTooltip2').html('').addClass('hidden');
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
            // Если курсор проходит над объектом
            if (object && object.type === 'feature' && object.entity) {
                const properties = object.entity.properties;
                
                // Проверяем, что это гексагон
                if (properties && properties.type === 'hexagon') {
                    
                    const originalData = properties ? properties.originalData : (object.entity._props && object.entity._props.properties ? object.entity._props.properties.originalData : null);
                    if (originalData) {
                        
                        showTooltip(originalData.properties);
                        isOverFeature = true;
                        currentFeatureData = originalData;
                        return;
                    }
                }
            }
            
            // Если не гексагон или нет данных - скрываем tooltip
            hideTooltip();
            isOverFeature = false;
            currentFeatureData = null;
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