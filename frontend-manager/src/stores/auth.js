import { defineStore } from 'pinia';
import { authService } from '@/services/authService';
import { axiosConfigService } from '@/services/axiosConfigService';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
    expiresIn: localStorage.getItem('expiresIn') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
    userId: localStorage.getItem('userId') || null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    currentUser: (state) => state.user
  },

  actions: {
    async login(email, password) {
      try {
        const { id, token, refreshToken, expiresIn, user } = await authService.login(email, password);
        
        this.token = token;
        this.refreshToken = refreshToken;
        this.expiresIn = expiresIn;
        this.user = user;
        
        localStorage.setItem('token', token);
        localStorage.setItem('refreshToken', refreshToken);
        localStorage.setItem('expiresIn', expiresIn);
        localStorage.setItem('user', JSON.stringify(user));
        localStorage.setItem('userId', id);
        
        // Устанавливаем токен для всех API клиентов
        axiosConfigService.setAuthToken(token);
        
        return { token, user };
      } catch (error) {
        throw error.response?.data || error;
      }
    },

    async register(name, email, password) {
      try {
        return await authService.register(name, email, password);
      } catch (error) {
        throw error.response?.data || error;
      }
    },

    async logout() {
      try {
        await authService.logout(this.refreshToken);
      } finally {
        this.token = null;
        this.refreshToken = null;
        this.expiresIn = null;
        this.user = null;
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
        localStorage.removeItem('expiresIn');
        localStorage.removeItem('user');
        // Удаляем токен из всех API клиентов
        axiosConfigService.removeAuthToken();
      }
    },

    async checkAuth() {
      if (!this.token) return false;

      try {
        const user = await authService.getCurrentUser();
        this.user = user;
        localStorage.setItem('user', JSON.stringify(user));
        // Устанавливаем токен для всех API клиентов
        axiosConfigService.setAuthToken(this.token);
        return true;
      } catch (error) {
        this.logout();
        return false;
      }
    }
  }
}); 