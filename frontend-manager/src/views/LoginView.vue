<template>
  <v-container class="fill-height">
    <v-row class="fill-height" justify="center" align="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="auth-card">
          <v-card-title class="text-center text-h4 font-weight-bold mb-6">
            EchoTranslate
          </v-card-title>
          
          <v-card-text>
            <v-form @submit.prevent="handleLogin" ref="form">
              <v-text-field
                v-model="email"
                label="Email"
                type="email"
                variant="outlined"
                :rules="[rules.required, rules.email]"
                class="mb-4"
                @input="validateForm"
              ></v-text-field>

              <v-text-field
                v-model="password"
                label="Пароль"
                type="password"
                variant="outlined"
                :rules="[rules.required, rules.min]"
                class="mb-6"
                @input="validateForm"
              ></v-text-field>

              <v-btn
                block
                color="grey-darken-2"
                size="large"
                type="submit"
                :loading="loading"
                :disabled="!isFormValid"
                class="mb-4"
              >
                Войти
              </v-btn>

              <div class="text-center">
                <router-link to="/register" class="text-decoration-none text-grey-darken-1">
                  Нет аккаунта? Зарегистрироваться
                </router-link>
              </div>
            </v-form>

            <v-divider class="my-6"></v-divider>

            <div class="features-section">
            <h2 class="text-h6 mb-4">Возможности платформы</h2>
            <div class="features-list">
                <div class="feature-item">
                <v-icon icon="mdi-translate" color="grey-darken-2"></v-icon>
                <span>Перевод документов</span>
                </div>
                <div class="feature-item">
                <v-icon icon="mdi-brain" color="grey-darken-2"></v-icon>
                <span>ИИ технологии</span>
                </div>
                <div class="feature-item">
                <v-icon icon="mdi-account-group" color="grey-darken-2"></v-icon>
                <span>Сообщество</span>
                </div>
            </div>
            </div>

          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useSnackbar } from '@/composables/useSnackbar';

const router = useRouter();
const { showError } = useSnackbar();
const form = ref(null);

const email = ref('');
const password = ref('');
const loading = ref(false);
const isFormValid = ref(false);

const rules = {
  required: value => !!value || 'Обязательное поле',
  email: value => {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return pattern.test(value) || 'Некорректный email';
  },
  min: value => value.length >= 6 || 'Минимум 6 символов'
};

const validateForm = async () => {
  if (!form.value) return;
  
  const { valid } = await form.value.validate();
  isFormValid.value = valid;
};

const handleLogin = async () => {
  if (!isFormValid.value) return;
  
  loading.value = true;
  try {
    // TODO: Implement login logic
    await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call
    router.push('/');
  } catch (error) {
    showError('Ошибка при входе');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.auth-card {
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.v-card-title {
  background: linear-gradient(45deg, #424242, #757575);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-family: 'Montserrat', sans-serif;
  letter-spacing: 2px;
}

.features-section {
  text-align: center;
}

.features-section h2 {
  color: rgba(0, 0, 0, 0.87);
  font-weight: 500;
}

.features-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 16px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  color: rgba(0, 0, 0, 0.6);
}
</style> 