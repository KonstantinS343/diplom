<template>
  <v-navigation-drawer
    v-model="drawer"
    :rail="rail"
    expand-on-hover
    @mouseenter="rail = false"
    @mouseleave="rail = true"
    class="sidebar"
    :rail-width="70"
    :app="false"
    :scrim="false"
  >
    <v-list v-if="authStore.isAuthenticated">
      <v-list-item
        prepend-avatar="https://randomuser.me/api/portraits/men/85.jpg"
        :title="rail ? '' : authStore.user?.username || 'Пользователь'"
        :subtitle="rail ? '' : authStore.user?.email || ''"
      ></v-list-item>
    </v-list>

    <v-divider></v-divider>

    <v-list density="compact" nav>
      <v-list-item
        v-for="item in menuItems"
        :key="item.title"
        :value="item.title"
        :to="item.path"
        :prepend-icon="item.icon"
        :title="rail ? '' : item.title"
        class="menu-item"
        :class="{ 'active-route': $route.path === item.path }"
      >
        <template v-slot:prepend>
          <v-icon :icon="item.icon" class="menu-icon"></v-icon>
        </template>
      </v-list-item>
    </v-list>

    <template v-slot:append>
      <div class="pa-2" v-if="authStore.isAuthenticated">
        <v-list-item
          @click="handleLogout"
          :value="'Выход'"
          :title="rail ? '' : 'Выход'"
          class="menu-item logout-item"
        >
          <template v-slot:prepend>
            <v-icon :icon="'mdi-logout'" class="menu-icon"></v-icon>
          </template>
        </v-list-item>

        <v-list-item
          :to="'/profile'"
          :value="'Настройки'"
          :title="rail ? '' : 'Настройки'"
          class="menu-item"
          :class="{ 'active-route': $route.path === '/profile' }"
        >
          <template v-slot:prepend>
            <v-icon :icon="'mdi-cog'" class="menu-icon"></v-icon>
          </template>
        </v-list-item>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const router = useRouter();
const drawer = ref(true);
const rail = ref(true);
const authStore = useAuthStore();

const handleLogout = async () => {
  await authStore.logout();
  router.push('/login');
};

const menuItems = computed(() => {
  const items = [
    {
      title: 'Главная',
      icon: 'mdi-home',
      path: '/',
      requiresAuth: false
    },
    {
      title: 'Оценка перевода',
      icon: 'mdi-translate',
      path: '/translation-evaluation',
      requiresAuth: false
    }
  ];

  // Добавляем защищенные маршруты только если пользователь авторизован
  if (authStore.isAuthenticated) {
    items.push(
      {
        title: 'Перевод документов',
        icon: 'mdi-file-document',
        path: '/translation-documents',
        requiresAuth: true
      },
      {
        title: 'Обучение',
        icon: 'mdi-book',
        path: '/learning',
        requiresAuth: true
      },
      {
        title: 'О платформе',
        icon: 'mdi-information',
        path: '/about',
        requiresAuth: false
      }
    );
  }

  return items;
});
</script>

<style scoped>
.sidebar {
  background: linear-gradient(180deg, #ffffff 0%, #f5f5f5 100%);
  border-right: 1px solid rgba(0, 0, 0, 0.12);
  transition: all 0.3s ease;
  position: fixed !important;
  top: 0;
  left: 0;
  height: 100vh;
  z-index: 1000;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}

.menu-item {
  margin: 4px 8px;
  border-radius: 8px !important;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.menu-item.active-route {
  background-color: #424242;
  color: white;
}

.menu-item.active-route .menu-icon {
  color: white;
}

.menu-item:hover {
  background-color: rgba(0, 0, 0, 0.04);
  transform: translateX(4px);
}

.menu-item.active-route:hover {
  background-color: #424242;
}

.menu-icon {
  transition: all 0.3s ease;
}

.menu-item:hover .menu-icon {
  transform: scale(1.1);
  color: #424242;
}

:deep(.v-list-item__prepend) {
  margin-right: 12px;
}

:deep(.v-navigation-drawer__content) {
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(0, 0, 0, 0.2) transparent;
}

:deep(.v-navigation-drawer__content::-webkit-scrollbar) {
  width: 6px;
}

:deep(.v-navigation-drawer__content::-webkit-scrollbar-track) {
  background: transparent;
}

:deep(.v-navigation-drawer__content::-webkit-scrollbar-thumb) {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

:deep(.v-navigation-drawer) {
  transition: width 0.3s ease !important;
}

:deep(.v-navigation-drawer--rail) {
  width: 70px !important;
}

:deep(.v-navigation-drawer--rail .v-list-item) {
  padding-left: 12px !important;
  padding-right: 12px !important;
}

/* Отключаем отступы для основного контента */
:deep(.v-main) {
  padding-left: 0 !important;
  transition: none !important;
}

/* Отключаем затемнение фона */
:deep(.v-navigation-drawer__scrim) {
  opacity: 0 !important;
}

.logout-item {
  color: #d32f2f;
}

.logout-item:hover {
  background-color: rgba(211, 47, 47, 0.04) !important;
}

.logout-item .menu-icon {
  color: #d32f2f;
}

.logout-item:hover .menu-icon {
  color: #d32f2f;
}
</style>