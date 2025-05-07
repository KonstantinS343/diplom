import { authApi, translationApi, autocompleteApi, evaluationApi, learningApi } from '@/plugins/axios';

export const axiosConfigService = {
  setAuthToken(token) {
    if (token) {
      authApi.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      translationApi.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      autocompleteApi.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      evaluationApi.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      learningApi.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      this.removeAuthToken();
    }
  },

  removeAuthToken() {
    delete authApi.defaults.headers.common['Authorization'];
    delete translationApi.defaults.headers.common['Authorization'];
    delete autocompleteApi.defaults.headers.common['Authorization'];
    delete evaluationApi.defaults.headers.common['Authorization'];
    delete learningApi.defaults.headers.common['Authorization'];
  },
}; 