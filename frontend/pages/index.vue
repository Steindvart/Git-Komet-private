<template>
  <div>
    <h1>Панель управления Git-Komet</h1>
    <p class="subtitle">Умный трекер разработки через анализ Git-метрик из T1 Сфера.Код</p>
    
    <div class="dashboard-grid">
      <div class="card">
        <h3>📊 Обзор</h3>
        <p>Анализируйте эффективность команды через метрики T1 Сфера.Код:</p>
        <ul class="feature-list">
          <li>✓ Оценка эффективности команд (0-100)</li>
          <li>✓ Отслеживание технического долга</li>
          <li>✓ Выявление узких мест</li>
          <li>✓ Забота о сотрудниках (переработки)</li>
          <li>✓ Алерты и рекомендации</li>
        </ul>
      </div>

      <div class="card">
        <h3>🎯 Быстрая статистика</h3>
        <div class="stats">
          <div class="stat-item">
            <span class="stat-label">Проекты</span>
            <span class="stat-value">{{ stats.projects }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Команды</span>
            <span class="stat-value">{{ stats.teams }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Средняя эффективность</span>
            <span class="stat-value">{{ stats.avgEffectiveness }}/100</span>
          </div>
        </div>
      </div>

      <div class="card">
        <h3>🚀 Быстрые действия</h3>
        <div class="actions">
          <NuxtLink to="/repositories" class="btn btn-primary">
            Управление проектами
          </NuxtLink>
          <NuxtLink to="/teams" class="btn btn-secondary">
            Управление командами
          </NuxtLink>
          <NuxtLink to="/metrics" class="btn btn-secondary">
            Просмотр аналитики
          </NuxtLink>
        </div>
      </div>

      <div class="card">
        <h3>🔍 Типы анализа</h3>
        <div class="analysis-types">
          <div class="analysis-item">
            <span class="analysis-icon">📊</span>
            <div class="analysis-info">
              <strong>Эффективность команды</strong>
              <p>Общая оценка производительности с трендами и алертами</p>
            </div>
          </div>
          <div class="analysis-item">
            <span class="analysis-icon">🔧</span>
            <div class="analysis-info">
              <strong>Технический долг</strong>
              <p>Покрытие тестами, рост TODO, качество ревью, code churn</p>
            </div>
          </div>
          <div class="analysis-item">
            <span class="analysis-icon">🚧</span>
            <div class="analysis-info">
              <strong>Узкие места</strong>
              <p>Выявление замедлений в workflow и рекомендации</p>
            </div>
          </div>
          <div class="analysis-item">
            <span class="analysis-icon">💼</span>
            <div class="analysis-info">
              <strong>Забота о сотрудниках</strong>
              <p>Отслеживание переработок и активности вне рабочего времени</p>
            </div>
          </div>
        </div>
      </div>

      <div class="card full-width">
        <h3>💡 Начало работы</h3>
        <div class="getting-started">
          <div class="step">
            <span class="step-number">1</span>
            <div class="step-content">
              <strong>Добавьте проект</strong>
              <p>Создайте проект из T1 Сфера.Код</p>
            </div>
          </div>
          <div class="step">
            <span class="step-number">2</span>
            <div class="step-content">
              <strong>Создайте команду</strong>
              <p>Настройте команду разработки и добавьте участников</p>
            </div>
          </div>
          <div class="step">
            <span class="step-number">3</span>
            <div class="step-content">
              <strong>Сгенерируйте демо-данные</strong>
              <p>Симулируйте данные T1 API (коммиты, PR, ревью, задачи)</p>
            </div>
          </div>
          <div class="step">
            <span class="step-number">4</span>
            <div class="step-content">
              <strong>Просмотрите аналитику</strong>
              <p>Изучайте метрики, тренды и рекомендации</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const stats = ref({
  projects: 0,
  teams: 0,
  avgEffectiveness: 0
})

onMounted(async () => {
  // В реальном приложении получаем данные из API
  // Пока используем заглушки
})
</script>

<style scoped>
.subtitle {
  color: var(--text-secondary);
  font-size: 1.125rem;
  margin-bottom: 2rem;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.full-width {
  grid-column: 1 / -1;
}

.stats {
  display: flex;
  gap: 2rem;
  margin-top: 1rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stat-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--accent-primary);
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1rem;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin-top: 1rem;
}

.feature-list li {
  padding: 0.5rem 0;
  color: var(--text-secondary);
}

.analysis-types {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1rem;
}

.analysis-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background-color: var(--bg-tertiary);
  border-radius: 0.5rem;
  border: 1px solid var(--border-primary);
}

.analysis-icon {
  font-size: 2rem;
}

.analysis-info strong {
  display: block;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.analysis-info p {
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin: 0;
}

.getting-started {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.step {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background-color: var(--bg-tertiary);
  border-radius: 0.5rem;
  border: 1px solid var(--border-primary);
}

.step-number {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background-color: var(--accent-secondary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  flex-shrink: 0;
}

.step-content strong {
  display: block;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.step-content p {
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin: 0;
}
</style>
