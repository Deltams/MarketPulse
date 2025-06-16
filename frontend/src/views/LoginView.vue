<template>
  <div class="login">
    <div class="login-container">
      <h1>Вход в систему</h1>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Имя пользователя</label>
          <input
            type="text"
            id="username"
            v-model="username"
            required
            class="form-input"
            :disabled="loading"
          />
        </div>
        
        <div class="form-group">
          <label for="password">Пароль</label>
          <input
            type="password"
            id="password"
            v-model="password"
            required
            class="form-input"
            :disabled="loading"
          />
        </div>

        <div v-if="authStore.error" class="error">
          {{ authStore.error }}
        </div>
        
        <button type="submit" class="submit-button" :disabled="loading">
          {{ loading ? 'Вход...' : 'Войти' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')

const loading = computed(() => authStore.loading)

const handleLogin = async () => {
  try {
    await authStore.login({
      username: username.value,
      password: password.value
    })
    router.push('/')
  } catch (error) {
    console.error('Login error:', error)
  }
}
</script>

<style scoped>
.login {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 200px);
  padding: 2rem;
}

.login-container {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h1 {
  color: #2c3e50;
  margin: 0 0 2rem 0;
  text-align: center;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  color: #2c3e50;
  font-weight: 500;
}

.form-input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: #3498db;
}

.form-input:disabled {
  background-color: #f8f9fa;
  cursor: not-allowed;
}

.submit-button {
  background-color: #2c3e50;
  color: white;
  border: none;
  padding: 0.75rem;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
}

.submit-button:hover:not(:disabled) {
  background-color: #34495e;
  transform: translateY(-1px);
}

.submit-button:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

.error {
  color: #dc3545;
  text-align: center;
  margin-top: 1rem;
  padding: 0.5rem;
  background-color: #f8d7da;
  border-radius: 4px;
}
</style>