<template>
  <div>
    <h1>Метрики и аналитика</h1>
    <p class="subtitle">Анализ эффективности команды на основе Git-метрик</p>

    <!-- Filters -->
    <div class="filters">
      <div class="filter-group">
        <label>Команда:</label>
        <select v-model="selectedTeamId" @change="loadMetrics">
          <option :value="null">Выберите команду</option>
          <option v-for="team in teams" :key="team.id" :value="team.id">{{ team.name }}</option>
        </select>
      </div>
      <div class="filter-group">
        <label>Проект (опционально):</label>
        <select v-model="selectedProjectId" @change="loadMetrics">
          <option :value="null">Все проекты</option>
          <option v-for="project in projects" :key="project.id" :value="project.id">{{ project.name }}</option>
        </select>
      </div>
      <div class="filter-group">
        <label>Период (дней):</label>
        <select v-model="periodDays" @change="loadMetrics">
          <option :value="7">7 дней</option>
          <option :value="30">30 дней</option>
          <option :value="90">90 дней</option>
        </select>
      </div>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
      <button @click="error = null" class="close-btn">×</button>
    </div>

    <div v-if="loading" class="loading-state">
      Загрузка метрик...
    </div>

    <div v-else-if="!selectedTeamId" class="empty-state">
      <p>Выберите команду для просмотра метрик</p>
    </div>

    <div v-else class="metrics-container">
      <!-- Team Effectiveness Score -->
      <div class="card full-width">
        <h3>📊 Оценка эффективности команды</h3>
        <p>Общий показатель производительности команды (0-100, аналогично SonarQube)</p>
        <div v-if="teamMetrics" class="score-display">
          <div class="score-circle">
            <span class="score-value">{{ Math.round(teamMetrics.effectiveness_score) }}</span>
            <span class="score-label">/100</span>
          </div>
          <div class="score-details">
            <div class="score-item">
              <span class="label">Тренд:</span>
              <span class="value">{{ teamMetrics.trend === 'stable' ? 'стабильно' : teamMetrics.trend }}</span>
            </div>
            <div class="score-item">
              <span class="label">Коммитов:</span>
              <span class="value">{{ teamMetrics.total_commits }}</span>
            </div>
            <div class="score-item">
              <span class="label">Pull Request:</span>
              <span class="value">{{ teamMetrics.total_prs }}</span>
            </div>
            <div class="score-item">
              <span class="label">Активные участники:</span>
              <span class="value">{{ teamMetrics.active_contributors }}</span>
            </div>
            <div class="score-item">
              <span class="label">Среднее время ревью:</span>
              <span class="value">{{ teamMetrics.avg_pr_review_time.toFixed(1) }}ч</span>
            </div>
          </div>
        </div>
        <div v-if="teamMetrics && teamMetrics.has_alert" class="alert" :class="`alert-${teamMetrics.alert_severity}`">
          <strong>{{ teamMetrics.alert_severity === 'critical' ? '🚨' : '⚠️' }}</strong>
          {{ teamMetrics.alert_message }}
        </div>
      </div>

      <!-- Work-Life Balance -->
      <div v-if="teamMetrics" class="card">
        <h3>💼 Забота о сотрудниках</h3>
        <p>Отслеживание переработок и активности вне рабочего времени</p>
        <div class="metric-group">
          <div class="metric-item">
            <span class="metric-label">Коммиты после рабочего времени</span>
            <span class="metric-value">{{ teamMetrics.after_hours_percentage.toFixed(1) }}% <span class="trend" :class="teamMetrics.after_hours_percentage > 30 ? 'up' : 'stable'">{{ teamMetrics.after_hours_percentage > 30 ? '↑' : '→' }}</span></span>
          </div>
          <div class="metric-item">
            <span class="metric-label">Коммиты в выходные</span>
            <span class="metric-value">{{ teamMetrics.weekend_percentage.toFixed(1) }}% <span class="trend" :class="teamMetrics.weekend_percentage > 20 ? 'up' : 'stable'">{{ teamMetrics.weekend_percentage > 20 ? '↑' : '→' }}</span></span>
          </div>
          <div class="metric-item">
            <span class="metric-label">Code Churn (переписывание)</span>
            <span class="metric-value">{{ teamMetrics.churn_rate.toFixed(1) }}% <span class="trend" :class="teamMetrics.churn_rate > 25 ? 'up' : 'stable'">{{ teamMetrics.churn_rate > 25 ? '↑' : '→' }}</span></span>
          </div>
        </div>
        <div v-if="teamMetrics.after_hours_percentage > 30 || teamMetrics.weekend_percentage > 20" class="alert alert-warning">
          <strong>⚠️</strong> Обнаружена высокая активность вне рабочего времени. Проверьте нагрузку на команду.
        </div>
      </div>

      <!-- Technical Debt Analysis -->
      <div v-if="technicalDebt" class="card">
        <h3>🔧 Анализ технического долга</h3>
        <div class="metric-group">
          <div class="metric-item">
            <span class="metric-label">Покрытие тестами</span>
            <div class="metric-bar">
              <div class="bar-fill" :style="{ width: technicalDebt.test_coverage + '%' }"></div>
            </div>
            <span class="metric-value">{{ technicalDebt.test_coverage.toFixed(1) }}% <span class="trend" :class="getTrendClass(technicalDebt.test_coverage_trend)">{{ getTrendArrow(technicalDebt.test_coverage_trend) }}</span></span>
          </div>
          <div class="metric-item">
            <span class="metric-label">TODO в коде</span>
            <span class="metric-value">{{ technicalDebt.todo_count_code }} <span class="trend" :class="getTrendClass(technicalDebt.todo_trend, true)">{{ getTrendArrow(technicalDebt.todo_trend, true) }}</span></span>
          </div>
          <div class="metric-item">
            <span class="metric-label">TODO в ревью</span>
            <span class="metric-value">{{ technicalDebt.todo_count_reviews }} <span class="trend" :class="getTrendClass(technicalDebt.todo_trend, true)">{{ getTrendArrow(technicalDebt.todo_trend, true) }}</span></span>
          </div>
          <div class="metric-item">
            <span class="metric-label">Code Churn (переписывание)</span>
            <span class="metric-value">{{ technicalDebt.churn_rate.toFixed(1) }}% <span class="trend" :class="technicalDebt.churn_rate > 25 ? 'up' : 'stable'">{{ technicalDebt.churn_rate > 25 ? '↑' : '→' }}</span></span>
          </div>
          <div class="metric-item">
            <span class="metric-label">Плотность комментариев в ревью</span>
            <span class="metric-value">{{ technicalDebt.review_comment_density.toFixed(1) }} на PR</span>
          </div>
          <div class="metric-item">
            <span class="metric-label">Оценка долга</span>
            <span class="metric-value debt-score">{{ technicalDebt.technical_debt_score.toFixed(0) }}/100</span>
          </div>
        </div>
        <div class="recommendations">
          <h4>💡 Рекомендации:</h4>
          <ul>
            <li v-for="rec in technicalDebt.recommendations" :key="rec">{{ rec }}</li>
          </ul>
        </div>
      </div>

      <!-- Bottleneck Analysis -->
      <div v-if="bottlenecks" class="card">
        <h3>🚧 Анализ узких мест</h3>
        <p>Этап workflow с самым долгим средним временем</p>
        <div class="bottleneck-info">
          <div class="bottleneck-stage">
            <span class="stage-icon">{{ getStageIcon(bottlenecks.bottleneck_stage) }}</span>
            <span class="stage-name">{{ getStageName(bottlenecks.bottleneck_stage) }}</span>
          </div>
          <div class="bottleneck-stats">
            <div class="stat">
              <span class="stat-label">Среднее время:</span>
              <span class="stat-value">{{ bottlenecks.avg_time_in_stage.toFixed(1) }} часов</span>
            </div>
            <div class="stat">
              <span class="stat-label">Затронутых задач:</span>
              <span class="stat-value">{{ bottlenecks.affected_tasks_count }}</span>
            </div>
            <div class="stat">
              <span class="stat-label">Оценка влияния:</span>
              <span class="stat-value" :class="getImpactClass(bottlenecks.impact_score)">{{ bottlenecks.impact_score.toFixed(0) }}/100</span>
            </div>
          </div>
        </div>
        <div v-if="bottlenecks.stage_breakdown" class="stage-breakdown">
          <h4>Распределение по этапам:</h4>
          <div v-for="(stage, key) in bottlenecks.stage_breakdown" :key="key" class="stage-item">
            <span class="stage-label">{{ getStageIcon(key) }} {{ getStageName(key) }}</span>
            <div class="stage-bar">
              <div class="bar-fill" :class="{ 'warning': key === bottlenecks.bottleneck_stage }" :style="{ width: getStageWidth(stage.avg_time, bottlenecks.stage_breakdown) + '%' }"></div>
            </div>
            <span class="stage-time">{{ stage.avg_time.toFixed(0) }}ч ({{ stage.count }})</span>
          </div>
        </div>
        <div class="recommendations">
          <h4>💡 Рекомендации:</h4>
          <ul>
            <li v-for="rec in bottlenecks.recommendations" :key="rec">{{ rec }}</li>
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

// State
const teams = ref([])
const projects = ref([])
const selectedTeamId = ref<number | null>(null)
const selectedProjectId = ref<number | null>(null)
const periodDays = ref(30)
const loading = ref(false)
const error = ref<string | null>(null)

// Metrics data
const teamMetrics = ref(null)
const technicalDebt = ref(null)
const bottlenecks = ref(null)

// Load teams and projects on mount
onMounted(async () => {
  await loadTeamsAndProjects()
})

const loadTeamsAndProjects = async () => {
  try {
    teams.value = await api.fetchTeams()
    projects.value = await api.fetchProjects()
    
    // Auto-select first team if available
    if (teams.value.length > 0) {
      selectedTeamId.value = teams.value[0].id
      await loadMetrics()
    }
  } catch (e: any) {
    error.value = 'Не удалось загрузить данные: ' + e.message
  }
}

const loadMetrics = async () => {
  if (!selectedTeamId.value) return
  
  loading.value = true
  error.value = null
  
  try {
    // Load all metrics in parallel
    const [effectiveness, debt, bottleneck] = await Promise.all([
      api.fetchTeamMetrics(selectedTeamId.value, periodDays.value, selectedProjectId.value),
      api.fetchTechnicalDebt(selectedTeamId.value, periodDays.value, selectedProjectId.value),
      api.fetchBottlenecks(selectedTeamId.value, periodDays.value, selectedProjectId.value)
    ])
    
    teamMetrics.value = effectiveness
    technicalDebt.value = debt
    bottlenecks.value = bottleneck
  } catch (e: any) {
    error.value = 'Не удалось загрузить метрики: ' + e.message
  } finally {
    loading.value = false
  }
}

// Helper functions for displaying data
const getTrendClass = (trend: string, inverted = false) => {
  if (inverted) {
    return trend === 'up' ? 'up' : trend === 'down' ? 'down' : 'stable'
  }
  return trend === 'up' ? 'down' : trend === 'down' ? 'up' : 'stable'
}

const getTrendArrow = (trend: string, inverted = false) => {
  if (inverted) {
    return trend === 'up' ? '↑' : trend === 'down' ? '↓' : '→'
  }
  return trend === 'up' ? '↓' : trend === 'down' ? '↑' : '→'
}

const getStageIcon = (stage: string) => {
  const icons = {
    'todo': '📋',
    'development': '💻',
    'review': '👁️',
    'testing': '🧪',
    'none': '✓'
  }
  return icons[stage] || '❓'
}

const getStageName = (stage: string) => {
  const names = {
    'todo': 'TODO',
    'development': 'Разработка',
    'review': 'Ревью',
    'testing': 'Тестирование',
    'none': 'Нет узких мест'
  }
  return names[stage] || stage
}

const getImpactClass = (score: number) => {
  if (score > 70) return 'impact-high'
  if (score > 40) return 'impact-medium'
  return 'impact-low'
}

const getStageWidth = (time: number, allStages: any) => {
  const maxTime = Math.max(...Object.values(allStages).map((s: any) => s.avg_time))
  return (time / maxTime) * 100
}
</script>

<style scoped>
.subtitle {
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
}

.filters {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: var(--bg-secondary);
  border: 1px solid var(--border-primary);
  border-radius: 0.5rem;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-width: 200px;
}

.filter-group label {
  font-weight: 500;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.filter-group select {
  padding: 0.5rem;
  border: 1px solid var(--border-primary);
  border-radius: 0.375rem;
  background-color: var(--bg-primary);
  color: var(--text-primary);
  cursor: pointer;
}

.filter-group select:focus {
  outline: none;
  border-color: var(--accent-primary);
}

.error-message {
  background-color: #fee;
  border: 1px solid #fcc;
  color: #c33;
  padding: 1rem;
  border-radius: 0.375rem;
  margin-bottom: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.error-message .close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #c33;
  padding: 0;
  width: 24px;
  height: 24px;
}

.loading-state,
.empty-state {
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

.impact-medium {
  color: var(--warning);
}

.impact-low {
  color: var(--success);
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
