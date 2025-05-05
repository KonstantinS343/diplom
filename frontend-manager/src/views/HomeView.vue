<template>
  <v-container class="py-8" max-width="2200px">
    <v-row justify="center" align="start">
      <v-col cols="12" md="10" lg="8">
        <!-- Название переводчика -->
        <div class="translator-title">
          <h1 class="text-h2 font-weight-bold">EchoTranslate</h1>
          <p class="text-subtitle-1 text-grey-darken-1">Простой и точный перевод</p>
        </div>

        <!-- Панель управления языками -->
        <div class="language-panel mb-6">
          <v-select
            v-model="sourceLanguage"
            :items="languages"
            label="Исходный язык"
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
            variant="outlined"
            density="compact"
            class="language-select"
          ></v-select>
        </div>

        <!-- Панели с текстом -->
        <v-row>
          <v-col cols="12" md="6">
            <v-card flat class="source-translation-card">
              <v-textarea
                v-model="sourceText"
                placeholder="Введите текст для перевода"
                auto-grow
                rows="10"
                variant="plain"
                class="translation-textarea"
                hide-details
                @input="debouncedTranslate"
                @keyup="debouncedAutocomplete"
                @keydown="handleKeyDown"
                :counter="10000"
                :rules="[v => v.length <= 10000 || 'Максимум 10,000 символов']"
              >
                <template v-slot:append>
                  <span v-if="isAutocompleteVisible" class="autocomplete-text">
                    {{ autocompleteText }}
                  </span>
                </template>
              </v-textarea>
              <v-card-actions class="pa-4 d-flex justify-end">
                <v-btn
                  color="grey-darken-2"
                  variant="text"
                  prepend-icon="mdi-delete"
                  @click="clearSourceText"
                >
                </v-btn>
                <v-btn
                  color="grey-darken-2"
                  variant="text"
                  :prepend-icon="sourceCopySuccess ? 'mdi-check' : 'mdi-content-copy'"
                  :color="sourceCopySuccess ? 'green-darken-2' : 'green-darken-3'"
                  @click="copySourceText"
                >
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card flat class="target-translation-card">
              <div class="translation-container">
                <v-textarea
                  v-model="translatedText"
                  placeholder="Перевод появится здесь"
                  auto-grow
                  rows="10"
                  variant="plain"
                  class="translation-textarea"
                  hide-details
                  readonly
                  :counter="10000"
                ></v-textarea>
                <div v-if="translating" class="loading-overlay">
                  <v-progress-circular
                    indeterminate
                    color="grey-darken-2"
                    size="64"
                  ></v-progress-circular>
                </div>
              </div>
              <v-card-actions class="pa-4 d-flex justify-end">
                <v-btn
                  color="grey-darken-2"
                  variant="text"
                  :prepend-icon="targetCopySuccess ? 'mdi-check' : 'mdi-content-copy'"
                  :color="targetCopySuccess ? 'green-darken-2' : 'green-darken-3'"
                  @click="copyTranslatedText"
                >
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>

        <!-- История переводов -->
        <div class="translation-history mt-8">
          <div class="d-flex align-center justify-space-between mb-4">
            <h2 class="text-h5 font-weight-medium">История переводов</h2>
            <div class="slider-controls">
              <v-btn
                icon
                variant="text"
                color="grey-darken-2"
                @click="scrollLeft"
                :disabled="!canScrollLeft"
              >
                <v-icon>mdi-chevron-left</v-icon>
              </v-btn>
              <v-btn
                icon
                variant="text"
                color="grey-darken-2"
                @click="scrollRight"
                :disabled="!canScrollRight"
              >
                <v-icon>mdi-chevron-right</v-icon>
              </v-btn>
            </div>
          </div>

          <div class="history-slider" ref="sliderRef">
            <div class="history-cards">
              <v-card
                v-for="(item, index) in translationHistory"
                :key="index"
                class="history-card"
                variant="outlined"
                @click="loadTranslation(item)"
              >
                <v-card-text>
                  <div class="d-flex align-center mb-2">
                    <v-icon size="small" color="grey-darken-1" class="mr-2">
                      mdi-translate
                    </v-icon>
                    <span class="text-caption text-grey-darken-1">
                      {{ item.sourceLang }} → {{ item.targetLang }}
                    </span>
                  </div>
                  <p class="text-body-2 text-truncate mb-1">{{ item.sourceText }}</p>
                  <p class="text-body-2 text-truncate text-grey-darken-1">{{ item.translatedText }}</p>
                </v-card-text>
              </v-card>
            </div>
          </div>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import { translationService } from '@/services/translationService';
import { useSnackbar } from '@/composables/useSnackbar';
import { useDebounce } from '@/composables/useDebounce';

const { showError } = useSnackbar();
const { debounce } = useDebounce();

const sourceText = ref('');
const translatedText = ref('');
const sourceLanguage = ref('ru');
const targetLanguage = ref('en');
const translating = ref(false);
const languages = ref([]);
const sourceCopySuccess = ref(false);
const targetCopySuccess = ref(false);

// Добавляем refs для автодополнения
const autocompleteText = ref('');
const cursorPosition = ref(0);
const isAutocompleteVisible = ref(false);

// История переводов
const translationHistory = ref([]);

const sliderRef = ref(null);
const canScrollLeft = ref(false);
const canScrollRight = ref(true);

// В script setup добавим ref для контроллера
const abortController = ref(null);

const scrollLeft = () => {
  if (sliderRef.value) {
    sliderRef.value.scrollBy({ left: -300, behavior: 'smooth' });
    updateScrollButtons();
  }
};

const scrollRight = () => {
  if (sliderRef.value) {
    sliderRef.value.scrollBy({ left: 300, behavior: 'smooth' });
    updateScrollButtons();
  }
};

const updateScrollButtons = () => {
  if (sliderRef.value) {
    const { scrollLeft, scrollWidth, clientWidth } = sliderRef.value;
    canScrollLeft.value = scrollLeft > 0;
    canScrollRight.value = scrollLeft < scrollWidth - clientWidth - 10;
  }
};

const loadTranslation = (item) => {
  sourceLanguage.value = languages.value.find(lang => lang.title === item.sourceLang)?.value || 'ru';
  targetLanguage.value = languages.value.find(lang => lang.title === item.targetLang)?.value || 'en';
  sourceText.value = item.sourceText;
  translate();
};

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
    console.error('Ошибка загрузки языков:', error);
  }
};

// В script setup добавим новые функции для работы с историей
const MAX_HISTORY_ITEMS = 10;

// Функция для загрузки истории из localStorage
const loadHistoryFromStorage = () => {
  const savedHistory = localStorage.getItem('translationHistory');
  if (savedHistory) {
    translationHistory.value = JSON.parse(savedHistory);
  }
};

// Функция для сохранения истории в localStorage
const saveHistoryToStorage = (history) => {
  localStorage.setItem('translationHistory', JSON.stringify(history));
};

// Функция для добавления перевода в историю
const addToHistory = (sourceText, translatedText) => {
  // Проверяем, есть ли уже такой перевод в истории
  const isDuplicate = translationHistory.value.some(
    item => item.sourceText === sourceText && item.translatedText === translatedText
  );

  if (isDuplicate) {
    return;
  }

  const sourceLangName = languages.value.find(lang => lang.value === sourceLanguage.value)?.title || sourceLanguage.value;
  const targetLangName = languages.value.find(lang => lang.value === targetLanguage.value)?.title || targetLanguage.value;

  const newItem = {
    sourceLang: sourceLangName,
    targetLang: targetLangName,
    sourceText,
    translatedText
  };

  // Добавляем новый перевод в начало массива
  translationHistory.value.unshift(newItem);
  
  // Ограничиваем историю 10 элементами
  if (translationHistory.value.length > MAX_HISTORY_ITEMS) {
    translationHistory.value = translationHistory.value.slice(0, MAX_HISTORY_ITEMS);
  }

  // Сохраняем обновленную историю
  saveHistoryToStorage(translationHistory.value);
};

// Обновим функцию translate
const translate = async () => {
  if (!sourceText.value) {
    translatedText.value = '';
    return;
  }
  
  // Отменяем предыдущий запрос, если он есть
  if (abortController.value) {
    abortController.value.abort();
  }
  
  // Создаем новый контроллер
  abortController.value = new AbortController();
  
  translating.value = true;
  try {
    const response = await translationService.translateText(
      sourceText.value,
      sourceLanguage.value,
      targetLanguage.value,
      abortController.value.signal
    );
    translatedText.value = response.data.text;
    addToHistory(sourceText.value, translatedText.value);
  } catch (error) {
    if (error.name === 'AbortError' || error.name === 'CanceledError') {
      console.log('Запрос на перевод отменен');
      return;
    }
    showError('Ошибка при переводе текста');
    console.error('Ошибка перевода:', error);
    translatedText.value = '';
  } finally {
    translating.value = false;
    abortController.value = null;
  }
};

onMounted(() => {
  loadLanguages();
  loadHistoryFromStorage();
  if (sliderRef.value) {
    sliderRef.value.addEventListener('scroll', updateScrollButtons);
    updateScrollButtons();
  }
});

onUnmounted(() => {
  if (sliderRef.value) {
    sliderRef.value.removeEventListener('scroll', updateScrollButtons);
  }
});

const clearSourceText = () => {
  // Отменяем текущий запрос при очистке
  if (abortController.value) {
    abortController.value.abort();
  }
  sourceText.value = '';
  translatedText.value = '';
};

const copySourceText = () => {
  navigator.clipboard.writeText(sourceText.value);
  sourceCopySuccess.value = true;
  setTimeout(() => {
    sourceCopySuccess.value = false;
  }, 2000);
};

const copyTranslatedText = () => {
  navigator.clipboard.writeText(translatedText.value);
  targetCopySuccess.value = true;
  setTimeout(() => {
    targetCopySuccess.value = false;
  }, 2000);
};

const swapLanguages = () => {
  const temp = sourceLanguage.value;
  sourceLanguage.value = targetLanguage.value;
  targetLanguage.value = temp;
  sourceText.value = translatedText.value;
  if (sourceText.value) {
    translate();
  }
};

// Создаем отложенную функцию перевода
const debouncedTranslate = debounce(translate, 1000);

// Функция для обработки автодополнения
const handleAutocomplete = async (event) => {
  const textarea = event.target;
  const position = textarea.selectionStart;
  cursorPosition.value = position;
  
  // Проверяем, есть ли пробел перед курсором
  const textBeforeCursor = sourceText.value.slice(0, position);
  if (!textBeforeCursor.endsWith(' ')) {
    isAutocompleteVisible.value = false;
    return;
  }
  
  try {
    const response = await translationService.autocomplete(sourceText.value, position, sourceLanguage.value);
    if (response.data) {
      // Фильтруем результаты, исключая те, что содержат # или .
      const filteredText = response.data.replace(/[#.]/g, '');
      if (filteredText) {
        autocompleteText.value = filteredText;
        isAutocompleteVisible.value = true;
      } else {
        isAutocompleteVisible.value = false;
      }
    }
  } catch (error) {
    console.error('Ошибка автодополнения:', error);
    isAutocompleteVisible.value = false;
  }
};

// Создаем отложенную функцию автодополнения
const debouncedAutocomplete = debounce(handleAutocomplete, 500);

// Функция для обработки нажатия клавиш
const handleKeyDown = (event) => {
  if (event.key === 'Tab' && isAutocompleteVisible.value) {
    event.preventDefault();
    insertAutocomplete();
  } else if (event.key !== 'Tab') {
    isAutocompleteVisible.value = false;
  }
};

// Функция для вставки автодополнения
const insertAutocomplete = () => {
  if (!isAutocompleteVisible.value) return;
  
  const beforeCursor = sourceText.value.slice(0, cursorPosition.value);
  const afterCursor = sourceText.value.slice(cursorPosition.value);
  
  sourceText.value = beforeCursor + autocompleteText.value + afterCursor;
  isAutocompleteVisible.value = false;
  autocompleteText.value = '';
};

watch(sourceLanguage, (newSourceLang, oldSourceLang) => {
  if (newSourceLang === targetLanguage.value) {
    targetLanguage.value = oldSourceLang;
    sourceText.value = translatedText.value;
  }
  if (sourceText.value) {
    translate();
  }
});

watch(targetLanguage, (newTargetLang, oldTargetLang) => {
  if (newTargetLang === sourceLanguage.value) {
    sourceLanguage.value = oldTargetLang;
    sourceText.value = translatedText.value;
  }
  if (sourceText.value) {
    translate();
  }
});

</script>

<style scoped>
.language-panel {
  display: flex;
  align-items: center;
  gap: 16px;
  width: 100%;
}

.language-select {
  flex: 1;
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


.source-translation-card:focus-within,
.target-translation-card:focus-within {
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2);
  transform: scale(1.01);
}

.translation-textarea {
  font-size: 1.1rem;
  line-height: 1.6;
  padding: 16px;
  flex-grow: 1;
  min-height: 350px !important;
}

:deep(.translation-textarea .v-field__input) {
  min-height: 350px !important;
  padding-top: 16px;
  padding-bottom: 16px;
  overflow-y: auto !important;
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

:deep(.v-field__counter) {
  position: absolute;
  bottom: 8px;
  right: 8px;
  font-size: 0.875rem;
  color: rgba(0, 0, 0, 0.6);
  background-color: rgba(255, 255, 255, 0.9);
  padding: 2px 8px;
  border-radius: 4px;
  z-index: 1;
}

:deep(.v-field__counter.error--text) {
  color: rgb(var(--v-theme-error));
}

:deep(.v-btn) {
  color: #757575;
  transition: all 0.3s ease;
}

:deep(.v-btn:hover) {
  color: #424242;
}

:deep(.v-btn.success) {
  transform: scale(1.1);
}

:deep(.v-icon) {
  color: #757575;
}

:deep(.v-btn:hover .v-icon) {
  color: #424242;
}

/* Исправление бага с увеличением */
.source-translation-card:not(:hover):not(:focus-within),
.target-translation-card:not(:hover):not(:focus-within) {
  transform: scale(1);
}

.translator-title {
  text-align: center;
  animation: fadeIn 0.8s ease-out;
  margin-top: 2rem;
  margin-bottom: 48px;
}

.translator-title h1 {
  background: linear-gradient(45deg, #424242, #757575);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-family: 'Montserrat', sans-serif;
  letter-spacing: 2px;
  margin-bottom: 4px;
  font-size: 3rem;
}

.translator-title p {
  font-family: 'Roboto', sans-serif;
  letter-spacing: 0.5px;
  opacity: 0.8;
  font-size: 1.2rem;
}

.translation-history {
  width: 100%;
}

.slider-controls {
  display: flex;
  gap: 8px;
}

.history-slider {
  width: 100%;
  overflow-x: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
  padding: 4px 0;
}

.history-slider::-webkit-scrollbar {
  display: none;
}

.history-cards {
  display: flex;
  gap: 16px;
  padding: 4px;
}

.history-card {
  min-width: 280px;
  max-width: 280px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
}

.history-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.history-card:active {
  transform: translateY(-2px);
}

.translation-container {
  position: relative;
  flex-grow: 1;
  min-height: 250px;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.8);
  z-index: 1;
}

.autocomplete-text {
  color: #9e9e9e;
  font-style: italic;
  pointer-events: none;
  user-select: none;
}

:deep(.v-field__append) {
  padding-right: 16px;
  opacity: 0.7;
}

:deep(.v-btn__prepend) {
  margin-right: 0;
}
</style> 