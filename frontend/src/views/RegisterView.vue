<template>
  <v-container class="d-flex justify-center">
    <v-card class="register-card" elevation="2" hover>
      <div class="register-header">
        <h1 class="text-h4 font-weight-bold mb-2">Создать аккаунт</h1>
        <p class="text-subtitle-1 text-medium-emphasis">Присоединяйтесь к нашему сообществу</p>
      </div>

      <v-form ref="form" @submit.prevent="handleSubmit" class="register-form">
        <v-row>
          <v-col cols="12">
            <v-text-field
              v-model="formData.name"
              placeholder="Имя пользователя"
              :rules="[
                v => !!v || 'Обязательное поле',
                v => v.length >= 3 || 'Минимум 3 символа'
              ]"
              variant="outlined"
              density="comfortable"
              class="rounded-lg custom-field"
              prepend-inner-icon="mdi-account"
              hide-details="auto"
            />
          </v-col>

          <v-col cols="12">
            <v-text-field
              v-model="formData.email"
              placeholder="Email"
              type="email"
              :rules="[
                v => !!v || 'Обязательное поле',
                v => /.+@.+\..+/.test(v) || 'Некорректный email'
              ]"
              variant="outlined"
              density="comfortable"
              class="rounded-lg custom-field"
              prepend-inner-icon="mdi-email"
              hide-details="auto"
            />
          </v-col>

          <v-col cols="12">
            <v-text-field
              v-model="formData.password"
              placeholder="Пароль"
              :type="showPassword ? 'text' : 'password'"
              :rules="[
                v => !!v || 'Обязательное поле',
                v => v.length >= 6 || 'Минимум 6 символов'
              ]"
              variant="outlined"
              density="comfortable"
              class="rounded-lg custom-field"
              prepend-inner-icon="mdi-lock"
              :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
              @click:append-inner="showPassword = !showPassword"
              hide-details="auto"
            />
          </v-col>

          <v-col cols="12">
            <v-text-field
              v-model="formData.confirmPassword"
              placeholder="Подтвердите пароль"
              :type="showConfirmPassword ? 'text' : 'password'"
              :rules="[
                v => !!v || 'Обязательное поле',
                v => v === formData.password || 'Пароли не совпадают'
              ]"
              variant="outlined"
              density="comfortable"
              class="rounded-lg custom-field"
              prepend-inner-icon="mdi-lock-check"
              :append-inner-icon="showConfirmPassword ? 'mdi-eye-off' : 'mdi-eye'"
              @click:append-inner="showConfirmPassword = !showConfirmPassword"
              hide-details="auto"
            />
          </v-col>

          <v-col cols="12">
            <v-card class="role-selector pa-4" variant="outlined">
              <div class="text-subtitle-1 font-weight-medium mb-2">Выберите тип аккаунта</div>
              <v-radio-group v-model="formData.role" inline hide-details>
                <v-radio
                  value="buyer"
                  color="primary"
                  class="role-radio"
                >
                  <template v-slot:label>
                    <div class="d-flex align-center">
                      <v-icon icon="mdi-cart" class="mr-2" />
                      <span>Покупатель</span>
                    </div>
                  </template>
                </v-radio>
                <v-radio
                  value="seller"
                  color="primary"
                  class="role-radio"
                >
                  <template v-slot:label>
                    <div class="d-flex align-center">
                      <v-icon icon="mdi-store" class="mr-2" />
                      <span>Продавец</span>
                    </div>
                  </template>
                </v-radio>
              </v-radio-group>
            </v-card>
          </v-col>

          <v-col cols="12">
            <v-btn
              color="primary"
              type="submit"
              block
              size="large"
              :loading="loading"
              class="register-button"
            >
              Создать аккаунт
            </v-btn>
          </v-col>

          <v-col cols="12" class="text-center">
            <span class="account-hint text-body-2">Уже есть аккаунт?</span>
            <router-link to="/login" class="text-decoration-none ml-2 login-link">
              Войти
            </router-link>
          </v-col>
        </v-row>
      </v-form>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const form = ref()
const loading = ref(false)
const showPassword = ref(false)
const showConfirmPassword = ref(false)

const formData = ref({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
  role: 'buyer' as 'buyer' | 'seller'
})

const handleSubmit = async () => {
  const { valid } = await form.value.validate()
  if (!valid) return

  loading.value = true
  try {
    const userData = {
      username: formData.value.name,
      email: formData.value.email,
      password: formData.value.password,
      is_seller: formData.value.role === 'seller',
      is_buyer: formData.value.role === 'buyer'
    }
    await authStore.register(userData)
    const redirectPath = route.query.redirect as string || '/'
    router.push(redirectPath)
  } catch (error) {
    if (error.response?.data) {
      const errors = error.response.data
      console.error('Registration error:', errors)
      console.error('Registration error:', error);
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-card,
:deep(.v-container) {
  cursor: default !important;
  margin-top: 0 !important;
}

.register-card {
  max-width: 500px;
  width: 100%;
  border-radius: 16px;
  padding: 2rem;
  background: #fff !important;
  box-shadow: 0 4px 16px rgba(0,0,0,0.10), 0 1.5px 4px rgba(0,0,0,0.08);
  border: 2px solid transparent;
  /* margin-top: 24px; */
}

.register-header {
  text-align: center;
  margin-bottom: 1rem;
}

.register-header h1 {
  color: #222;
  font-weight: 700;
  letter-spacing: 0.01em;
}

.register-header p {
  color: #6b7280;
  font-weight: 500;
  letter-spacing: 0.02em;
}

.register-form {
  margin-top: 0.5rem;
}

.role-selector {
  border-radius: 12px;
  background: #f8f9fa;
}

.role-selector:hover {
  background: #f8f9fa;
  box-shadow: none;
}

.role-selector .text-subtitle-1 {
  color: #222;
  font-weight: 600;
  letter-spacing: 0.01em;
}

.role-radio {
  margin-right: 2rem;
}

.role-radio :deep(.v-label) {
  color: #222 !important;
  font-weight: 500;
}

.register-button {
  background: linear-gradient(90deg, #1976d2 0%, #42a5f5 100%);
  color: #fff !important;
  font-weight: 700;
  font-size: 1.1rem;
  height: 48px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.08);
  transition: background 0.2s, box-shadow 0.2s;
  text-transform: none;
  letter-spacing: 0.5px;
}

.register-button:hover {
  background: linear-gradient(90deg, #1565c0 0%, #1e88e5 100%);
  box-shadow: 0 4px 16px rgba(25, 118, 210, 0.16);
}

.login-link {
  color: #1976d2;
  font-weight: 600;
  transition: color 0.2s;
}

.login-link:hover {
  color: #1565c0;
}

:deep(.custom-field) {
  background: #fff;
}

:deep(.custom-field:hover) {
  background: #fff;
}

:deep(.v-field) {
  border: 2px solid #1976d2 !important;
  border-radius: 8px;
  box-shadow: none !important;
  background: #fff;
}

:deep(.v-field--focused) {
  border-color: #1976d2;
  box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.1);
}

:deep(.v-field__input) {
  padding-top: 12px;
  padding-bottom: 12px;
  color: #222 !important;
  font-weight: 500;
}

:deep(.v-label) {
  color: #6b7280 !important;
  font-weight: 500;
  letter-spacing: 0.02em;
}

:deep(.v-messages__message) {
  color: #6b7280;
}

:deep(.v-icon) {
  color: #6b7280;
  opacity: 0.8;
}

:deep(.v-field--focused .v-icon) {
  color: #1976d2;
}

:deep(.v-field--focused .v-label) {
  color: #1976d2 !important;
}

:deep(.v-field--error) {
  border: none !important;
}

:deep(.v-field__outline),
:deep(.v-field__overlay) {
  border: none !important;
  box-shadow: none !important;
}

.account-hint {
  color: #1976d2;
  font-weight: 600;
}

:deep(.v-col) {
  margin-bottom: 0.5rem !important;
  padding-top: 0 !important;
  padding-bottom: 0 !important;
}

:deep(.v-container) {
  padding-top: 0 !important;
  padding-bottom: 0 !important;
}

:deep(.pa-4) {
  padding-top: 0 !important;
}
</style> 