<script>
    const tables = [
      { name: 'aircraft_type', desc: 'Типы воздушных судов (B738, A320 и др.)' },
      { name: 'admin_boundaries', desc: 'Административные границы регионов и стран' },
      { name: 'aircraft', desc: 'Реестр воздушных судов с позывными и типами' },
      { name: 'grid_hexagon', desc: 'Гексагональная сетка для анализа покрытия' },
      { name: 'grid_square', desc: 'Квадратная сетка (альтернатива гексагонам)' },
      { name: 'points', desc: 'Точки наблюдения за воздушным движением' },
      { name: 'regions', desc: 'Регионы, зоны ответственности, сектора' },
      { name: 'processed_flights', desc: 'Обработанные полёты с траекториями' }
    ];

    // Render table cards
    function renderTableCards() {
      const container = document.querySelector('.tables-grid');
      container.innerHTML = '';
      tables.forEach(t => {
        const card = document.createElement('div');
        card.className = 'table-card';
        card.innerHTML = `
          <h4>${t.name}</h4>
          <div class="desc">${t.desc}</div>
          <div class="actions">
            <a href="https://aerometr.ru/api/api.php?table=${t.name}&limit=3" target="_blank">Посмотреть 3 записи</a>
            <a href="https://aerometr.ru/api/api.php?table=${t.name}&id=1" target="_blank">Запись id=1</a>
          </div>
        `;
        container.appendChild(card);
      });
    }

    // Try-it functions
    async function tryAll() {
      const table = document.getElementById('try-table-all').value;
      const page = document.getElementById('try-page').value;
      const limit = document.getElementById('try-limit').value;
      const url = `https://aerometr.ru/api/api.php?table=${encodeURIComponent(table)}&page=${page}&limit=${limit}`;
      
      const resp = document.getElementById('response-all');
      resp.style.display = 'block';
      resp.textContent = 'Загрузка...';
      
      try {
        const res = await fetch(url);
        const data = await res.json();
        resp.textContent = JSON.stringify(data, null, 2);
      } catch (e) {
        resp.textContent = `Ошибка: ${e.message}`;
      }
    }

    async function tryById() {
      const table = document.getElementById('try-table-id').value;
      const id = document.getElementById('try-id').value;
      const url = `https://aerometr.ru/api/api.php?table=${encodeURIComponent(table)}&id=${id}`;
      
      const resp = document.getElementById('response-id');
      resp.style.display = 'block';
      resp.textContent = 'Загрузка...';
      
      try {
        const res = await fetch(url);
        const data = await res.json();
        resp.textContent = JSON.stringify(data, null, 2);
      } catch (e) {
        resp.textContent = `Ошибка: ${e.message}`;
      }
    }

    // Инициализация
    renderTableCards();
</script>