<script setup>
// Компонент использует router-view для отображения маршрутизированных компонентов
import { ref } from 'vue';
import { useSnackbar } from '@/composables/useSnackbar';
import Sidebar from '@/components/Sidebar.vue';

const { snackbar } = useSnackbar();
</script>

<template>
  <v-app>
    <Sidebar />
    <v-main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </v-main>

    <v-snackbar
      class="snackbar"
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="snackbar.timeout"
    >
      {{ snackbar.text }}
    </v-snackbar>
  </v-app>
</template>

<style>
/* Глобальные стили */
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  overflow-y: auto;
  background-color: #f5f5f5 !important;
}

#app {
  height: 100%;
  width: 100%;
  display: block;
}

.v-application {
  background-color: #f5f5f5 !important;
  min-height: 100vh;
}

.main-content {
  position: relative;
  z-index: 1;
  margin-left: 0 !important;
  transition: none !important;
  padding-left: 0 !important;
}

/* Стили для скроллбара */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background-color: rgba(0, 0, 0, 0.3);
}

/* Отключаем стандартные отступы Vuetify */
:deep(.v-main__wrap) {
  padding-left: 0 !important;
}

:deep(.v-layout) {
  padding-left: 0 !important;
}

.nav-drawer {
  position: fixed !important;
  z-index: 2;
  height: 100vh;
  transition: transform 0.3s ease;
}

.nav-drawer :deep(.v-list-item) {
  transition: all 0.3s ease;
  border-radius: 0 24px 24px 0;
  margin-right: 16px;
  color: #424242;
}

.nav-drawer :deep(.v-list-item.active-route) {
  background-color: #424242;
  color: white;
}

.nav-drawer :deep(.v-list-item:hover) {
  background-color: rgba(66, 66, 66, 0.1);
}

.nav-drawer :deep(.v-list-item.active-route:hover) {
  background-color: #424242;
}

.nav-drawer :deep(.v-icon) {
  color: #757575;
}

.nav-drawer :deep(.v-list-item.active-route .v-icon) {
  color: white;
}

/* Анимации переходов */
.page-enter-active,
.page-leave-active {
  transition: all 0.4s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
