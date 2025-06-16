<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center" class="fill-height">
      <v-col cols="12" sm="8" md="6" lg="5" xl="4">
        <v-card class="elevation-12 login-card mx-auto">
          <v-card-title class="text-h5 text-center pt-6">
            Вход в систему
          </v-card-title>

          <v-card-text>
            <BaseForm
              ref="form"
              :loading="loading"
              submit-text="Войти"
              @submit="handleSubmit"
              @cancel="$router.push('/register')"
            >
              <BaseInput
                v-model="formData.email"
                label="Email"
                type="email"
                :rules="[
                  v => !!v || 'Обязательное поле',
                  v => /.+@.+\..+/.test(v) || 'Некорректный email'
                ]"
                prepend-icon="mdi-email"
              />

              <BaseInput
                v-model="formData.password"
                label="Пароль"
                type="password"
                :rules="[v => !!v || 'Обязательное поле']"
                prepend-icon="mdi-lock"
              />
            </BaseForm>
          </v-card-text>

          <v-card-text class="text-center">
            <p class="text-body-2">
              Нет аккаунта?
              <router-link to="/register" class="text-decoration-none">
                Зарегистрироваться
              </router-link>
            </p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import BaseForm from '../components/common/BaseForm.vue'
import BaseInput from '../components/common/BaseInput.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const form = ref()
const loading = ref(false)

const formData = ref({
  email: '',
  password: ''
})

const handleSubmit = async () => {
  const { valid } = await form.value.validate()
  if (!valid) return

  loading.value = true
  try {
    await authStore.login(formData.value.email, formData.value.password)
    const redirectPath = route.query.redirect as string || '/'
    router.push(redirectPath)
  } catch (error: any) {
    console.error('Login failed:', error)
    // Здесь можно добавить обработку ошибок
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-card {
  max-width: 480px;
  width: 100%;
  margin: 48px auto;
  padding: 32px 24px 24px 24px;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
}

@media (max-width: 600px) {
  .login-card {
    padding: 20px 8px 16px 8px;
    margin: 24px auto;
    max-width: 98vw;
  }
}

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