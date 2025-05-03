import api from '@/plugins/axios';

export const userService = {
  // Получение списка пользователей
  getUsers() {
    return api.get('/users');
  },

  // Получение пользователя по ID
  getUser(id) {
    return api.get(`/users/${id}`);
  },

  // Создание нового пользователя
  createUser(userData) {
    return api.post('/users', userData);
  },

  // Обновление пользователя
  updateUser(id, userData) {
    return api.put(`/users/${id}`, userData);
  },

  // Удаление пользователя
  deleteUser(id) {
    return api.delete(`/users/${id}`);
  },

  // Авторизация
  login(credentials) {
    return api.post('/auth/login', credentials);
  },

  // Регистрация
  register(userData) {
    return api.post('/auth/register', userData);
  }
}; 