<template>
  <div class="profile-container">
    <!-- Заголовок страницы -->
    <div class="page-header">
      <h1 class="text-h4">Профиль пользователя</h1>
    </div>

    <v-card class="settings-card">
      <v-card-title class="text-h5 font-weight-medium">
        Настройки профиля
      </v-card-title>
      
      <v-card-text>
        <v-form @submit.prevent>
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="profile.name"
                label="Имя пользователя"
                variant="outlined"
                density="comfortable"
                bg-color="grey-lighten-4"
                readonly
              ></v-text-field>
            </v-col>
            
            <v-col cols="12" md="6">
              <v-text-field
                v-model="profile.email"
                label="Email"
                variant="outlined"
                density="comfortable"
                bg-color="grey-lighten-4"
                readonly
              ></v-text-field>
            </v-col>

            <v-col cols="12">
              <v-text-field
                v-model="profile.apiToken"
                label="API Токен"
                variant="outlined"
                density="comfortable"
                bg-color="grey-lighten-4"
                readonly
              >
                <template v-slot:append>
                  <v-btn
                    icon="mdi-content-copy"
                    variant="text"
                    size="small"
                    @click="copyToken"
                  ></v-btn>
                </template>
              </v-text-field>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>

    <!-- Текст внизу страницы -->
    <div class="bottom-text mt-8">
      <v-card class="info-card">
        <v-card-text>
          <div class="text-center">
            <v-icon size="48" color="grey-darken-2" class="mb-4">mdi-star</v-icon>
            <h3 class="text-h6 mb-2">Преимущества платформы</h3>
            <p class="text-body-1">
              Получите доступ к передовым технологиям машинного перевода, анализу качества и возможности улучшать свои навыки перевода. Наша платформа постоянно развивается благодаря обратной связи от пользователей.
            </p>
          </div>
        </v-card-text>
      </v-card>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useSnackbar } from '@/composables/useSnackbar';

const { showSnackbar } = useSnackbar();

const profile = ref({
  name: 'Константин',
  email: 'konstantin@example.com',
  apiToken: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...' // Пример токена
});

const copyToken = () => {
  navigator.clipboard.writeText(profile.value.apiToken);
  showSnackbar('Токен скопирован в буфер обмена', 'success');
};
</script>

<style scoped>
.profile-container {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 32px;
}

.page-header h1 {
  color: rgba(0, 0, 0, 0.87);
  font-weight: 500;
}

.settings-card {
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.info-card {
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  text-align: center;
}

.info-card h3 {
  color: rgba(0, 0, 0, 0.87);
  font-weight: 500;
}

.info-card p {
  color: rgba(0, 0, 0, 0.6);
  max-width: 600px;
  margin: 0 auto;
}

:deep(.v-card-title) {
  color: #424242;
  padding: 24px 24px 16px;
}

:deep(.v-card-text) {
  padding: 16px 24px;
}

:deep(.v-field) {
  border-radius: 8px;
}

:deep(.v-field__input) {
  color: #424242;
}

:deep(.v-field--focused .v-field__outline) {
  color: #424242;
}
</style> 