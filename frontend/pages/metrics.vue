<template>
  <div>
    <h1>Metrics & Analytics</h1>
    <p class="subtitle">Team effectiveness and repository metrics</p>

    <div class="metrics-container">
      <div class="card">
        <h3>Team Effectiveness</h3>
        <p>Analyze team performance through Git metrics</p>
        <div class="chart-placeholder">
          <p>📊 Chart visualization will appear here</p>
          <p class="note">Charts will be rendered using Chart.js/vue-chartjs</p>
        </div>
      </div>

      <div class="card">
        <h3>Commit Frequency</h3>
        <div class="chart-placeholder">
          <p>📈 Commit frequency over time</p>
        </div>
      </div>

      <div class="card">
        <h3>Code Churn</h3>
        <div class="chart-placeholder">
          <p>📉 Lines added/deleted over time</p>
        </div>
      </div>

      <div class="card">
        <h3>Contributor Activity</h3>
        <div class="chart-placeholder">
          <p>👥 Active contributors per team</p>
        </div>
      </div>

      <div class="card full-width">
        <h3>Key Metrics Summary</h3>
        <div class="metrics-grid">
          <div class="metric-item">
            <span class="metric-label">Total Commits (30d)</span>
            <span class="metric-value">0</span>
          </div>
          <div class="metric-item">
            <span class="metric-label">Active Contributors</span>
            <span class="metric-value">0</span>
          </div>
          <div class="metric-item">
            <span class="metric-label">Avg Commit Size</span>
            <span class="metric-value">0</span>
          </div>
          <div class="metric-item">
            <span class="metric-label">Commit Frequency</span>
            <span class="metric-value">0/day</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// In a real implementation, this would fetch data from the API
// and render charts using Chart.js via vue-chartjs
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

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  margin-top: 1rem;
}

.metric-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.metric-label {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
}

.metric-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary-color);
}
</style>
