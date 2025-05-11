import { authApi, API_CONFIG } from '@/plugins/axios';

export const authService = {
  async login(email, password) {
    const response = await authApi.post(API_CONFIG.auth.endpoints.login, {
      email,
      password
    });
    
    const { id, access_token, refresh_token, expires_in, user } = response.data;
    
    return {
      id: id,
      token: access_token,
      refreshToken: refresh_token,
      expiresIn: expires_in,
      user: {
        email: user.email,
        username: user.username,
      }
    };
  },

  async register(username, email, password) {
    const response = await authApi.post(API_CONFIG.auth.endpoints.register, {
      username,
      email,
      password
    });
    return response.data;
  },

  async getCurrentUser() {
    const response = await authApi.get(API_CONFIG.auth.endpoints.me);
    return response.data;
  },

  async logout(refreshToken) {
    const response = await authApi.post(API_CONFIG.auth.endpoints.logout, {
      refresh_token: refreshToken
    });
    return response.data;
  }
}; 