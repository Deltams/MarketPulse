<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center" class="fill-height">
      <v-col cols="14" sm="14" md="6" lg="12" xl="4">
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
  background: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
}

@media (max-width: 600px) {
  .login-card {
    padding: 20px 8px 16px 8px;
    margin: 24px auto;
    max-width: 98vw;
  }
}
</style>