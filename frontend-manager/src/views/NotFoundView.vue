<template>
  <v-container class="fill-height">
    <v-row class="fill-height" justify="center" align="center">
      <v-col cols="12" sm="8" md="6" lg="4" class="text-center">
        <div class="error-container">
          <h1 class="text-h1 font-weight-bold mb-4 error-code">404</h1>
          <h2 class="text-h4 mb-6">Страница не найдена</h2>
          <p class="text-body-1 mb-8 text-grey-darken-1">
            Похоже, что страница, которую вы ищете, не существует или была перемещена.
          </p>
          <v-btn
            color="grey-darken-2"
            variant="text"
            prepend-icon="mdi-arrow-left"
            @click="router.push('/')"
            class="home-btn"
          >
            Вернуться на главную
          </v-btn>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();
</script>

<style scoped>
.error-container {
  animation: fadeIn 0.8s ease-out;
}

.error-code {
  font-size: 8rem;
  line-height: 1;
  background: linear-gradient(45deg, #424242, #757575);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: float 3s ease-in-out infinite;
}

.home-btn {
  transition: transform 0.3s ease;
}

.home-btn:hover {
  transform: translateX(-5px);
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

@keyframes float {
  0% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
  100% {
    transform: translateY(0);
  }
}
</style> 