<template>
  <div class="dashboard">
    <header class="header">
      <h1>⚡ Git Komet</h1>
      <p class="subtitle">Система автооценки эффективности команд через анализ Git-метрик</p>
    </header>

    <main class="container">
      <!-- Controls -->
      <div class="controls">
        <button 
          @click="loadData" 
          :disabled="loading"
          class="btn btn-primary"
        >
          {{ loading ? 'Загрузка...' : 'Обновить данные' }}
        </button>
        <button 
          @click="generateMockDataAction" 
          :disabled="loading"
          class="btn btn-secondary"
        >
          Сгенерировать тестовые данные
        </button>
      </div>

      <!-- Error message -->
      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <!-- Project Selector -->
      <div v-if="projects && projects.length > 0" class="project-selector">
        <label for="project-select">Выберите проект:</label>
        <select 
          id="project-select"
          v-model="selectedProjectId" 
          @change="onProjectChange"
          class="select"
        >
          <option 
            v-for="project in projects" 
            :key="project.id" 
            :value="project.id"
          >
            {{ project.name }}
          </option>
        </select>
      </div>

      <!-- Analysis Results -->
      <div v-if="analysis" class="analysis-section">
        <h2>Анализ узких мест: {{ analysis.project_name }}</h2>
        
        <!-- Summary Cards -->
        <div class="metrics-grid">
          <div class="metric-card">
            <h3>Pull Requests</h3>
            <div class="metric-value">{{ analysis.total_prs }}</div>
            <p class="metric-label">Всего PR</p>
          </div>
          <div class="metric-card">
            <h3>Задачи</h3>
            <div class="metric-value">{{ analysis.total_issues }}</div>
            <p class="metric-label">Всего задач</p>
          </div>
        </div>

        <!-- PR Metrics Chart -->
        <div v-if="prChartData" class="chart-section">
          <h3>Метрики Pull Requests</h3>
          <BarChart :data="prChartData" />
          <div class="metric-details">
            <div v-if="analysis.avg_pr_review_time_hours !== null">
              <strong>Первое ревью:</strong> {{ analysis.avg_pr_review_time_hours.toFixed(1) }} часов
            </div>
            <div v-if="analysis.avg_pr_approval_time_hours !== null">
              <strong>Одобрение:</strong> {{ analysis.avg_pr_approval_time_hours.toFixed(1) }} часов
            </div>
            <div v-if="analysis.avg_pr_merge_time_hours !== null">
              <strong>Мердж:</strong> {{ analysis.avg_pr_merge_time_hours.toFixed(1) }} часов
            </div>
          </div>
        </div>

        <!-- Issue Metrics Chart -->
        <div v-if="issueChartData" class="chart-section">
          <h3>Метрики задач</h3>
          <BarChart :data="issueChartData" />
          <div class="metric-details">
            <div v-if="analysis.avg_issue_start_time_hours !== null">
              <strong>До начала работы:</strong> {{ analysis.avg_issue_start_time_hours.toFixed(1) }} часов
            </div>
            <div v-if="analysis.avg_issue_completion_time_hours !== null">
              <strong>Выполнение:</strong> {{ analysis.avg_issue_completion_time_hours.toFixed(1) }} часов
            </div>
          </div>
        </div>

        <!-- Bottlenecks -->
        <div v-if="analysis.bottlenecks && analysis.bottlenecks.length > 0" class="bottlenecks">
          <h3>🔴 Обнаруженные узкие места</h3>
          <ul>
            <li v-for="(bottleneck, index) in analysis.bottlenecks" :key="index">
              {{ bottleneck }}
            </li>
          </ul>
        </div>

        <!-- Recommendations -->
        <div v-if="analysis.recommendations && analysis.recommendations.length > 0" class="recommendations">
          <h3>💡 Рекомендации</h3>
          <ul>
            <li v-for="(recommendation, index) in analysis.recommendations" :key="index">
              {{ recommendation }}
            </li>
          </ul>
        </div>
      </div>

      <!-- TODO Section -->
      <div class="todo-section">
        <h2>🚀 Планируемые функции</h2>
        <ul>
          <li>Отслеживание TODO в коде и на ревью</li>
          <li>Индикаторы заботы о сотрудниках (активность вне рабочего времени, переработки)</li>
          <li>Тренды изменения качества кода (code churn, покрытие тестами)</li>
          <li>Общая оценка проекта и рекомендации по развитию</li>
          <li>Интеграция с Т1 Сфера.Код</li>
          <li>Метрики для команд и персональные метрики</li>
        </ul>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
const api = useApi()

const projects = ref<any[]>([])
const selectedProjectId = ref<number | null>(null)
const analysis = ref<any>(null)
const loading = ref(false)
const error = ref<string | null>(null)

const prChartData = computed(() => {
  if (!analysis.value) return null
  
  const labels: string[] = []
  const values: number[] = []
  
  if (analysis.value.avg_pr_review_time_hours !== null) {
    labels.push('До первого ревью')
    values.push(analysis.value.avg_pr_review_time_hours)
  }
  
  if (analysis.value.avg_pr_approval_time_hours !== null) {
    labels.push('До одобрения')
    values.push(analysis.value.avg_pr_approval_time_hours)
  }
  
  if (analysis.value.avg_pr_merge_time_hours !== null) {
    labels.push('До мерджа')
    values.push(analysis.value.avg_pr_merge_time_hours)
  }
  
  return labels.length > 0 ? { labels, values } : null
})

const issueChartData = computed(() => {
  if (!analysis.value) return null
  
  const labels: string[] = []
  const values: number[] = []
  
  if (analysis.value.avg_issue_start_time_hours !== null) {
    labels.push('До начала работы')
    values.push(analysis.value.avg_issue_start_time_hours)
  }
  
  if (analysis.value.avg_issue_completion_time_hours !== null) {
    labels.push('Время выполнения')
    values.push(analysis.value.avg_issue_completion_time_hours)
  }
  
  return labels.length > 0 ? { labels, values } : null
})

const loadProjects = async () => {
  try {
    projects.value = await api.fetchProjects()
    if (projects.value.length > 0 && !selectedProjectId.value) {
      selectedProjectId.value = projects.value[0].id
    }
  } catch (e) {
    error.value = 'Не удалось загрузить список проектов'
  }
}

const loadAnalysis = async () => {
  if (!selectedProjectId.value) return
  
  try {
    analysis.value = await api.fetchBottleneckAnalysis(selectedProjectId.value)
    error.value = null
  } catch (e) {
    error.value = 'Не удалось загрузить анализ'
  }
}

const loadData = async () => {
  loading.value = true
  error.value = null
  
  try {
    await loadProjects()
    if (selectedProjectId.value) {
      await loadAnalysis()
    }
  } finally {
    loading.value = false
  }
}

const onProjectChange = async () => {
  await loadAnalysis()
}

const generateMockDataAction = async () => {
  loading.value = true
  error.value = null
  
  try {
    await api.generateMockData()
    await loadData()
  } catch (e: any) {
    if (e.data?.note) {
      error.value = e.data.note
    } else {
      error.value = 'Не удалось сгенерировать тестовые данные'
    }
  } finally {
    loading.value = false
  }
}

// Load data on mount
onMounted(() => {
  loadData()
})
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.header {
  text-align: center;
  color: white;
  margin-bottom: 2rem;
}

.header h1 {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #5568d3;
}

.btn-secondary {
  background: #48bb78;
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background: #38a169;
}

.error-message {
  background: #fed7d7;
  color: #c53030;
  padding: 1rem;
  border-radius: 6px;
  margin-bottom: 1rem;
}

.project-selector {
  margin-bottom: 2rem;
}

.project-selector label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.select {
  width: 100%;
  max-width: 400px;
  padding: 0.75rem;
  border: 2px solid #e2e8f0;
  border-radius: 6px;
  font-size: 1rem;
}

.analysis-section h2 {
  color: #2d3748;
  margin-bottom: 1.5rem;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.metric-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
}

.metric-card h3 {
  font-size: 1rem;
  margin-bottom: 0.5rem;
  opacity: 0.9;
}

.metric-value {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.metric-label {
  font-size: 0.875rem;
  opacity: 0.8;
}

.chart-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #f7fafc;
  border-radius: 8px;
}

.chart-section h3 {
  color: #2d3748;
  margin-bottom: 1rem;
}

.metric-details {
  margin-top: 1rem;
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.metric-details div {
  font-size: 0.95rem;
  color: #4a5568;
}

.bottlenecks {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #fed7d7;
  border-left: 4px solid #e53e3e;
  border-radius: 6px;
}

.bottlenecks h3 {
  color: #c53030;
  margin-bottom: 1rem;
}

.bottlenecks ul {
  list-style: none;
  padding: 0;
}

.bottlenecks li {
  padding: 0.5rem 0;
  color: #742a2a;
}

.recommendations {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #c6f6d5;
  border-left: 4px solid #38a169;
  border-radius: 6px;
}

.recommendations h3 {
  color: #22543d;
  margin-bottom: 1rem;
}

.recommendations ul {
  list-style: none;
  padding: 0;
}

.recommendations li {
  padding: 0.5rem 0;
  color: #276749;
}

.todo-section {
  margin-top: 3rem;
  padding: 1.5rem;
  background: #edf2f7;
  border-radius: 8px;
}

.todo-section h2 {
  color: #2d3748;
  margin-bottom: 1rem;
}

.todo-section ul {
  color: #4a5568;
}

.todo-section li {
  margin-bottom: 0.5rem;
}
</style>
