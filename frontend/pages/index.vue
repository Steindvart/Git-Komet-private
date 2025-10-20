<template>
  <div>
    <h1>Git-Komet Dashboard</h1>
    <p class="subtitle">Team Effectiveness Analysis Through Git Metrics</p>
    
    <div class="dashboard-grid">
      <div class="card">
        <h3>📊 Overview</h3>
        <p>Welcome to Git-Komet, a system for analyzing team effectiveness through Git metrics.</p>
        <div class="stats">
          <div class="stat-item">
            <span class="stat-label">Repositories</span>
            <span class="stat-value">{{ stats.repositories }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Teams</span>
            <span class="stat-value">{{ stats.teams }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Total Commits</span>
            <span class="stat-value">{{ stats.commits }}</span>
          </div>
        </div>
      </div>

      <div class="card">
        <h3>🚀 Quick Actions</h3>
        <div class="actions">
          <NuxtLink to="/repositories" class="btn btn-primary">
            Manage Repositories
          </NuxtLink>
          <NuxtLink to="/teams" class="btn btn-secondary">
            Manage Teams
          </NuxtLink>
          <NuxtLink to="/metrics" class="btn btn-secondary">
            View Metrics
          </NuxtLink>
        </div>
      </div>

      <div class="card">
        <h3>📈 Recent Activity</h3>
        <p>Track recent commits and team activities across all repositories.</p>
        <ul class="activity-list">
          <li>System ready for data collection</li>
          <li>Configure repositories to start analysis</li>
          <li>Add teams and team members</li>
        </ul>
      </div>

      <div class="card">
        <h3>ℹ️ Features</h3>
        <ul class="feature-list">
          <li>✓ Git repository analysis</li>
          <li>✓ Team effectiveness metrics</li>
          <li>✓ Commit frequency tracking</li>
          <li>✓ Code churn analysis</li>
          <li>✓ Contributor statistics</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const stats = ref({
  repositories: 0,
  teams: 0,
  commits: 0
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

.activity-list,
.feature-list {
  list-style: none;
  padding: 0;
  margin-top: 1rem;
}

.activity-list li,
.feature-list li {
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--border-color);
}

.activity-list li:last-child,
.feature-list li:last-child {
  border-bottom: none;
}
</style>
