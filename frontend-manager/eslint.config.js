import pluginVue from 'eslint-plugin-vue';
import eslintPluginImport from 'eslint-plugin-import';
import eslintPluginPrettier from 'eslint-plugin-prettier';
import globals from 'globals';
import js from '@eslint/js';

export default [
  // Базовые правила для JavaScript
  js.configs.recommended,

  // Правила для Vue 3
  ...pluginVue.configs['flat/recommended'],

  // Правила для импортов
  {
    plugins: {
      import: eslintPluginImport,
    },
    rules: {
      'import/order': ['error', { 'newlines-between': 'always' }], // Сортировка импортов
      'import/no-unresolved': 'error', // Проверка корректности импортов
    },
  },

  // Интеграция с Prettier
  {
    plugins: {
      prettier: eslintPluginPrettier,
    },
    rules: {
      'prettier/prettier': 'error', // Использовать Prettier как правила форматирования
    },
  },

  // Общие настройки
  {
    files: ['**/*.js', '**/*.vue'], // Применять к JS и Vue файлам
    languageOptions: {
      sourceType: 'module', // Использовать ES Modules
      globals: {
        ...globals.browser, // Поддержка браузерных глобальных переменных (window, document)
        ...globals.node, // Поддержка Node.js (если нужно)
      },
      parserOptions: {
        ecmaVersion: 'latest', // Поддержка последних возможностей ECMAScript
      },
    },
    rules: {
      // Vue-специфичные правила
      'vue/no-unused-vars': 'error', // Запретить неиспользуемые переменные в шаблонах
      'vue/multi-word-component-names': 'off', // Отключить требование многословных имён компонентов
      'vue/no-v-html': 'warn', // Предупреждать о небезопасном использовании v-html

      // Общие правила
      'no-unused-vars': 'error', // Запретить неиспользуемые переменные
      'no-console': ['warn', { allow: ['error'] }], // Разрешить console.error, но предупреждать о других
      eqeqeq: 'error', // Требовать === вместо ==
      curly: 'error', // Требовать фигурные скобки для всех блоков
    },
  },
];
