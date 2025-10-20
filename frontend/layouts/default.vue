<template>
  <div>
    <nav class="navbar">
      <div class="container">
        <div class="nav-content">
          <NuxtLink to="/" class="logo">
            <h2>Git-Komet</h2>
          </NuxtLink>
          <div class="nav-links">
            <NuxtLink to="/">Dashboard</NuxtLink>
            <NuxtLink to="/repositories">Repositories</NuxtLink>
            <NuxtLink to="/teams">Teams</NuxtLink>
            <NuxtLink to="/metrics">Metrics</NuxtLink>
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
        <p>&copy; 2024 Git-Komet. Team Effectiveness Analysis System.</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.navbar {
  background-color: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 1rem 0;
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  text-decoration: none;
  color: var(--primary-color);
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
  color: var(--text-color);
  font-weight: 500;
  transition: color 0.2s;
}

.nav-links a:hover {
  color: var(--primary-color);
}

.main-content {
  min-height: calc(100vh - 200px);
  padding: 2rem 0;
}

.footer {
  background-color: white;
  border-top: 1px solid var(--border-color);
  padding: 2rem 0;
  text-align: center;
  color: #6b7280;
}
</style>
