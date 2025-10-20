<template>
  <div>
    <h1>Metrics & Analytics</h1>
    <p class="subtitle">Team effectiveness analysis from T1 Сфера.Код</p>

    <div class="metrics-container">
      <!-- Team Effectiveness Score -->
      <div class="card full-width">
        <h3>📊 Team Effectiveness Score</h3>
        <p>Overall team performance indicator (0-100, similar to SonarQube)</p>
        <div class="score-display">
          <div class="score-circle">
            <span class="score-value">{{ effectivenessScore }}</span>
            <span class="score-label">/100</span>
          </div>
          <div class="score-details">
            <div class="score-item">
              <span class="label">Trend:</span>
              <span class="value">{{ trend }}</span>
            </div>
            <div class="score-item">
              <span class="label">Active Contributors:</span>
              <span class="value">{{ activeContributors }}</span>
            </div>
            <div class="score-item">
              <span class="label">Avg Review Time:</span>
              <span class="value">{{ avgReviewTime }}h</span>
            </div>
          </div>
        </div>
        <div v-if="hasAlert" class="alert" :class="`alert-${alertSeverity}`">
          <strong>{{ alertSeverity === 'critical' ? '🚨' : '⚠️' }}</strong>
          {{ alertMessage }}
        </div>
      </div>

      <!-- Technical Debt Analysis -->
      <div class="card">
        <h3>🔧 Technical Debt Analysis</h3>
        <div class="metric-group">
          <div class="metric-item">
            <span class="metric-label">Test Coverage</span>
            <div class="metric-bar">
              <div class="bar-fill" :style="{ width: '65%' }"></div>
            </div>
            <span class="metric-value">65% <span class="trend up">↑</span></span>
          </div>
          <div class="metric-item">
            <span class="metric-label">TODO Count</span>
            <span class="metric-value">42 <span class="trend stable">→</span></span>
          </div>
          <div class="metric-item">
            <span class="metric-label">Review Comment Density</span>
            <span class="metric-value">3.2 per PR <span class="trend down">↓</span></span>
          </div>
          <div class="metric-item">
            <span class="metric-label">Debt Score</span>
            <span class="metric-value debt-score">72/100</span>
          </div>
        </div>
        <div class="recommendations">
          <h4>💡 Recommendations:</h4>
          <ul>
            <li>Test coverage is improving - keep it up!</li>
            <li>TODO count is stable - schedule time to address technical debt</li>
          </ul>
        </div>
      </div>

      <!-- Bottleneck Analysis -->
      <div class="card">
        <h3>🚧 Bottleneck Analysis</h3>
        <p>Workflow stage with longest average time</p>
        <div class="bottleneck-info">
          <div class="bottleneck-stage">
            <span class="stage-icon">🔍</span>
            <span class="stage-name">Code Review</span>
          </div>
          <div class="bottleneck-stats">
            <div class="stat">
              <span class="stat-label">Avg Time:</span>
              <span class="stat-value">48.5 hours</span>
            </div>
            <div class="stat">
              <span class="stat-label">Affected Tasks:</span>
              <span class="stat-value">15</span>
            </div>
            <div class="stat">
              <span class="stat-label">Impact Score:</span>
              <span class="stat-value impact-high">68/100</span>
            </div>
          </div>
        </div>
        <div class="stage-breakdown">
          <h4>Stage Breakdown:</h4>
          <div class="stage-item">
            <span class="stage-label">📋 TODO</span>
            <div class="stage-bar">
              <div class="bar-fill" style="width: 20%"></div>
            </div>
            <span class="stage-time">12h</span>
          </div>
          <div class="stage-item">
            <span class="stage-label">💻 Development</span>
            <div class="stage-bar">
              <div class="bar-fill" style="width: 45%"></div>
            </div>
            <span class="stage-time">28h</span>
          </div>
          <div class="stage-item">
            <span class="stage-label">👁️ Review</span>
            <div class="stage-bar">
              <div class="bar-fill warning" style="width: 80%"></div>
            </div>
            <span class="stage-time">48h</span>
          </div>
          <div class="stage-item">
            <span class="stage-label">🧪 Testing</span>
            <div class="stage-bar">
              <div class="bar-fill" style="width: 25%"></div>
            </div>
            <span class="stage-time">15h</span>
          </div>
        </div>
        <div class="recommendations">
          <h4>💡 Recommendations:</h4>
          <ul>
            <li>⚠️ Code review is taking over 2 days on average</li>
            <li>Consider: increasing reviewer capacity or setting review SLAs</li>
          </ul>
        </div>
      </div>

      <!-- Trend Charts Placeholder -->
      <div class="card full-width">
        <h3>📈 Trends Over Time</h3>
        <div class="chart-placeholder">
          <p>📊 Historical trend visualization</p>
          <p class="note">Charts showing effectiveness score, technical debt, and bottlenecks over time</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Mock data - in real app, fetch from API
const effectivenessScore = ref(72)
const trend = ref('improving')
const activeContributors = ref(8)
const avgReviewTime = ref(24.5)
const hasAlert = ref(true)
const alertSeverity = ref('warning')
const alertMessage = ref('Team effectiveness could be improved. Consider process optimization.')

// In real implementation, fetch from:
// GET /api/v1/metrics/team/{id}/effectiveness
// GET /api/v1/metrics/team/{id}/technical-debt
// GET /api/v1/metrics/team/{id}/bottlenecks
</script>

<style scoped>
.subtitle {
  color: #6b7280;
  margin-bottom: 1.5rem;
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
  background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%);
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
  border-bottom: 1px solid #e5e7eb;
}

.score-item .label {
  font-weight: 500;
  color: #6b7280;
}

.score-item .value {
  font-weight: 600;
  color: #111827;
}

.alert {
  padding: 1rem;
  border-radius: 0.5rem;
  margin-top: 1rem;
}

.alert-warning {
  background-color: #fef3c7;
  border-left: 4px solid #f59e0b;
  color: #92400e;
}

.alert-critical {
  background-color: #fee2e2;
  border-left: 4px solid #ef4444;
  color: #991b1b;
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
  color: #4b5563;
}

.metric-value {
  font-weight: 600;
  color: #111827;
}

.debt-score {
  color: #4f46e5;
  font-size: 1.125rem;
}

.metric-bar {
  flex: 2;
  height: 8px;
  background-color: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #4f46e5 0%, #06b6d4 100%);
  transition: width 0.3s ease;
}

.bar-fill.warning {
  background: linear-gradient(90deg, #f59e0b 0%, #ef4444 100%);
}

.trend {
  margin-left: 0.5rem;
  font-size: 0.875rem;
}

.trend.up {
  color: #10b981;
}

.trend.down {
  color: #ef4444;
}

.trend.stable {
  color: #6b7280;
}

.bottleneck-info {
  margin: 1rem 0;
}

.bottleneck-stage {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background-color: #fef3c7;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}

.stage-icon {
  font-size: 2rem;
}

.stage-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: #92400e;
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
  color: #6b7280;
}

.stat-value {
  font-weight: 600;
  font-size: 1.125rem;
  color: #111827;
}

.impact-high {
  color: #ef4444;
}

.stage-breakdown {
  margin: 1.5rem 0;
}

.stage-breakdown h4 {
  margin-bottom: 1rem;
  font-size: 1rem;
  color: #4b5563;
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
  color: #4b5563;
}

.stage-bar {
  flex: 1;
  height: 8px;
  background-color: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}

.stage-time {
  min-width: 50px;
  text-align: right;
  font-weight: 600;
  color: #111827;
}

.recommendations {
  margin-top: 1.5rem;
  padding: 1rem;
  background-color: #f9fafb;
  border-radius: 0.5rem;
}

.recommendations h4 {
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #4b5563;
}

.recommendations ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.recommendations li {
  padding: 0.5rem 0;
  color: #6b7280;
  font-size: 0.875rem;
}

.chart-placeholder {
  background: #f9fafb;
  border: 2px dashed var(--border-color);
  border-radius: 0.5rem;
  padding: 3rem;
  text-align: center;
  margin-top: 1rem;
  color: #6b7280;
}

.note {
  font-size: 0.875rem;
  margin-top: 0.5rem;
}
</style>
