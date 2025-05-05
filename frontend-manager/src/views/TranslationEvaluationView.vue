<template>
  <div class="evaluation-container">
    <div class="content-wrapper">
      <!-- Заголовок страницы -->
      <div class="page-header">
        <h1 class="text-h4 mb-2">Оценка перевода</h1>
        <p class="text-body-1 text-medium-emphasis">
          Сравните ваш перевод с эталонным и получите детальный анализ различий
        </p>
      </div>

      <div class="language-panel mb-6">
        <v-select
          v-model="sourceLanguage"
          :items="languages"
          label="Исходный язык"
          bg-color="white"
          variant="outlined"
          density="compact"
          class="language-select"
        ></v-select>

        <v-btn
          icon
          variant="text"
          color="grey-darken-2"
          @click="swapLanguages"
          class="swap-btn"
        >
          <v-icon>mdi-swap-horizontal</v-icon>
        </v-btn>

        <v-select
          v-model="targetLanguage"
          :items="languages"
          label="Язык перевода"
          bg-color="white"
          variant="outlined"
          density="compact"
          class="language-select"
        ></v-select>
      </div>

      <v-row>
        <v-col cols="12" md="6">
          <v-card flat class="source-translation-card">
            <v-textarea
              v-model="sourceText"
              placeholder="Исходный текст"
              auto-grow
              rows="10"
              variant="plain"
              class="translation-textarea"
              hide-details
            ></v-textarea>
          </v-card>
        </v-col>

        <v-col cols="12" md="6">
          <v-card flat class="target-translation-card">
            <v-textarea
              v-model="translatedText"
              placeholder="Переведенный текст"
              auto-grow
              rows="10"
              variant="plain"
              class="translation-textarea"
              hide-details
            ></v-textarea>
          </v-card>
        </v-col>
      </v-row>

      <v-row justify="center" class="mt-4">
        <v-col cols="auto">
          <v-btn
            color="grey-darken-2"
            size="large"
            @click="evaluateTranslation"
            :loading="isEvaluating"
            :disabled="!sourceText || !translatedText"
          >
            Оценить
          </v-btn>
        </v-col>
      </v-row>

      <v-expand-transition>
        <v-row v-if="evaluationResult" class="mt-4">
          <v-col cols="12" md="6">
            <v-card flat class="source-translation-card">
              <div class="evaluation-header">
                <v-icon icon="mdi-translate" color="grey-darken-2" class="mr-2"></v-icon>
                <span class="evaluation-title">Правильный перевод</span>
              </div>
              <div class="evaluation-content">
                <v-textarea
                  v-model="modelTranslation"
                  auto-grow
                  rows="10"
                  variant="plain"
                  class="translation-textarea"
                  hide-details
                  readonly
                ></v-textarea>
              </div>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card flat class="source-translation-card">
              <div class="evaluation-header">
                <v-icon icon="mdi-chart-bar" color="grey-darken-2" class="mr-2"></v-icon>
                <span class="evaluation-title">Результат оценки</span>
              </div>
              <div class="evaluation-content">
                <div class="marked-text-wrapper">
                  <marked-text :text="evaluationResult" />
                </div>
              </div>
            </v-card>
          </v-col>
        </v-row>
      </v-expand-transition>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useSnackbar } from '@/composables/useSnackbar';
import { translationService } from '@/services/translationService';
import { evaluationService } from '@/services/evaluationService';
import MarkedText from '@/components/MarkedText.vue';

const { showSuccess, showError } = useSnackbar();

const sourceLanguage = ref('ru');
const targetLanguage = ref('en');
const sourceText = ref('');
const translatedText = ref('');
const evaluationResult = ref('');
const modelTranslation = ref('');
const isEvaluating = ref(false);
const languages = ref([]);

const swapLanguages = () => {
  let temp = sourceLanguage.value;
  sourceLanguage.value = targetLanguage.value;
  targetLanguage.value = temp;

  temp = translatedText.value;
  translatedText.value = sourceText.value;
  sourceText.value = temp;
};

const evaluateTranslation = async () => {
  if (!sourceText.value || !translatedText.value) {
    showError('Пожалуйста, заполните оба поля');
    return;
  }

  isEvaluating.value = true;
  try {
    const response = await evaluationService.evaluateTranslation(
      sourceText.value,
      translatedText.value,
      sourceLanguage.value,
      targetLanguage.value
    );

    evaluationResult.value = response.data.highlighted_text;
    modelTranslation.value = response.data.model_text;
    showSuccess('Оценка перевода успешно выполнена');
  } catch (error) {
    console.error('Ошибка оценки перевода:', error);
    showError('Произошла ошибка при оценке перевода');
  } finally {
    isEvaluating.value = false;
  }
};

onMounted(() => {
  loadLanguages();
});

// Загрузка списка поддерживаемых языков
const loadLanguages = async () => {
  try {
    const response = await translationService.getSupportedLanguages();
    
    languages.value = Object.entries(response.data).map(([code, info]) => ({
      title: info.language_name_user,
      value: code
    }));
  } catch (error) {
    showError('Не удалось загрузить список языков');
  }
};

watch(sourceLanguage, (newSourceLang, oldSourceLang) => {
  if (newSourceLang === targetLanguage.value) {
    targetLanguage.value = oldSourceLang;
    const temp = translatedText.value;
    translatedText.value = sourceText.value;
    sourceText.value = temp;
  }
});

watch(targetLanguage, (newTargetLang, oldTargetLang) => {
  if (newTargetLang === sourceLanguage.value) {
    sourceLanguage.value = oldTargetLang;
    const temp = translatedText.value;
    translatedText.value = sourceText.value;
    sourceText.value = temp;
  }
});
</script>

<style scoped>
.evaluation-container {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
  margin-block: 25px;
}

.content-wrapper {
  width: 100%;
}

.language-panel {
  display: flex;
  align-items: center;
  gap: 16px;
  width: 100%;
}

.language-select {
  flex: 1;
  min-width: 0;
}

.swap-btn {
  margin: 0 8px;
  align-self: center;
  color: #757575;
  margin-bottom: 1.2rem;
}

.swap-btn:hover {
  color: #424242;
}

.source-translation-card,
.target-translation-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: 100%;
  min-height: 450px;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
  transform: scale(1);
}

.source-translation-card:hover,
.target-translation-card:hover {
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2);
  transform: scale(1.01);
}

.translation-textarea {
  font-size: 1.1rem;
  line-height: 1.6;
  padding: 16px;
  flex-grow: 1;
  overflow-y: auto;
  color: #424242;
}

:deep(.source-translation-card .v-field__input),
:deep(.target-translation-card .v-field__input) {
  padding-top: 16px;
  padding-bottom: 16px;
  min-height: 250px;
  overflow-y: auto !important;
  color: #424242;
}

:deep(.v-field) {
  background-color: white !important;
}

:deep(.v-field--variant-outlined) {
  background-color: white !important;
}

:deep(.v-field--variant-plain) {
  background-color: white !important;
}

:deep(.v-textarea textarea) {
  overflow-y: auto !important;
  scrollbar-width: thin;
  scrollbar-color: rgba(0, 0, 0, 0.2) transparent;
  color: #424242;
}

:deep(.v-textarea textarea::placeholder) {
  color: #9e9e9e;
}

:deep(.v-textarea textarea::-webkit-scrollbar) {
  width: 6px;
}

:deep(.v-textarea textarea::-webkit-scrollbar-track) {
  background: transparent;
}

:deep(.v-textarea textarea::-webkit-scrollbar-thumb) {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

:deep(.v-btn) {
  color: #757575;
}

:deep(.v-btn:hover) {
  color: #424242;
}

:deep(.v-icon) {
  color: #757575;
}

:deep(.v-btn:hover .v-icon) {
  color: #424242;
}

.evaluation-header {
  padding: 16px 16px 8px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}

.evaluation-title {
  font-size: 1.1rem;
  font-weight: 500;
  color: #424242;
}

.page-header {
  text-align: center;
  margin-bottom: 32px;
}

.page-header h1 {
  color: rgba(0, 0, 0, 0.87);
  font-weight: 500;
}

.page-header p {
  color: rgba(0, 0, 0, 0.6);
}

.evaluation-content {
  position: relative;
  background-color: white;
  border-radius: 0 0 12px 12px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.marked-text-wrapper {
  flex-grow: 1;
  overflow-y: auto;
  padding: 16px;
  font-size: 1.1rem;
  line-height: 1.6;
  color: #424242;
}
</style> 