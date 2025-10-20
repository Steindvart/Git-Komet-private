<template>
  <div>
    <h1>Git-Komet Dashboard</h1>
    <p class="subtitle">Team Effectiveness Analysis Through T1 Сфера.Код Metrics</p>
    
    <div class="dashboard-grid">
      <div class="card">
        <h3>📊 Overview</h3>
        <p>Analyze team effectiveness through T1 Сфера.Код metrics:</p>
        <ul class="feature-list">
          <li>✓ Team effectiveness scores (0-100)</li>
          <li>✓ Technical debt tracking</li>
          <li>✓ Bottleneck identification</li>
          <li>✓ Alerts and recommendations</li>
        </ul>
      </div>

      <div class="card">
        <h3>🎯 Quick Stats</h3>
        <div class="stats">
          <div class="stat-item">
            <span class="stat-label">Projects</span>
            <span class="stat-value">{{ stats.projects }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Teams</span>
            <span class="stat-value">{{ stats.teams }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Avg Effectiveness</span>
            <span class="stat-value">{{ stats.avgEffectiveness }}/100</span>
          </div>
        </div>
      </div>

      <div class="card">
        <h3>🚀 Quick Actions</h3>
        <div class="actions">
          <NuxtLink to="/repositories" class="btn btn-primary">
            Manage Projects
          </NuxtLink>
          <NuxtLink to="/teams" class="btn btn-secondary">
            Manage Teams
          </NuxtLink>
          <NuxtLink to="/metrics" class="btn btn-secondary">
            View Analytics
          </NuxtLink>
        </div>
      </div>

      <div class="card">
        <h3>🔍 Analysis Types</h3>
        <div class="analysis-types">
          <div class="analysis-item">
            <span class="analysis-icon">📊</span>
            <div class="analysis-info">
              <strong>Team Effectiveness</strong>
              <p>Overall performance score with trends and alerts</p>
            </div>
          </div>
          <div class="analysis-item">
            <span class="analysis-icon">🔧</span>
            <div class="analysis-info">
              <strong>Technical Debt</strong>
              <p>Test coverage, TODO growth, review quality</p>
            </div>
          </div>
          <div class="analysis-item">
            <span class="analysis-icon">🚧</span>
            <div class="analysis-info">
              <strong>Bottlenecks</strong>
              <p>Identify workflow slowdowns and get recommendations</p>
            </div>
          </div>
        </div>
      </div>

      <div class="card full-width">
        <h3>💡 Getting Started</h3>
        <div class="getting-started">
          <div class="step">
            <span class="step-number">1</span>
            <div class="step-content">
              <strong>Add a Project</strong>
              <p>Create a project from T1 Сфера.Код</p>
            </div>
          </div>
          <div class="step">
            <span class="step-number">2</span>
            <div class="step-content">
              <strong>Create a Team</strong>
              <p>Set up your development team and add members</p>
            </div>
          </div>
          <div class="step">
            <span class="step-number">3</span>
            <div class="step-content">
              <strong>Generate Mock Data</strong>
              <p>Simulate T1 API data (commits, PRs, reviews, tasks)</p>
            </div>
          </div>
          <div class="step">
            <span class="step-number">4</span>
            <div class="step-content">
              <strong>View Analytics</strong>
              <p>Explore metrics, trends, and recommendations</p>
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
  // In a real application, fetch these from the API
  // For now, using placeholder data
})
</script>

<style scoped>
.subtitle {
  color: #6b7280;
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
  color: #6b7280;
  font-weight: 500;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary-color);
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
  color: #4b5563;
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
  background-color: #f9fafb;
  border-radius: 0.5rem;
}

.analysis-icon {
  font-size: 2rem;
}

.analysis-info strong {
  display: block;
  color: #111827;
  margin-bottom: 0.25rem;
}

.analysis-info p {
  color: #6b7280;
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
  background-color: #f9fafb;
  border-radius: 0.5rem;
}

.step-number {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background-color: var(--primary-color);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  flex-shrink: 0;
}

.step-content strong {
  display: block;
  color: #111827;
  margin-bottom: 0.25rem;
}

.step-content p {
  color: #6b7280;
  font-size: 0.875rem;
  margin: 0;
}
</style>
