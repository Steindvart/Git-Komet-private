<template>
  <div>
    <nav class="navbar">
      <div class="container">
        <div class="nav-content">
          <NuxtLink to="/" class="logo">
            <h2>Git-Komet</h2>
          </NuxtLink>
          <div class="nav-links">
            <NuxtLink to="/">Главная</NuxtLink>
            <NuxtLink to="/repositories">Проекты</NuxtLink>
            <NuxtLink to="/teams">Команды</NuxtLink>
            <NuxtLink to="/metrics">Аналитика</NuxtLink>
          </div>
        </div>
      </div>
    </nav>
    <main class="main-content">
      <div class="container">
        <slot />
      </div>
    </main>
    <footer class="footer">
      <div class="container">
        <p>&copy; 2024 Git-Komet. Система анализа эффективности команд разработки.</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.navbar {
  background-color: var(--bg-secondary);
  border-bottom: 1px solid var(--border-primary);
  padding: 1rem 0;
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  text-decoration: none;
  color: var(--text-primary);
}

.logo h2 {
  margin: 0;
  font-size: 1.5rem;
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-links a {
  text-decoration: none;
  color: var(--text-secondary);
  font-weight: 500;
  transition: color 0.2s;
}

.nav-links a:hover {
  color: var(--text-primary);
  text-decoration: none;
}

.main-content {
  min-height: calc(100vh - 200px);
  padding: 2rem 0;
}

.footer {
  background-color: var(--bg-secondary);
  border-top: 1px solid var(--border-primary);
  padding: 2rem 0;
  text-align: center;
  color: var(--text-secondary);
}
</style>
