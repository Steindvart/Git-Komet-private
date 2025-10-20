<template>
  <div>
    <h1>Repositories</h1>
    <p class="subtitle">Manage your Git repositories for analysis</p>

    <div class="actions-bar">
      <button class="btn btn-primary" @click="showAddModal = true">
        + Add Repository
      </button>
    </div>

    <div class="repositories-list">
      <div v-if="repositories.length === 0" class="empty-state">
        <p>No repositories yet. Add your first repository to start analyzing!</p>
      </div>
      
      <div v-else class="card-grid">
        <div v-for="repo in repositories" :key="repo.id" class="card">
          <h3>{{ repo.name }}</h3>
          <p class="repo-url">{{ repo.url }}</p>
          <p v-if="repo.description" class="repo-description">{{ repo.description }}</p>
          <div class="card-actions">
            <button class="btn btn-secondary" @click="syncRepository(repo.id)">
              Sync Commits
            </button>
            <button class="btn" @click="deleteRepository(repo.id)">
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Repository Modal (simplified) -->
    <div v-if="showAddModal" class="modal">
      <div class="modal-content">
        <h2>Add Repository</h2>
        <form @submit.prevent="addRepository">
          <div class="form-group">
            <label>Name</label>
            <input v-model="newRepo.name" type="text" required />
          </div>
          <div class="form-group">
            <label>URL</label>
            <input v-model="newRepo.url" type="text" required />
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea v-model="newRepo.description"></textarea>
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
const config = useRuntimeConfig()
const showAddModal = ref(false)
const repositories = ref([])
const newRepo = ref({
  name: '',
  url: '',
  description: ''
})

const addRepository = async () => {
  // API call would go here
  console.log('Adding repository:', newRepo.value)
  showAddModal.value = false
  newRepo.value = { name: '', url: '', description: '' }
}

const syncRepository = async (id: number) => {
  console.log('Syncing repository:', id)
}

const deleteRepository = async (id: number) => {
  console.log('Deleting repository:', id)
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

.repo-url {
  font-size: 0.875rem;
  color: #6b7280;
  font-family: monospace;
  margin: 0.5rem 0;
}

.repo-description {
  margin: 0.5rem 0;
  color: #4b5563;
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
