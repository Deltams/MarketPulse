<template>
  <div class="app-layout">
    <header class="header">
      <nav class="nav">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/categories" class="nav-link">Categories</router-link>
        <router-link to="/brands" class="nav-link">Brands</router-link>
        <router-link to="/products" class="nav-link">Products</router-link>
        <router-link to="/about" class="nav-link">About</router-link>
        <div class="nav-right">
          <router-link to="/login" class="nav-link">Login</router-link>
          <router-link to="/profile" class="nav-link">Profile</router-link>
        </div>
      </nav>
    </header>

    <main class="main-content">
      <slot></slot>
    </main>

    <footer class="footer">
      <p>&copy; 2024 MarketPulse. All rights reserved.</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
// Component logic can be added here
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background-color: #2c3e50;
  padding: 1rem;
}

.nav {
  display: flex;
  align-items: center;
  gap: 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

.nav-right {
  margin-left: auto;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-link:hover {
  background-color: #34495e;
}

.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.footer {
  background-color: #2c3e50;
  color: white;
  text-align: center;
  padding: 1rem;
  margin-top: auto;
}
</style>