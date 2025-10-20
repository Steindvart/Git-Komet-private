<template>
  <div>
    <h1>Проекты</h1>
    <p class="subtitle">Управление Git-репозиториями</p>

    <div class="actions-bar">
      <button class="btn btn-primary" @click="showAddModal = true">
        + Добавить проект
      </button>
    </div>

    <div class="projects-list">
      <div v-if="projects.length === 0" class="empty-state">
        <p>Пока нет проектов. Добавьте ваш первый Git-репозиторий!</p>
      </div>
      
      <div v-else class="card-grid">
        <div v-for="project in projects" :key="project.id" class="card">
          <h3>{{ project.name }}</h3>
          <p class="project-id">ID: {{ project.external_id }}</p>
          <p v-if="project.description" class="project-description">{{ project.description }}</p>
          <div class="card-actions">
            <button class="btn btn-secondary" @click="generateMockData(project.id)">
              Сгенерировать демо-данные
            </button>
            <button class="btn" @click="deleteProject(project.id)">
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
            <input v-model="newProject.name" type="text" required />
          </div>
          <div class="form-group">
            <label>Внешний ID (ID проекта)</label>
            <input v-model="newProject.external_id" type="text" required />
          </div>
          <div class="form-group">
            <label>Описание</label>
            <textarea v-model="newProject.description"></textarea>
          </div>
          <div class="modal-actions">
            <button type="submit" class="btn btn-primary">Добавить</button>
            <button type="button" class="btn" @click="showAddModal = false">Отмена</button>
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
  console.log('Добавление проекта:', newProject.value)
  showAddModal.value = false
  newProject.value = { name: '', external_id: '', description: '' }
}

const generateMockData = async (id: number) => {
  // API call: POST /api/v1/projects/{id}/generate-mock-data?team_id=1
  console.log('Генерация демо-данных T1 для проекта:', id)
  alert('Генерация демо-данных создаст:\n- Коммиты с отслеживанием покрытия тестами\n- Pull Request с временем ревью\n- Ревью кода\n- Задачи с информацией об узких местах')
}

const deleteProject = async (id: number) => {
  console.log('Удаление проекта:', id)
}
</script>

<style scoped>
.subtitle {
  color: var(--text-secondary);
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
