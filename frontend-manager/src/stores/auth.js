import { defineStore } from 'pinia';
import axios from 'axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    currentUser: (state) => state.user
  },

  actions: {
    async login(email, password) {
      try {
        const response = await axios.post('/api/auth/login', { email, password });
        const { token, user } = response.data;
        
        this.token = token;
        this.user = user;
        
        localStorage.setItem('token', token);
        localStorage.setItem('user', JSON.stringify(user));
        
        // Устанавливаем токен для всех последующих запросов
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        
        return response.data;
      } catch (error) {
        throw error.response?.data || error;
      }
    },

    async register(email, password) {
      try {
        const response = await axios.post('/api/auth/register', { email, password });
        return response.data;
      } catch (error) {
        throw error.response?.data || error;
      }
    },

    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      delete axios.defaults.headers.common['Authorization'];
    },

    async checkAuth() {
      if (!this.token) return false;

      try {
        const response = await axios.get('/api/auth/me');
        this.user = response.data;
        localStorage.setItem('user', JSON.stringify(response.data));
        return true;
      } catch (error) {
        this.logout();
        return false;
      }
    }
  }
}); 