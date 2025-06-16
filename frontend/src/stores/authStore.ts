import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/config'
import { useRouter } from 'vue-router'

interface User {
  id: number
  username: string
  email: string
  is_seller: boolean
}

interface LoginCredentials {
  username: string
  password: string
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))
  const loading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!token.value)
  const isSeller = computed(() => user.value?.is_seller || false)

  const setToken = (newToken: string | null) => {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('token', newToken)
    } else {
      localStorage.removeItem('token')
    }
  }

  const login = async (credentials: LoginCredentials) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/auth/token/', credentials)
      const { access, refresh } = response.data
      setToken(access)
      localStorage.setItem('refreshToken', refresh)
      
      // После получения токена, получаем данные пользователя
      await fetchUser()
      return user.value
    } catch (e: any) {
      error.value = e.response?.data?.detail || 'Ошибка авторизации'
      throw e
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    user.value = null
    setToken(null)
    localStorage.removeItem('refreshToken')
  }

  const fetchUser = async () => {
    if (!token.value) return null

    try {
      const response = await api.get('/auth/user/')
      user.value = response.data
      return response.data
    } catch (e) {
      console.error('Error fetching user:', e)
      logout()
      return null
    }
  }

  // Инициализация при создании store
  if (token.value) {
    fetchUser()
  }

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    isSeller,
    login,
    logout,
    fetchUser
  }
}) 