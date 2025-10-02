<div class="layout-top-spacing">
 <div class="col-xxl-12 col-xl-12 col-lg-12 col-md-12 col-sm-12 mb-4">


                            <div class="single-post-content">

                                <div class="post-content">
    <header>
      <h1>✈️ Flight Data API</h1>
      <p>Интерактивная документация и explorer для разработчиков. Получайте данные о воздушном транспорте, границах, гексагонах и полётах в формате JSON.</p>
    </header>
    <!-- Документация -->
    <div class="" id="docs-view">
      <div class="col-xxl-12 col-xl-12 col-lg-12 col-md-12 layout-spacing" >
        <div class="widget widget-chart-two">
          <div class="widget-content widget-content-area">
            <div class="widget-heading">
              <h5 class="">Базовый URL</h5>
            </div>
            <p class="fs-6"><code>https://aerometr.ru/api/api.php</code></p>
          </div>
        </div>
      </div>

      <div class="col-xxl-12 col-xl-12 col-lg-12 col-md-12 layout-spacing" >
        <div class="widget widget-chart-two">
          <div class="widget-content widget-content-area">
            <h2 class="mb-4">Методы</h2>
            
            <div class="widget-heading">
              <h5 class="">1. Получить все записи из таблицы (с пагинацией)</h5>
            </div>
           
        <div class="row params">
          <div class="param">
            <div class="name">table <span class="badge badge-required">обязательный</span></div>
            <div>Имя таблицы из списка разрешённых</div>
          </div>
          <div class="param">
            <div class="name">page <span class="badge badge-optional">опциональный</span></div>
            <div>Номер страницы (по умолчанию: 1)</div>
          </div>
          <div class="param">
            <div class="name">limit <span class="badge badge-optional">опциональный</span></div>
            <div>Записей на страницу (1–1000, по умолчанию: 100)</div>
          </div>
        </div>

        <div class="row mb-5">
          <div class="col-md-4">
          <select id="try-table-all" class="form-select mb-3">
            <option value="aircraft">aircraft</option>
            <option value="regions">regions</option>
            <option value="points">points</option>
            <option value="processed_flights">processed_flights</option>
          </select>
          </div>
          <div class="col-md-4">
          <input type="number" id="try-page" value="1" min="1" class="form-control mb-3">
          </div>
          <div class="col-md-4">
          <input type="number" id="try-limit" value="5" min="1" max="1000" class="form-control mb-3">
          </div>
          <div class="col-md-4">
          <button class="btn btn-primary btn-lg" onclick="tryAll()">Выполнить запрос</button>
          </div>
        </div>
        <div id="response-all" class="response mb-5" style="display:none;"></div>
        
        <div class="widget-heading">
        <h5>2. Получить одну запись по ID</h5>
        </div>
        <div class="params">
          <div class="param">
            <div class="name">table <span class="badge badge-required">обязательный</span></div>
            <div>Имя таблицы</div>
          </div>
          <div class="param">
            <div class="name">id <span class="badge badge-required">обязательный</span></div>
            <div>Целое положительное число</div>
          </div>
        </div>

        <div class="row mb-4">
         <div class="col-md-4">
          <select id="try-table-id" class="form-select mb-3">
            <option value="aircraft">aircraft</option>
            <option value="regions">regions</option>
            <option value="admin_boundaries">admin_boundaries</option>
          </select>
         </div>
         <div class="col-md-4">
          <input type="number" id="try-id" value="1" min="1" class="form-control mb-3">
         </div>
         <div class="col-md-4">
          <button class="btn btn-primary btn-lg mb-3" onclick="tryById()">Выполнить запрос</button>
         </div>
        </div>
        <div id="response-id" class="response mb-5" style="display:none;"></div>
      </div>
      
          </div>
        </div>
      </div>

     <div class="col-xxl-12 col-xl-12 col-lg-12 col-md-12 layout-spacing" >
        <div class="widget widget-chart-two">
          <div class="widget-content widget-content-area">
          <div class="widget-heading">
          <h5>Разрешённые таблицы</h5>
          </div>
        <ul style="padding-left: 0; margin-top: 12px;">
          <li><code>aircraft_type</code> — типы воздушных судов</li>
          <li><code>admin_boundaries</code> — административные границы</li>
          <li><code>aircraft</code> — реестр воздушных судов</li>
          <li><code>grid_hexagon</code> — гексагональная сетка покрытия</li>
          <li><code>grid_square</code> — квадратная сетка (альтернатива гексагонам)</li>
          <li><code>points</code> — точки наблюдения за воздушным движением</li>
          <li><code>regions</code> — регионы, зоны ответственности, сектора</li>
          <li><code>processed_flights</code> — обработанные полёты с траекториями</li>
        </ul>
      </div>
     </div>
    </div>

      <div class="col-xxl-12 col-xl-12 col-lg-12 col-md-12 layout-spacing" >
        <div class="widget widget-chart-two">
          <div class="widget-content widget-content-area">
          <div class="widget-heading">
             <h5>Коды ответов</h5>
          </div>
        <ul style="padding-left: 0; margin-top: 12px;">
          <li><strong>200 OK</strong> — успешный запрос</li>
          <li><strong>400 Bad Request</strong> — неверные параметры</li>
          <li><strong>404 Not Found</strong> — запись не найдена</li>
          <li><strong>500 Internal Error</strong> — ошибка сервера</li>
        </ul>
      </div>
      </div>
      </div>

    <!-- Таблицы -->
   <div class="col-xxl-12 col-xl-12 col-lg-12 col-md-12 layout-spacing" >
        <div class="widget widget-chart-two">
          <div class="widget-content widget-content-area">
          <div class="widget-heading"><h5>Все таблицы</h5></div>
          <p>Кликните по таблице, чтобы увидеть примеры запросов и данные.</p>

        <div class="tables-grid">
          
        </div>
      </div>
    </div>
  </div>
  
  </div>
    </div>
  </div>
  
  
  </div>