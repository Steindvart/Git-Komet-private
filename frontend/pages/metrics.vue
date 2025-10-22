<template>
  <div>
    <h1>Метрики и аналитика</h1>
    <p class="subtitle">Анализ эффективности проекта на основе Git-метрик</p>

    <!-- Project Selector -->
    <div class="project-selector">
      <label for="project-select">Проект:</label>
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

    <div v-if="!selectedProjectId" class="empty-state">
      <p>Выберите проект для просмотра метрик и аналитики</p>
    </div>

    <div v-else-if="loading" class="loading-state">
      Загрузка метрик...
    </div>

    <div v-else class="metrics-container">
      <!-- Team Effectiveness Score -->
      <div class="card full-width">
        <h3>📊 Оценка эффективности команды</h3>
        <p>Общий показатель производительности команды (0-100, аналогично SonarQube)</p>
        <div class="score-display">
          <div class="score-circle">
            <span class="score-value">{{ effectivenessScore }}</span>
            <span class="score-label">/100</span>
          </div>
          <div class="score-details">
            <div class="score-item">
              <span class="label">Тренд:</span>
              <span class="value">улучшение</span>
            </div>
            <div class="score-item">
              <span class="label">Активные участники:</span>
              <span class="value">{{ activeContributors }}</span>
            </div>
            <div class="score-item">
              <span class="label">Среднее время ревью:</span>
              <span class="value">{{ avgReviewTime }}ч</span>
            </div>
          </div>
        </div>
        <div v-if="hasAlert" class="alert" :class="`alert-${alertSeverity}`">
          <strong>{{ alertSeverity === 'critical' ? '🚨' : '⚠️' }}</strong>
          {{ alertMessage }}
        </div>
      </div>

      <!-- Work-Life Balance -->
      <div class="card">
        <h3>💼 Забота о сотрудниках</h3>
        <p>Отслеживание переработок и активности вне рабочего времени</p>
        <div class="metric-group">
          <div class="metric-item">
            <span class="metric-label">Коммиты после рабочего времени</span>
            <span class="metric-value">{{ afterHoursPercentage }}% <span class="trend" :class="afterHoursPercentage > 30 ? 'up' : 'stable'">{{ afterHoursPercentage > 30 ? '↑' : '→' }}</span></span>
          </div>
          <div class="metric-item">
            <span class="metric-label">Коммиты в выходные</span>
            <span class="metric-value">{{ weekendPercentage }}% <span class="trend" :class="weekendPercentage > 20 ? 'up' : 'stable'">{{ weekendPercentage > 20 ? '↑' : '→' }}</span></span>
          </div>
          <div class="metric-item">
            <span class="metric-label">Пики активности</span>
            <span class="metric-value">{{ peakHours }}</span>
          </div>
        </div>
        <div v-if="afterHoursPercentage > 30 || weekendPercentage > 20" class="alert alert-warning">
          <strong>⚠️</strong> Обнаружена высокая активность вне рабочего времени. Проверьте нагрузку на команду.
        </div>
      </div>

      <!-- Technical Debt Analysis -->
      <div class="card">
        <h3>🔧 Анализ технического долга</h3>
        <div class="metric-group">
          <div class="metric-item">
            <span class="metric-label">Покрытие тестами</span>
            <div class="metric-bar">
              <div class="bar-fill" :style="{ width: '67%' }"></div>
            </div>
            <span class="metric-value">67% <span class="trend up">↑</span></span>
          </div>
          <div class="metric-item">
            <span class="metric-label">TODO в коде</span>
            <span class="metric-value">{{ todoInCode }} <span class="trend stable">→</span></span>
          </div>
          <div class="metric-item">
            <span class="metric-label">TODO в ревью</span>
            <span class="metric-value">{{ todoInReviews }} <span class="trend up">↑</span></span>
          </div>
          <div class="metric-item">
            <span class="metric-label">Code Churn (переписывание)</span>
            <span class="metric-value">{{ churnRate }}% <span class="trend" :class="churnRate > 25 ? 'up' : 'stable'">{{ churnRate > 25 ? '↑' : '→' }}</span></span>
          </div>
          <div class="metric-item">
            <span class="metric-label">Плотность комментариев в ревью</span>
            <span class="metric-value">{{ reviewCommentDensity }} на PR <span class="trend down">↓</span></span>
          </div>
          <div class="metric-item">
            <span class="metric-label">Оценка долга</span>
            <span class="metric-value debt-score">{{ debtScore }}/100</span>
          </div>
        </div>
        <div class="recommendations">
          <h4>💡 Рекомендации:</h4>
          <ul>
            <li>Покрытие тестами улучшается - продолжайте в том же духе!</li>
            <li>TODO в ревью растут - рассмотрите оформление их в отдельные тикеты</li>
            <li v-if="churnRate > 25">⚠️ Высокий уровень переписывания кода - проверьте качество планирования</li>
          </ul>
        </div>
      </div>

      <!-- Bottleneck Analysis -->
      <div class="card">
        <h3>🚧 Анализ узких мест</h3>
        <p>Этап workflow с самым долгим средним временем</p>
        <div class="bottleneck-info" v-if="bottleneckStage !== 'none'">
          <div class="bottleneck-stage">
            <span class="stage-icon">🔍</span>
            <span class="stage-name">{{ getStageDisplayName(bottleneckStage) }}</span>
          </div>
          <div class="bottleneck-stats">
            <div class="stat">
              <span class="stat-label">Среднее время:</span>
              <span class="stat-value">{{ bottleneckTime.toFixed(1) }} часов</span>
            </div>
          </div>
        </div>
        <div v-else class="bottleneck-info">
          <p>✓ Нет явных узких мест в workflow</p>
        </div>
        <div class="stage-breakdown">
          <h4>Распределение по этапам:</h4>
          <div class="stage-item">
            <span class="stage-label">📋 TODO</span>
            <div class="stage-bar">
              <div class="bar-fill" style="width: 20%"></div>
            </div>
            <span class="stage-time">12ч</span>
          </div>
          <div class="stage-item">
            <span class="stage-label">💻 Разработка</span>
            <div class="stage-bar">
              <div class="bar-fill" style="width: 45%"></div>
            </div>
            <span class="stage-time">28ч</span>
          </div>
          <div class="stage-item">
            <span class="stage-label">👁️ Ревью</span>
            <div class="stage-bar">
              <div class="bar-fill warning" style="width: 80%"></div>
            </div>
            <span class="stage-time">48ч</span>
          </div>
          <div class="stage-item">
            <span class="stage-label">🧪 Тестирование</span>
            <div class="stage-bar">
              <div class="bar-fill" style="width: 25%"></div>
            </div>
            <span class="stage-time">15ч</span>
          </div>
        </div>
        <div class="recommendations">
          <h4>💡 Рекомендации:</h4>
          <ul>
            <li>⚠️ Ревью кода занимает более 2 дней в среднем</li>
            <li>Рассмотрите: увеличение мощности ревьюеров или установку SLA для ревью</li>
          </ul>
        </div>
      </div>

      <!-- Trend Charts Placeholder -->
      <div class="card full-width">
        <h3>📈 Тренды во времени</h3>
        <div class="chart-placeholder">
          <p>📊 Визуализация исторических трендов</p>
          <p class="note">Графики, показывающие эффективность, технический долг и узкие места во времени</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const api = useApi()
const projects = ref([])
const selectedProjectId = ref<number | null>(null)
const loading = ref(false)

// Metrics data
const effectivenessScore = ref(0)
const activeContributors = ref(0)
const avgReviewTime = ref(0)
const hasAlert = ref(false)
const alertSeverity = ref('')
const alertMessage = ref('')

// Work-life balance metrics
const afterHoursPercentage = ref(0)
const weekendPercentage = ref(0)
const peakHours = ref('--:--')

// Technical debt metrics
const todoInCode = ref(0)
const todoInReviews = ref(0)
const churnRate = ref(0)
const reviewCommentDensity = ref(0)
const debtScore = ref(0)

// Bottleneck data
const bottleneckStage = ref('none')
const bottleneckTime = ref(0)

onMounted(async () => {
  await loadProjects()
})

const loadProjects = async () => {
  loading.value = true
  try {
    projects.value = await api.fetchProjects()
    if (projects.value.length > 0) {
      selectedProjectId.value = projects.value[0].id
      await loadAllMetrics()
    }
  } catch (error) {
    console.error('Error loading projects:', error)
  } finally {
    loading.value = false
  }
}

const onProjectChange = async () => {
  if (selectedProjectId.value) {
    await loadAllMetrics()
  }
}

const loadAllMetrics = async () => {
  if (!selectedProjectId.value) return
  
  loading.value = true
  try {
    // Load effectiveness metrics
    const effectiveness = await api.fetchProjectMetrics(selectedProjectId.value)
    effectivenessScore.value = Math.round(effectiveness.effectiveness_score)
    activeContributors.value = effectiveness.active_contributors
    avgReviewTime.value = effectiveness.avg_pr_review_time
    hasAlert.value = effectiveness.has_alert
    alertSeverity.value = effectiveness.alert_severity || 'info'
    alertMessage.value = effectiveness.alert_message || ''
    afterHoursPercentage.value = Math.round(effectiveness.after_hours_percentage)
    weekendPercentage.value = Math.round(effectiveness.weekend_percentage)
    churnRate.value = Math.round(effectiveness.churn_rate)
    
    // Load technical debt
    const debt = await api.fetchProjectTechnicalDebt(selectedProjectId.value)
    todoInCode.value = debt.todo_count
    todoInReviews.value = debt.todo_in_reviews || 0
    reviewCommentDensity.value = debt.review_comment_density
    debtScore.value = Math.round(debt.technical_debt_score)
    
    // Load bottlenecks
    const bottleneck = await api.fetchProjectBottlenecks(selectedProjectId.value)
    bottleneckStage.value = bottleneck.bottleneck_stage
    bottleneckTime.value = bottleneck.avg_time_in_stage
    
  } catch (error) {
    console.error('Error loading metrics:', error)
  } finally {
    loading.value = false
  }
}

const getStageDisplayName = (stage: string) => {
  const names: Record<string, string> = {
    'todo': 'TODO (ожидание начала)',
    'development': 'Разработка',
    'review': 'Ревью кода',
    'testing': 'Тестирование',
    'none': 'Нет узких мест'
  }
  return names[stage] || stage
}
</script>

<style scoped>
.subtitle {
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
}

.project-selector {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background-color: var(--bg-secondary);
  border-radius: 0.5rem;
  border: 1px solid var(--border-primary);
}

.project-selector label {
  display: block;
  margin-bottom: 0.75rem;
  font-weight: 600;
  color: var(--text-primary);
}

.project-selector select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-primary);
  border-radius: 0.375rem;
  background-color: var(--bg-primary);
  color: var(--text-primary);
  font-size: 1rem;
  cursor: pointer;
}

.project-selector select:focus {
  outline: none;
  border-color: var(--accent-primary);
}

.project-selector select:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: var(--text-secondary);
  background-color: var(--bg-secondary);
  border-radius: 0.5rem;
  border: 1px solid var(--border-primary);
}

.loading-state {
  text-align: center;
  padding: 3rem;
  color: var(--text-secondary);
  font-size: 1.125rem;
}

.metrics-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
}

.full-width {
  grid-column: 1 / -1;
}

.score-display {
  display: flex;
  gap: 2rem;
  align-items: center;
  margin: 1.5rem 0;
}

.score-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent-secondary) 0%, var(--accent-primary) 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
}

.score-value {
  font-size: 2.5rem;
  font-weight: 700;
}

.score-label {
  font-size: 1rem;
  opacity: 0.9;
}

.score-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.score-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--border-primary);
}

.score-item .label {
  font-weight: 500;
  color: var(--text-secondary);
}

.score-item .value {
  font-weight: 600;
  color: var(--text-primary);
}

.alert {
  padding: 1rem;
  border-radius: 0.5rem;
  margin-top: 1rem;
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

.metric-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin: 1rem 0;
}

.metric-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.metric-label {
  flex: 1;
  font-weight: 500;
  color: var(--text-secondary);
}

.metric-value {
  font-weight: 600;
  color: var(--text-primary);
}

.debt-score {
  color: var(--accent-primary);
  font-size: 1.125rem;
}

.metric-bar {
  flex: 2;
  height: 8px;
  background-color: var(--bg-tertiary);
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--accent-secondary) 0%, var(--accent-primary) 100%);
  transition: width 0.3s ease;
}

.bar-fill.warning {
  background: linear-gradient(90deg, var(--warning) 0%, var(--danger) 100%);
}

.trend {
  margin-left: 0.5rem;
  font-size: 0.875rem;
}

.trend.up {
  color: var(--danger);
}

.trend.down {
  color: var(--success);
}

.trend.stable {
  color: var(--text-secondary);
}

.bottleneck-info {
  margin: 1rem 0;
}

.bottleneck-stage {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background-color: rgba(210, 153, 34, 0.15);
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  border: 1px solid rgba(210, 153, 34, 0.3);
}

.stage-icon {
  font-size: 2rem;
}

.stage-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
}

.bottleneck-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1rem;
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.stat-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.stat-value {
  font-weight: 600;
  font-size: 1.125rem;
  color: var(--text-primary);
}

.impact-high {
  color: var(--danger);
}

.stage-breakdown {
  margin: 1.5rem 0;
}

.stage-breakdown h4 {
  margin-bottom: 1rem;
  font-size: 1rem;
  color: var(--text-secondary);
}

.stage-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.stage-label {
  min-width: 120px;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.stage-bar {
  flex: 1;
  height: 8px;
  background-color: var(--bg-tertiary);
  border-radius: 4px;
  overflow: hidden;
}

.stage-time {
  min-width: 50px;
  text-align: right;
  font-weight: 600;
  color: var(--text-primary);
}

.recommendations {
  margin-top: 1.5rem;
  padding: 1rem;
  background-color: var(--bg-tertiary);
  border-radius: 0.5rem;
  border: 1px solid var(--border-primary);
}

.recommendations h4 {
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.recommendations ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.recommendations li {
  padding: 0.5rem 0;
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.chart-placeholder {
  background: var(--bg-tertiary);
  border: 2px dashed var(--border-primary);
  border-radius: 0.5rem;
  padding: 3rem;
  text-align: center;
  margin-top: 1rem;
  color: var(--text-secondary);
}

.note {
  font-size: 0.875rem;
  margin-top: 0.5rem;
}
</style>
