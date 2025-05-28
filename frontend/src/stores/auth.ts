import { defineStore } from 'pinia';
import api from '../api';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null as { id: number; role: 'buyer' | 'seller'; name: string } | null,
  }),
  actions: {
    async login(email, password) {
      try {
        const response = await api.post('/auth/login/', { email, password });
        this.token = response.data.token;
        this.user = response.data.user || { id: response.data.id, role: 'buyer', name: 'User' }; // Adjust based on API response
        localStorage.setItem('token', this.token);
        return true;
      } catch (error) {
        console.error('Login failed:', error);
        return false;
      }
    },
    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem('token');
    },
  },
});