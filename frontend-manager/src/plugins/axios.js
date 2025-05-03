import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api', // Базовый URL вашего API
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// Перехватчик запросов
api.interceptors.request.use(
  (config) => {
    // Здесь можно добавить токен авторизации
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Перехватчик ответов
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Обработка ошибки авторизации
      localStorage.removeItem('token');
      // Здесь можно добавить редирект на страницу логина
    }
    return Promise.reject(error);
  }
);

export default api; 