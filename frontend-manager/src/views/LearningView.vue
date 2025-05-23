<template>
  <div class="learning-container">
    <div class="content-wrapper">
      <!-- Основной контент -->
      <div class="learning-content">
        <!-- Список языковых пар -->
        <div 
          class="language-pairs-list"
          :class="{ 'shifted': selectedPair }"
        >
          <div class="welcome-section" v-if="!selectedPair">
            <h1 class="text-h4 mb-6">Улучшайте платформу вместе с нами</h1>
            <p class="text-body-1 mb-8">
              Загружайте свои переводы для обучения моделей. Каждая загруженная языковая пара помогает сделать
              платформу умнее и точнее. Выберите языковую пару или загрузите новую для начала работы.
            </p>
            <div class="features-grid">
              <div class="feature-card">
                <v-icon icon="mdi-brain" size="32" color="grey-darken-2"></v-icon>
                <h3 class="text-h6 mt-4">Улучшайте модели</h3>
                <p class="text-body-2">Ваши переводы помогают обучать и совершенствовать алгоритмы платформы</p>
              </div>
              <div class="feature-card">
                <v-icon icon="mdi-account-group" size="32" color="grey-darken-2"></v-icon>
                <h3 class="text-h6 mt-4">Сообщество</h3>
                <p class="text-body-2">Станьте частью сообщества, которое делает переводы лучше</p>
              </div>
              <div class="feature-card">
                <v-icon icon="mdi-chart-timeline-variant" size="32" color="grey-darken-2"></v-icon>
                <h3 class="text-h6 mt-4">Развитие платформы</h3>
                <p class="text-body-2">Расширяйте функционал, добавляя новые языковые пары и контексты</p>
              </div>
            </div>
            <div class="action-buttons mt-8">
              <v-btn
                color="grey-darken-2"
                size="large"
                prepend-icon="mdi-plus"
                @click="openNewPairDialog"
              >
                Создать новую пару
              </v-btn>
            </div>
          </div>
          <div
            v-for="pair in languagePairs"
            class="language-pair-item"
            :class="{ 'selected': selectedPair?.id === pair.id }"
            @click="selectPair(pair)"
          >
            <div class="pair-content">
              <div class="language left">
                <div class="flag-circle">
                  <img :src="getFlagUrl(pair.sourceLanguage)" :alt="pair.sourceLanguage">
                </div>
                <span class="language-name">{{ pair.sourceLanguage }}</span>
              </div>
              <div class="center-column">
                <v-chip
                  v-if="pair.isNew"
                  color="primary"
                  size="small"
                  class="new-chip"
                >
                  NEW
                </v-chip>
                <v-icon icon="mdi-arrow-left-right" class="arrow-icon"></v-icon>
              </div>
              <div class="language right">
                <div class="flag-circle">
                  <img :src="getFlagUrl(pair.targetLanguage)" :alt="pair.targetLanguage">
                </div>
                <span class="language-name">{{ pair.targetLanguage }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Карточки для обучения -->
        <div 
          class="learning-cards-container"
          :class="{ 'visible': selectedPair }"
        >
          <!-- Заголовок и фильтры -->
          <div class="cards-header" v-if="selectedPair">
            <div class="header-left">
              <v-btn
                icon
                variant="text"
                color="grey-darken-2"
                @click="selectedPair = null"
                class="back-btn"
              >
                <v-icon>mdi-arrow-left</v-icon>
              </v-btn>
              <div class="pair-info">
                <h2 class="text-h5 mb-1">{{ selectedPair.sourceLanguage }} <v-icon icon="mdi-arrow-left-right" class="arrow-icon"></v-icon> {{ selectedPair.targetLanguage }}</h2>
                <div class="stats">
                  <span class="stat-item">
                    <v-icon size="small" color="grey-darken-2">mdi-cards</v-icon>
                    {{ learningCards.length }} карточек
                  </span>
                  <span class="stat-item">
                    <v-icon size="small" color="grey-darken-2">mdi-thumb-up</v-icon>
                    {{ ratedCardsCount }} оценено
                  </span>
                </div>
              </div>
            </div>
            <div class="filters-panel">
              <v-btn
                color="grey-darken-2"
                variant="text"
                :class="{ 'active-filter': !showOnlyRated }"
                @click="showOnlyRated = false"
              >
                Все
              </v-btn>
              <v-btn
                color="grey-darken-2"
                variant="text"
                :class="{ 'active-filter': showOnlyRated }"
                @click="showOnlyRated = true"
              >
                Оцененные
              </v-btn>
              <v-btn
                color="grey-darken-2"
                variant="text"
                :class="{ 'active-filter': true }"
                @click="sortOrder = sortOrder === 'desc' ? 'asc' : 'desc'"
              >
                <v-icon>{{ sortOrder === 'desc' ? 'mdi-sort-calendar-descending' : 'mdi-sort-calendar-ascending' }}</v-icon>
                {{ sortOrder === 'desc' ? 'Сначала новые' : 'Сначала старые' }}
              </v-btn>
              <v-btn
                color="grey-darken-2"
                prepend-icon="mdi-plus"
                @click="openUploadDialog"
              >
                Добавить
              </v-btn>
            </div>
          </div>

          <!-- Список карточек -->
          <div class="learning-cards">
            <div
              v-for="card in paginatedCards"
              :key="card.id"
              class="learning-card"
            >
              <div class="card-content">
                <div class="source-text">{{ card.sourceText }}</div>
                <div class="target-text">{{ card.targetText }}</div>
                <div class="card-actions">
                  <div class="vote-group">
                    <v-btn
                      icon
                      variant="text"
                      :color="card.user_vote === 'like' ? 'success' : 'grey-darken-2'"
                      @click="rateCard(card, 'like')"
                    >
                      <v-icon>mdi-thumb-up</v-icon>
                    </v-btn>
                    <span class="vote-count">{{ card.likes }}</span>
                  </div>
                  <div class="vote-group">
                    <v-btn
                      icon
                      variant="text"
                      :color="card.user_vote === 'dislike' ? 'error' : 'grey-darken-2'"
                      @click="rateCard(card, 'dislike')"
                    >
                      <v-icon>mdi-thumb-down</v-icon>
                    </v-btn>
                    <span class="vote-count">{{ card.dislikes }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Пагинация -->
          <div class="pagination" v-if="selectedPair">
            <v-pagination
              v-model="currentPage"
              :length="totalPages"
              :total-visible="7"
              color="grey-darken-2"
            ></v-pagination>
          </div>
        </div>
      </div>
    </div>

    <!-- Диалог загрузки JSON -->
    <v-dialog v-model="uploadDialog" max-width="500px">
      <v-card>
        <v-card-title>Загрузка данных для обучения</v-card-title>
        <v-card-text>
          <div 
            class="upload-area" 
            @click="triggerFileInput"
            @dragover.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
            @drop.prevent="handleFileDrop"
            :class="{ 'is-dragging': isDragging }"
          >
            <input
              ref="fileInput"
              type="file"
              accept=".json"
              class="file-input"
              @change="handleFileSelect"
            />
            <template v-if="!jsonFile">
              <v-icon
                icon="mdi-cloud-upload"
                size="64"
                color="grey-darken-2"
                class="mb-4"
              ></v-icon>
              <div class="upload-text">
                <div class="text-h6 mb-2">Перетащите JSON файл сюда</div>
                <div class="text-body-1 text-medium-emphasis">или нажмите для выбора файла</div>
              </div>
            </template>
            <template v-else>
              <div class="selected-file">
                <v-icon
                  icon="mdi-file-document"
                  size="48"
                  color="grey-darken-2"
                  class="mb-4"
                ></v-icon>
                <div class="file-info">
                  <div class="text-h6 mb-2">{{ jsonFile.name }}</div>
                  <div class="text-body-2 text-medium-emphasis">
                    {{ formatFileSize(jsonFile.size) }}
                  </div>
                </div>
              </div>
            </template>
          </div>
          <div v-if="uploadError" class="error-message mt-4">
            {{ uploadError }}
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="grey-darken-2"
            variant="text"
            @click="uploadDialog = false"
          >
            Отмена
          </v-btn>
          <v-btn
            color="grey-darken-2"
            @click="uploadJson"
            :loading="isUploading"
            :disabled="!jsonFile || !!uploadError"
          >
            Загрузить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог создания новой пары -->
    <v-dialog v-model="newPairDialog" max-width="500px">
      <v-card>
        <v-card-title>Создание новой языковой пары</v-card-title>
        <v-card-text>
          <v-text-field
            v-model="newPair.sourceLanguage"
            label="Исходный язык"
            placeholder="Например: Русский"
            class="mb-4"
            :error-messages="newPairErrors.sourceLanguage"
            color="grey-darken-2"
          >
            <template v-slot:prepend-inner>
              <div class="flag-circle-small" v-if="newPair.sourceLanguage">
                <img :src="getFlagUrl(newPair.sourceLanguage)" :alt="newPair.sourceLanguage">
              </div>
            </template>
          </v-text-field>
          
          <v-text-field
            v-model="newPair.targetLanguage"
            label="Целевой язык"
            placeholder="Например: Английский"
            :error-messages="newPairErrors.targetLanguage"
            color="grey-darken-2"
          >
            <template v-slot:prepend-inner>
              <div class="flag-circle-small" v-if="newPair.targetLanguage">
                <img :src="getFlagUrl(newPair.targetLanguage)" :alt="newPair.targetLanguage">
              </div>
            </template>
          </v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="grey-darken-2"
            variant="text"
            @click="newPairDialog = false"
            :disabled="isCheckingPair"
          >
            Отмена
          </v-btn>
          <v-btn
            color="grey-darken-2"
            @click="createNewPair"
            :loading="isCheckingPair"
          >
            {{ isCheckingPair ? 'Проверка...' : 'Создать' }}
          </v-btn>
        </v-card-actions>
        </v-card>
    </v-dialog>
  </div>
</template> 

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useSnackbar } from '@/composables/useSnackbar';
import { languages } from '@/constants/languages';
import { languagePairsService } from '@/services/languagePairsService';

const { showSuccess, showError } = useSnackbar();

// Состояние
const showOnlyRated = ref(false);
const selectedPair = ref(null);
const uploadDialog = ref(false);
const jsonFile = ref(null);
const uploadError = ref('');
const isUploading = ref(false);
const currentPage = ref(1);
const itemsPerPage = 10;
const isDragging = ref(false);
const newPairDialog = ref(false);
const sortOrder = ref('desc');
const newPair = ref({
  sourceLanguage: '',
  targetLanguage: ''
});
const newPairErrors = ref({
  sourceLanguage: '',
  targetLanguage: ''
});
const isCheckingPair = ref(false);

// Тестовые данные
const languagePairs = ref([]);

const learningCards = ref([]);

// Вычисляемые свойства
const paginatedCards = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  
  // Создаем копию массива для сортировки
  const sortedCards = [...learningCards.value].sort((a, b) => {
    const dateA = new Date(a.createdAt);
    const dateB = new Date(b.createdAt);
    return sortOrder.value === 'desc' ? dateB - dateA : dateA - dateB;
  });
  
  return sortedCards.slice(start, end);
});

const totalPages = computed(() => {
  return Math.ceil(learningCards.value.length / itemsPerPage);
});

const ratedCardsCount = computed(() => {
  return learningCards.value.filter(card => card.user_vote !== null).length;
});

// Методы
const selectPair = async (pair) => {
  selectedPair.value = pair;
  currentPage.value = 1;
  await loadCards();
};

const loadCards = async () => {
  try {
    const sourceLang = languages.find(l => l.name === selectedPair.value.sourceLanguage)?.iso;
    const targetLang = languages.find(l => l.name === selectedPair.value.targetLanguage)?.iso;
    
    if (!sourceLang || !targetLang) {
      throw new Error('Не удалось определить языки');
    }

    const cards = await languagePairsService.getCards(sourceLang, targetLang);
    learningCards.value = cards.data.map(card => ({
      id: card._id,
      sourceText: card[sourceLang],
      targetText: card[targetLang],

      likes: card.likes,
      dislikes: card.dislikes,
      createdAt: card.created_at,
      user_vote: card.user_vote
    }));
  } catch (error) {
    learningCards.value = [];
  }
};

const rateCard = async (card, rating) => {
  try {
    const collection = `${selectedPair.value.sourceLang}-${selectedPair.value.targetLang}`;
    
    // Если нажали на ту же кнопку, что уже была активна - отменяем голос
    if (card.user_vote === rating) {
      const response = await languagePairsService.rateCard(card.id, null, collection);
      if (response.data) {
        // Уменьшаем счетчик в зависимости от типа голоса
        if (rating === 'like') {
          card.likes--;
        } else {
          card.dislikes--;
        }
        card.user_vote = null;
        showSuccess('Оценка отменена');
      }
      return;
    }
    
    const response = await languagePairsService.rateCard(card.id, rating, collection);
    
    if (response.data) {
      // Если был другой голос, уменьшаем его счетчик
      if (card.user_vote === 'like') {
        card.likes--;
      } else if (card.user_vote === 'dislike') {
        card.dislikes--;
      }
      
      // Увеличиваем счетчик нового голоса
      if (rating === 'like') {
        card.likes++;
      } else {
        card.dislikes++;
      }
      card.user_vote = rating;
      showSuccess('Оценка сохранена');
    } else {
      showError('Ошибка при сохранении оценки');
    }
  } catch (error) {
    showError('Ошибка при сохранении оценки');
    console.error('Error rating card:', error);
  }
};

const getFlagUrl = (language) => {
  const lang = languages.find(l => l.name === language);
  const iso = lang?.iso || 'un';
  if (iso === 'en') {
    return `https://flagcdn.com/w40/gb.png`;
  }
  return `https://flagcdn.com/w40/${iso}.png`;
};

const openUploadDialog = () => {
  uploadDialog.value = true;
  jsonFile.value = null;
  uploadError.value = '';
};

const handleFileSelect = (event) => {
  const file = event.target.files[0];
  if (file) {
    if (file.type !== 'application/json') {
      uploadError.value = 'Пожалуйста, выберите JSON файл';
      return;
    }
    jsonFile.value = file;
    validateJsonFile(file);
  }
};

const handleFileDrop = (event) => {
  isDragging.value = false;
  const file = event.dataTransfer.files[0];
  if (file) {
    if (file.type !== 'application/json') {
      uploadError.value = 'Пожалуйста, выберите JSON файл';
      return;
    }
    jsonFile.value = file;
    validateJsonFile(file);
  }
};

const validateJsonFile = (file) => {
  if (!file) {
    uploadError.value = '';
    return;
  }

  const reader = new FileReader();
  reader.onload = (e) => {
    try {
      const data = JSON.parse(e.target.result);
      if (!Array.isArray(data)) {
        uploadError.value = 'JSON должен содержать массив объектов';
        return;
      }
      if (data.length === 0) {
        uploadError.value = 'JSON файл пуст';
        return;
      }
      uploadError.value = '';
    } catch (error) {
      uploadError.value = 'Некорректный JSON файл';
    }
  };
  reader.onerror = () => {
    uploadError.value = 'Ошибка при чтении файла';
  };
  reader.readAsText(file);
};

const uploadJson = async () => {
  if (!jsonFile.value || uploadError.value) return;

  isUploading.value = true;
  try {
    const sourceLang = languages.find(l => l.name === selectedPair.value.sourceLanguage)?.iso;
    const targetLang = languages.find(l => l.name === selectedPair.value.targetLanguage)?.iso;

    if (!sourceLang || !targetLang) {
      throw new Error('Не удалось определить языки');
    }

    await languagePairsService.uploadDataset(
      sourceLang,
      targetLang,
      jsonFile.value
    );
    showSuccess('Данные успешно загружены');
    uploadDialog.value = false;
    // Обновляем список карточек после загрузки
    await getLanguageSections();
  } catch (error) {
    if (error.response?.status === 400) {
      uploadError.value = error.response.data.detail;
    } else {
      showError(error.message || 'Ошибка при загрузке данных');
    }
  } finally {
    isUploading.value = false;
  }
};

const validateNewPair = () => {
  newPairErrors.value = {
    sourceLanguage: '',
    targetLanguage: ''
  };
  
  if (!newPair.value.sourceLanguage.trim()) {
    newPairErrors.value.sourceLanguage = 'Введите исходный язык';
  } else if (!languages.some(l => l.name === newPair.value.sourceLanguage)) {
    newPairErrors.value.sourceLanguage = 'Язык не поддерживается';
  }
  
  if (!newPair.value.targetLanguage.trim()) {
    newPairErrors.value.targetLanguage = 'Введите целевой язык';
  } else if (!languages.some(l => l.name === newPair.value.targetLanguage)) {
    newPairErrors.value.targetLanguage = 'Язык не поддерживается';
  }
  
  if (newPair.value.sourceLanguage === newPair.value.targetLanguage) {
    newPairErrors.value.targetLanguage = 'Языки не должны совпадать';
  }
  
  // Проверяем, существует ли уже такая пара
  const pairExists = languagePairs.value.some(
    pair => 
      (pair.sourceLanguage === newPair.value.sourceLanguage && 
       pair.targetLanguage === newPair.value.targetLanguage) ||
      (pair.sourceLanguage === newPair.value.targetLanguage && 
       pair.targetLanguage === newPair.value.sourceLanguage)
  );
  
  if (pairExists) {
    newPairErrors.value.targetLanguage = 'Такая языковая пара уже существует';
  }
  
  return !newPairErrors.value.sourceLanguage && !newPairErrors.value.targetLanguage;
};

const createNewPair = async () => {
  if (!validateNewPair()) {
    return;
  }
  
  isCheckingPair.value = true;
  try {
    const sourceLang = languages.find(l => l.name === newPair.value.sourceLanguage);
    const targetLang = languages.find(l => l.name === newPair.value.targetLanguage);
    
    await languagePairsService.createLanguageSection(
      sourceLang.iso,
      targetLang.iso
    );
    
    await getLanguageSections();
    newPairDialog.value = false;
    showSuccess('Новая языковая пара создана');
  } catch (error) {
    if (error.response?.status === 400) {
      newPairErrors.value.targetLanguage = error.response.data.detail;
    } else {
      showError('Ошибка при создании языковой пары', 'error');
    }
  } finally {
    isCheckingPair.value = false;
  }
};

const openNewPairDialog = () => {
  newPair.value = {
    sourceLanguage: '',
    targetLanguage: ''
  };
  newPairErrors.value = {
    sourceLanguage: '',
    targetLanguage: ''
  };
  newPairDialog.value = true;
};

const getLanguageSections = async () => {
  try {
    const response = await languagePairsService.getLanguageSections();
    languagePairs.value = [];
    
    // Обработка старых пар
    Object.entries(response.data.old).forEach(([sourceLang, targetLang]) => {
      const sourceLanguage = languages.find(l => l.iso === sourceLang)?.name;
      const targetLanguage = languages.find(l => l.iso === targetLang)?.name;
      
      if (sourceLanguage && targetLanguage) {
        languagePairs.value.push({
          sourceLanguage,
          targetLanguage,
          sourceLang: sourceLang,
          targetLang: targetLang,
          isNew: false
        });
      }
    });
    
    // Обработка новых пар
    Object.entries(response.data.new).forEach(([sourceLang, targetLang]) => {
      const sourceLanguage = languages.find(l => l.iso === sourceLang)?.name;
      const targetLanguage = languages.find(l => l.iso === targetLang)?.name;
      
      if (sourceLanguage && targetLanguage) {
        languagePairs.value.push({
          sourceLanguage,
          targetLanguage,
          sourceLang: sourceLang,
          targetLang: targetLang,
          isNew: true
        });
      }
    });
  } catch (error) {
    showError('Ошибка при загрузке языковых пар', 'error');
  }
};

const fileInput = ref(null);

const triggerFileInput = () => {
  fileInput.value.click();
};

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

// Загрузка языковых пар при монтировании компонента
onMounted(async () => {
  await getLanguageSections();
});
</script>

<style scoped>
.learning-container {
  padding: 24px;
  max-width: 1500px;
  margin: 0 auto;
  margin-block: 25px;
  overflow-x: hidden;
  height: 100%;
}

.content-wrapper {
  width: 100%;
}

.learning-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
  position: relative;
}

.language-pairs-list {
  width: 600px;
  transition: all 0.3s ease;
  padding: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: absolute;
  top: 0;
}

.language-pairs-list.shifted {
  transform: translateX(-100%);
  opacity: 0;
  pointer-events: none;
}

.welcome-section {
  text-align: center;
  margin-bottom: 32px;
  color: rgba(0, 0, 0, 0.87);
}

.welcome-section h1 {
  color: rgba(0, 0, 0, 0.87);
  font-weight: 500;
}

.welcome-section p {
  color: rgba(0, 0, 0, 0.6);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-top: 32px;
}

.feature-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(0, 0, 0, 0.12);
}

.feature-card:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.language-pair-item {
  width: 100%;
  padding: 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(0, 0, 0, 0.12);
}

.language-pair-item:hover {
  background-color: rgba(0, 0, 0, 0.05);
  transform: translateY(-2px) scale(1.01);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.language-pair-item.selected {
  border-color: rgba(0, 0, 0, 0.24);
  transform: scale(1.01);
}

.pair-content {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 16px;
}

.language {
  display: flex;
  align-items: center;
  gap: 12px;
}

.language.left {
  justify-content: flex-start;
}

.language.right {
  justify-content: flex-end;
}

.language-name {
  font-size: 1.1rem;
  white-space: nowrap;
}

.center-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  min-width: 80px;
}

.new-chip {
  margin-bottom: 4px;
}

.arrow-icon {
  font-size: 24px;
  color: rgba(0, 0, 0, 0.6);
}

.flag-circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.flag-circle img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.learning-cards-container {
  width: 100%;
  opacity: 0;
  transform: translateX(100%);
  transition: all 0.3s ease;
  pointer-events: none;
}

.learning-cards-container.visible {
  opacity: 1;
  transform: translateX(0);
  pointer-events: all;
}

.cards-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  padding: 16px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(0, 0, 0, 0.12);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.pair-info {
  display: flex;
  flex-direction: column;
}

.stats {
  display: flex;
  gap: 16px;
  color: rgba(0, 0, 0, 0.6);
  font-size: 0.9rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.filters-panel {
  display: flex;
  gap: 16px;
}

.active-filter {
  background-color: rgba(0, 0, 0, 0.05);
}

.learning-cards {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
}

.learning-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 24px;
  position: relative;
  padding-bottom: 80px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(0, 0, 0, 0.12);
}

.learning-card:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.source-text,
.target-text {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #424242;
}

.card-actions {
  position: absolute;
  bottom: 24px;
  left: 24px;
  display: flex;
  gap: 12px;
  align-items: center;
  background: rgba(255, 255, 255, 0.9);
  padding: 4px 8px;
  border-radius: 8px;
  border: 1px solid rgba(0, 0, 0, 0.08);
}

.vote-group {
  display: flex;
  align-items: center;
  gap: 4px;
}

.vote-count {
  font-size: 13px;
  color: rgba(0, 0, 0, 0.6);
  min-width: 20px;
  text-align: center;
}

.card-actions .v-btn {
  width: 32px;
  height: 32px;
  transition: transform 0.2s ease;
}

.card-actions .v-btn:hover {
  transform: scale(1.1);
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 24px;
  padding: 16px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(0, 0, 0, 0.12);
}

.upload-area {
  border: 2px dashed rgba(0, 0, 0, 0.12);
  border-radius: 12px;
  padding: 48px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.upload-area.is-dragging {
  border-color: rgb(var(--v-theme-primary));
  background-color: rgba(var(--v-theme-primary), 0.05);
}

.upload-area:hover {
  border-color: rgba(0, 0, 0, 0.24);
  background-color: rgba(0, 0, 0, 0.02);
}

.file-input {
  display: none;
}

.error-message {
  color: rgb(var(--v-theme-error));
  text-align: center;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
}

.flag-circle-small {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  overflow: hidden;
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-right: 8px;
}

.flag-circle-small img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.v-text-field :deep(.v-field__prepend-inner) {
  padding-top: 0;
  padding-bottom: 0;
  display: flex;
  align-items: center;
}

.selected-file {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;
}

.file-info {
  text-align: center;
}
</style> 