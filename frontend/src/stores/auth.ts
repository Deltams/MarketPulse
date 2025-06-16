import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import axios from 'axios';

interface User {
  id: number;
  email: string;
  name: string;
  role: 'buyer' | 'seller' | 'admin';
}

interface AuthState {
  user: User | null;
  token: string | null;
}

export const useAuthStore = defineStore('auth', () => {
  const state = ref<AuthState>({
    user: null,
    token: localStorage.getItem('token')
  });

  const isAuthenticated = computed(() => !!state.value.token);
  const isSeller = computed(() => state.value.user?.role === 'seller');
  const isAdmin = computed(() => state.value.user?.role === 'admin');

  const setAuth = (user: User, token: string) => {
    state.value.user = user;
    state.value.token = token;
    localStorage.setItem('token', token);
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  };

  const clearAuth = () => {
    state.value.user = null;
    state.value.token = null;
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
  };

  const login = async (email: string, password: string) => {
    try {
      const response = await axios.post('/api/auth/login', { email, password });
      const { user, token } = response.data;
      setAuth(user, token);
      return user;
    } catch (error) {
      clearAuth();
      throw error;
    }
  };

  const register = async (userData: { email: string; password: string; name: string; role: 'buyer' | 'seller' }) => {
    try {
      const response = await axios.post('/api/auth/register', userData);
      const { user, token } = response.data;
      setAuth(user, token);
      return user;
    } catch (error) {
      clearAuth();
      throw error;
    }
  };

  const logout = () => {
    clearAuth();
  };

  const checkAuth = async () => {
    if (!state.value.token) return null;

    try {
      const response = await axios.get('/api/auth/me');
      state.value.user = response.data;
      return response.data;
    } catch (error) {
      clearAuth();
      return null;
    }
  };

  return {
    user: computed(() => state.value.user),
    isAuthenticated,
    isSeller,
    isAdmin,
    login,
    register,
    logout,
    checkAuth
  };
});