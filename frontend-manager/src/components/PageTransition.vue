<template>
  <div class="page-transition">
    <slot></slot>
  </div>
</template>

<script setup>
import { onBeforeRouteUpdate } from 'vue-router';

// Добавляем класс анимации при обновлении маршрута
onBeforeRouteUpdate(() => {
  const element = document.querySelector('.page-transition');
  if (element) {
    element.classList.remove('page-transition');
    void element.offsetWidth; // Форсируем перерисовку
    element.classList.add('page-transition');
  }
});
</script>

<style scoped>
.page-transition {
  animation: fadeIn 0.8s ease-out;
  min-height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style> 