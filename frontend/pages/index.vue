<template>
  <div>
    <h1>Панель управления Git-Komet</h1>
    <p class="subtitle">Умный трекер разработки через анализ Git-метрик</p>
    
    <!-- Project Selector -->
    <div class="project-selector">
      <label for="project-select">Выберите проект для анализа:</label>
      <select 
        id="project-select" 
        v-model="selectedProjectId" 
        @change="onProjectChange"
        :disabled="loading"
      >
        <option :value="null">-- Выберите проект --</option>
        <option v-for="project in projects" :key="project.id" :value="project.id">
          {{ project.name }}
        </option>
      </select>
    </div>
    
    <div class="dashboard-grid">
      <div class="card stats-card" v-if="selectedProjectId && projectMetrics">
        <h3>🎯 Статистика проекта</h3>
        <div class="stats">
          <div class="stat-item">
            <span class="stat-label">Эффективность</span>
            <span class="stat-value">{{ projectMetrics.effectiveness_score }}/100</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Коммиты</span>
            <span class="stat-value">{{ projectMetrics.total_commits }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">PR</span>
            <span class="stat-value">{{ projectMetrics.total_prs }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Участники</span>
            <span class="stat-value">{{ projectMetrics.active_contributors }}</span>
          </div>
        </div>
        <div v-if="projectMetrics.has_alert" class="alert" :class="`alert-${projectMetrics.alert_severity}`">
          <strong>{{ projectMetrics.alert_severity === 'critical' ? '🚨' : '⚠️' }}</strong>
          {{ projectMetrics.alert_message }}
        </div>
      </div>
      
      <div class="card stats-card" v-else-if="!selectedProjectId">
        <h3>🎯 Начните работу</h3>
        <p>Выберите проект из списка выше для просмотра статистики и метрик</p>
        <p style="margin-top: 1rem; color: var(--text-secondary);">Всего проектов: {{ projects.length }}</p>
      </div>

      <div class="card actions-card">
        <h3>🚀 Быстрые действия</h3>
        <div class="actions">
          <NuxtLink to="/repositories" class="btn btn-primary">
            Управление проектами
          </NuxtLink>
          <NuxtLink :to="`/metrics?project=${selectedProjectId}`" class="btn btn-secondary" v-if="selectedProjectId">
            Детальная аналитика
          </NuxtLink>
        </div>
      </div>

      <div class="card full-width">
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
    </div>
  </div>
</template>

<script setup lang="ts">
const api = useApi()
const projects = ref([])
const selectedProjectId = ref<number | null>(null)
const projectMetrics = ref<any>(null)
const loading = ref(false)

onMounted(async () => {
  await loadProjects()
})

const loadProjects = async () => {
  loading.value = true
  try {
    projects.value = await api.fetchProjects()
    // Автоматически выбрать первый проект, если есть
    if (projects.value.length > 0) {
      selectedProjectId.value = projects.value[0].id
      await loadProjectMetrics()
    }
  } catch (error) {
    console.error('Error loading projects:', error)
  } finally {
    loading.value = false
  }
}

const onProjectChange = async () => {
  if (selectedProjectId.value) {
    await loadProjectMetrics()
  } else {
    projectMetrics.value = null
  }
}

const loadProjectMetrics = async () => {
  if (!selectedProjectId.value) return
  
  loading.value = true
  try {
    projectMetrics.value = await api.fetchProjectMetrics(selectedProjectId.value)
  } catch (error) {
    console.error('Error loading project metrics:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.subtitle {
  color: var(--text-secondary);
  font-size: 1.125rem;
  margin-bottom: 1.5rem;
}

.project-selector {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
  border-radius: 0.75rem;
  border: 1px solid var(--border-primary);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.project-selector label {
  display: block;
  margin-bottom: 0.75rem;
  font-weight: 600;
  font-size: 1.125rem;
  color: var(--text-primary);
}

.project-selector select {
  width: 100%;
  padding: 1rem;
  border: 2px solid var(--border-primary);
  border-radius: 0.5rem;
  background-color: var(--bg-primary);
  color: var(--text-primary);
  font-size: 1.125rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.project-selector select:hover:not(:disabled) {
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.1);
}

.project-selector select:focus {
  outline: none;
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 4px rgba(88, 166, 255, 0.2);
}

.project-selector select:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.alert {
  margin-top: 1rem;
  padding: 1rem;
  border-radius: 0.5rem;
}

.alert-warning {
  background-color: rgba(210, 153, 34, 0.15);
  border-left: 4px solid var(--warning);
  color: var(--text-primary);
}

.alert-critical {
  background-color: rgba(248, 81, 73, 0.15);
  border-left: 4px solid var(--danger);
  color: var(--text-primary);
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.5rem;
  margin-top: 2rem;
}

.full-width {
  grid-column: 1 / -1;
}

.stats-card {
  grid-column: 1;
}

.actions-card {
  grid-column: 2;
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem;
  background-color: var(--bg-tertiary);
  border-radius: 0.5rem;
  border: 1px solid var(--border-primary);
}

.stat-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--accent-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1rem;
}



.analysis-types {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
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


</style>
