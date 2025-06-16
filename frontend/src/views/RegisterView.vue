<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-12">
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
                :rules="[v => !!v || 'Обязательное поле']"
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
                prepend-icon="mdi-email"
              />

              <BaseInput
                v-model="formData.password"
                label="Пароль"
                type="password"
                :rules="[
                  v => !!v || 'Обязательное поле',
                  v => v.length >= 6 || 'Минимум 6 символов'
                ]"
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
    await authStore.register({
      name: formData.value.name,
      email: formData.value.email,
      password: formData.value.password,
      role: formData.value.role
    })

    const redirectPath = route.query.redirect as string || '/'
    router.push(redirectPath)
  } catch (error: any) {
    console.error('Registration failed:', error)
    // Здесь можно добавить обработку ошибок
  } finally {
    loading.value = false
  }
}
</script> 