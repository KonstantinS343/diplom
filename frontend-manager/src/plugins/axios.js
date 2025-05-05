import axios from 'axios';
import API_CONFIG from '../config/api';

// Базовые настройки для всех инстансов
const createAxiosInstance = (baseURL) => {
  const instance = axios.create({
    baseURL,
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
  });

  // Перехватчик запросов
  instance.interceptors.request.use(
    (config) => {
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
  instance.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401) {
        localStorage.removeItem('token');
        // Здесь можно добавить редирект на страницу логина
      }
      return Promise.reject(error);
    }
  );

  return instance;
};

// Создаем инстансы для каждого микросервиса
const authApi = createAxiosInstance(API_CONFIG.auth.baseURL);
const translationApi = createAxiosInstance(API_CONFIG.translation.baseURL);
const autocompleteApi = createAxiosInstance(API_CONFIG.autocomplete.baseURL);
const evaluationApi = createAxiosInstance(API_CONFIG.evaluation.baseURL);
const learningApi = createAxiosInstance(API_CONFIG.learning.baseURL);

export {
  authApi,
  translationApi,
  evaluationApi,
  learningApi,
  autocompleteApi,
  API_CONFIG
}; 