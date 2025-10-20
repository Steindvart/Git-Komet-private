<template>
  <div>
    <h1>Projects</h1>
    <p class="subtitle">Projects from T1 Сфера.Код</p>

    <div class="actions-bar">
      <button class="btn btn-primary" @click="showAddModal = true">
        + Add Project
      </button>
    </div>

    <div class="projects-list">
      <div v-if="projects.length === 0" class="empty-state">
        <p>No projects yet. Add your first project from T1 Сфера.Код!</p>
      </div>
      
      <div v-else class="card-grid">
        <div v-for="project in projects" :key="project.id" class="card">
          <h3>{{ project.name }}</h3>
          <p class="project-id">ID: {{ project.external_id }}</p>
          <p v-if="project.description" class="project-description">{{ project.description }}</p>
          <div class="card-actions">
            <button class="btn btn-secondary" @click="generateMockData(project.id)">
              Generate Mock Data
            </button>
            <button class="btn" @click="deleteProject(project.id)">
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Project Modal -->
    <div v-if="showAddModal" class="modal">
      <div class="modal-content">
        <h2>Add Project</h2>
        <p class="modal-note">Add a project from T1 Сфера.Код</p>
        <form @submit.prevent="addProject">
          <div class="form-group">
            <label>Name</label>
            <input v-model="newProject.name" type="text" required />
          </div>
          <div class="form-group">
            <label>External ID (T1 Project ID)</label>
            <input v-model="newProject.external_id" type="text" required />
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea v-model="newProject.description"></textarea>
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
const projects = ref([])
const newProject = ref({
  name: '',
  external_id: '',
  description: ''
})

const addProject = async () => {
  // API call: POST /api/v1/projects
  console.log('Adding project:', newProject.value)
  showAddModal.value = false
  newProject.value = { name: '', external_id: '', description: '' }
}

const generateMockData = async (id: number) => {
  // API call: POST /api/v1/projects/{id}/generate-mock-data?team_id=1
  console.log('Generating mock T1 data for project:', id)
  alert('Mock data generation would create:\n- Commits with test coverage tracking\n- Pull requests with review times\n- Code reviews\n- Tasks with bottleneck information')
}

const deleteProject = async (id: number) => {
  console.log('Deleting project:', id)
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

.project-id {
  font-size: 0.875rem;
  color: #6b7280;
  font-family: monospace;
  margin: 0.5rem 0;
}

.project-description {
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

.modal-note {
  color: #6b7280;
  font-size: 0.875rem;
  margin-bottom: 1rem;
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
