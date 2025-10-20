<template>
  <div>
    <h1>Teams</h1>
    <p class="subtitle">Manage your development teams</p>

    <div class="actions-bar">
      <button class="btn btn-primary" @click="showAddModal = true">
        + Add Team
      </button>
    </div>

    <div class="teams-list">
      <div v-if="teams.length === 0" class="empty-state">
        <p>No teams yet. Create your first team to start tracking effectiveness!</p>
      </div>
      
      <div v-else class="card-grid">
        <div v-for="team in teams" :key="team.id" class="card">
          <h3>{{ team.name }}</h3>
          <p v-if="team.description" class="team-description">{{ team.description }}</p>
          <div class="team-stats">
            <span class="stat">👥 {{ team.members?.length || 0 }} members</span>
          </div>
          <div class="card-actions">
            <NuxtLink :to="`/teams/${team.id}`" class="btn btn-secondary">
              View Details
            </NuxtLink>
            <button class="btn" @click="deleteTeam(team.id)">
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Team Modal -->
    <div v-if="showAddModal" class="modal">
      <div class="modal-content">
        <h2>Add Team</h2>
        <form @submit.prevent="addTeam">
          <div class="form-group">
            <label>Team Name</label>
            <input v-model="newTeam.name" type="text" required />
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea v-model="newTeam.description"></textarea>
          </div>
          <div class="modal-actions">
            <button type="submit" class="btn btn-primary">Add</button>
            <button type="button" class="btn" @click="showAddModal = false">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const showAddModal = ref(false)
const teams = ref([])
const newTeam = ref({
  name: '',
  description: ''
})

const addTeam = async () => {
  console.log('Adding team:', newTeam.value)
  showAddModal.value = false
  newTeam.value = { name: '', description: '' }
}

const deleteTeam = async (id: number) => {
  console.log('Deleting team:', id)
}
</script>

<style scoped>
.subtitle {
  color: #6b7280;
  margin-bottom: 1.5rem;
}

.actions-bar {
  margin-bottom: 2rem;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.team-description {
  margin: 0.5rem 0;
  color: #4b5563;
}

.team-stats {
  margin: 1rem 0;
  color: #6b7280;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #6b7280;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 0.5rem;
  max-width: 500px;
  width: 90%;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: 0.375rem;
}

.form-group textarea {
  min-height: 100px;
  resize: vertical;
}

.modal-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1.5rem;
}
</style>
