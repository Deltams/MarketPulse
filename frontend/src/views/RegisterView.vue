<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="14" class="d-flex justify-center">
        <v-card class="elevation-14 registration-card">
          <v-card-title class="text-h5 text-center pt-6">
            Регистрация
          </v-card-title>

          <v-card-text>
            <BaseForm
              ref="form"
              :loading="loading"
              submit-text="Зарегистрироваться"
              @submit="handleSubmit"
              @cancel="$router.push('/login')"
            >
              <BaseInput
                v-model="formData.name"
                label="Имя"
                :rules="[
                  v => !!v || 'Обязательное поле',
                  v => v.length >= 3 || 'Минимум 3 символа',
                  v => /^[a-zA-Z0-9_]+$/.test(v) || 'Только буквы, цифры и подчеркивание'
                ]"
                :error-messages="formErrors.name"
                prepend-icon="mdi-account"
              />

              <BaseInput
                v-model="formData.email"
                label="Email"
                type="email"
                :rules="[
                  v => !!v || 'Обязательное поле',
                  v => /.+@.+\..+/.test(v) || 'Некорректный email'
                ]"
                :error-messages="formErrors.email"
                prepend-icon="mdi-email"
              />

              <BaseInput
                v-model="formData.password"
                label="Пароль"
                type="password"
                :rules="[
                  v => !!v || 'Обязательное поле',
                  v => v.length >= 8 || 'Минимум 8 символов',
                  v => /[A-Z]/.test(v) || 'Минимум одна заглавная буква',
                  v => /[a-z]/.test(v) || 'Минимум одна строчная буква',
                  v => /[0-9]/.test(v) || 'Минимум одна цифра'
                ]"
                :error-messages="formErrors.password"
                prepend-icon="mdi-lock"
              />

              <BaseInput
                v-model="formData.confirmPassword"
                label="Подтверждение пароля"
                type="password"
                :rules="[
                  v => !!v || 'Обязательное поле',
                  v => v === formData.password || 'Пароли не совпадают'
                ]"
                :error-messages="formErrors.confirmPassword"
                prepend-icon="mdi-lock-check"
              />

              <v-radio-group
                v-model="formData.role"
                label="Тип аккаунта"
                inline
                class="mt-4"
              >
                <v-radio
                  label="Покупатель"
                  value="buyer"
                ></v-radio>
                <v-radio
                  label="Продавец"
                  value="seller"
                ></v-radio>
              </v-radio-group>
            </BaseForm>
          </v-card-text>

          <v-card-text class="text-center">
            <p class="text-body-2">
              Уже есть аккаунт?
              <router-link to="/login" class="text-decoration-none">
                Войти
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
const formErrors = ref({
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const formData = ref({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
  role: 'buyer' as 'buyer' | 'seller'
})

const handleSubmit = async () => {
  // Reset form errors
  formErrors.value = {
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  }

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
    console.log('Sending registration data:', userData)
    
    await authStore.register(userData)

    const redirectPath = route.query.redirect as string || '/'
    router.push(redirectPath)
  } catch (error: any) {
    console.error('Registration failed:', error)
    if (error.response?.data) {
      console.log('Error response data:', error.response.data)
      // Show validation errors from the backend
      const errors = error.response.data
      // Map backend field names to frontend field names
      if (errors.username) formErrors.value.name = errors.username[0]
      if (errors.email) formErrors.value.email = errors.email[0]
      if (errors.password) formErrors.value.password = errors.password[0]
      if (errors.non_field_errors) {
        // Handle non-field errors
        formErrors.value.password = errors.non_field_errors[0]
      }
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.registration-card {
  width: 100%;
  min-width: 600px;
  max-width: 500px;
  margin: 2rem auto;
  padding: 2rem 2.5rem 1.5rem 2.5rem;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
}

.v-card-title {
  font-size: 2rem !important;
  margin-bottom: 1.5rem;
}

.v-card-text {
  padding: 1rem 0 !important;
}

:deep(.v-form) {
  width: 100%;
}

:deep(.v-form .v-field) {
  width: 100%;
}

:deep(.v-form .v-btn-group) {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1.2rem;
  margin-top: 1.2rem;
  width: 100%;
}

:deep(.v-form .v-btn) {
  min-width: 140px;
  height: 44px;
  font-size: 1.08rem;
  font-weight: 600;
  text-transform: none;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.08);
  transition: all 0.2s cubic-bezier(.4,0,.2,1);
  letter-spacing: 0.2px;
}

:deep(.v-form .v-btn:first-child) {
  background-color: #f3f4f6 !important;
  color: #222 !important;
  border: 1px solid #e0e0e0;
}

:deep(.v-form .v-btn:first-child:hover) {
  background-color: #e0e0e0 !important;
  color: #111 !important;
}

:deep(.v-form .v-btn:last-child) {
  background-color: #1976d2 !important;
  color: #fff !important;
  border: 1px solid #1976d2;
}

:deep(.v-form .v-btn:last-child:hover) {
  background-color: #1565c0 !important;
  color: #fff !important;
  box-shadow: 0 4px 16px rgba(25, 118, 210, 0.15);
  transform: translateY(-2px) scale(1.03);
}

@media (max-width: 600px) {
  .registration-card {
    min-width: unset;
    max-width: 98vw;
    margin: 1rem;
    padding: 1rem;
  }
  .v-card-title {
    font-size: 1.3rem !important;
  }
}
</style> 