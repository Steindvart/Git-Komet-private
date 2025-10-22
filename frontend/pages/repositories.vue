<template>
  <div>
    <h1>Проекты</h1>
    <p class="subtitle">Управление Git-репозиториями</p>

    <div v-if="error" class="error-message">
      {{ error }}
      <button @click="error = null" class="close-btn">×</button>
    </div>

    <div class="actions-bar">
      <button class="btn btn-primary" @click="showAddModal = true" :disabled="loading">
        + Добавить проект
      </button>
    </div>

    <div v-if="loading && projects.length === 0" class="loading-state">
      Загрузка...
    </div>

    <div v-else class="projects-list">
      <div v-if="projects.length === 0" class="empty-state">
        <p>Пока нет проектов. Добавьте ваш первый Git-репозиторий!</p>
      </div>
      
      <div v-else class="card-grid">
        <div v-for="project in projects" :key="project.id" class="card">
          <h3>{{ project.name }}</h3>
          <p class="project-id">ID: {{ project.external_id }}</p>
          <p v-if="project.description" class="project-description">{{ project.description }}</p>
          <div class="card-actions">
            <button class="btn btn-secondary" @click="generateMockData(project.id)" :disabled="loading">
              Сгенерировать демо-данные
            </button>
            <button class="btn" @click="deleteProject(project.id)" :disabled="loading">
              Удалить
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Project Modal -->
    <div v-if="showAddModal" class="modal">
      <div class="modal-content">
        <h2>Добавить проект</h2>
        <p class="modal-note">Добавьте Git-репозиторий для анализа</p>
        <form @submit.prevent="addProject">
          <div class="form-group">
            <label>Название</label>
            <input v-model="newProject.name" type="text" required :disabled="loading" />
          </div>
          <div class="form-group">
            <label>Внешний ID (ID проекта)</label>
            <input v-model="newProject.external_id" type="text" required :disabled="loading" />
          </div>
          <div class="form-group">
            <label>Описание</label>
            <textarea v-model="newProject.description" :disabled="loading"></textarea>
          </div>
          <div class="modal-actions">
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? 'Добавление...' : 'Добавить' }}
            </button>
            <button type="button" class="btn" @click="showAddModal = false" :disabled="loading">Отмена</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const api = useApi()
const showAddModal = ref(false)
const projects = ref([])
const teams = ref([])
const selectedTeamId = ref<number | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)
const newProject = ref({
  name: '',
  external_id: '',
  description: ''
})

// Load projects and teams on mount
onMounted(async () => {
  await loadProjects()
  await loadTeams()
})

const loadProjects = async () => {
  loading.value = true
  error.value = null
  try {
    projects.value = await api.fetchProjects()
  } catch (e: any) {
    error.value = 'Не удалось загрузить проекты: ' + e.message
  } finally {
    loading.value = false
  }
}

const loadTeams = async () => {
  try {
    teams.value = await api.fetchTeams()
    if (teams.value.length > 0) {
      selectedTeamId.value = teams.value[0].id
    }
  } catch (e: any) {
    console.error('Не удалось загрузить команды:', e)
  }
}

const addProject = async () => {
  loading.value = true
  error.value = null
  try {
    await api.createProject(newProject.value)
    showAddModal.value = false
    newProject.value = { name: '', external_id: '', description: '' }
    await loadProjects()
  } catch (e: any) {
    error.value = 'Не удалось создать проект: ' + e.message
  } finally {
    loading.value = false
  }
}

const generateMockData = async (id: number) => {
  if (!selectedTeamId.value) {
    alert('Сначала создайте команду на странице "Команды"')
    return
  }
  
  const confirmed = confirm('Генерация демо-данных создаст:\n- Коммиты с отслеживанием покрытия тестами\n- Pull Request с временем ревью\n- Ревью кода\n- Задачи с информацией об узких местах\n\nПродолжить?')
  if (!confirmed) return
  
  loading.value = true
  error.value = null
  try {
    const result = await api.generateMockData(id, selectedTeamId.value)
    alert(`Успешно создано:\n- ${result.commits_created} коммитов\n- ${result.pull_requests_created} pull requests\n- ${result.reviews_created} ревью\n- ${result.tasks_created} задач`)
  } catch (e: any) {
    error.value = 'Не удалось сгенерировать данные: ' + e.message
  } finally {
    loading.value = false
  }
}

const deleteProject = async (id: number) => {
  const confirmed = confirm('Вы уверены, что хотите удалить этот проект?')
  if (!confirmed) return
  
  loading.value = true
  error.value = null
  try {
    await api.deleteProject(id)
    await loadProjects()
  } catch (e: any) {
    error.value = 'Не удалось удалить проект: ' + e.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.subtitle {
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
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

.loading-state {
  text-align: center;
  padding: 3rem;
  color: var(--text-secondary);
  font-size: 1.125rem;
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
  color: var(--text-secondary);
  font-family: monospace;
  margin: 0.5rem 0;
}

.project-description {
  margin: 0.5rem 0;
  color: var(--text-secondary);
}

.card-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: var(--text-secondary);
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: var(--bg-secondary);
  border: 1px solid var(--border-primary);
  padding: 2rem;
  border-radius: 0.5rem;
  max-width: 500px;
  width: 90%;
}

.modal-note {
  color: var(--text-secondary);
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
  color: var(--text-primary);
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid var(--border-primary);
  border-radius: 0.375rem;
  background-color: var(--bg-primary);
  color: var(--text-primary);
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--accent-primary);
}

.form-group input:disabled,
.form-group textarea:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
