<template>
  <div class="documents-container">
    <div class="content-wrapper">
      <!-- Заголовок страницы -->
      <div class="page-header">
        <h1 class="text-h4 mb-2">Перевод документов</h1>
        <p class="text-body-1 text-medium-emphasis">
          Загрузите документ и получите профессиональный перевод с сохранением форматирования
        </p>
      </div>

      <v-row justify="center">
        <v-col cols="12" md="10">
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
        </v-col>
      </v-row>

      <v-row justify="center">
        <v-col cols="12" md="10">
          <v-card
            flat
            class="upload-card"
            :class="{ 'is-dragging': isDragging }"
            @dragover.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
            @drop.prevent="handleFileDrop"
          >
            <div class="upload-content" @click="triggerFileInput">
              <input
                ref="fileInput"
                type="file"
                accept=".doc,.docx,.xlsx,.pptx"
                class="file-input"
                @change="handleFileSelect"
              />
              <v-icon
                :icon="uploadedFile ? 'mdi-file-document' : 'mdi-cloud-upload'"
                size="64"
                color="grey-darken-2"
                class="mb-4"
              ></v-icon>
              <div class="upload-text">
                <template v-if="!uploadedFile">
                  <div class="text-h6 mb-2">Перетащите файл сюда</div>
                  <div class="text-body-1 text-medium-emphasis">или нажмите для выбора файла</div>
                  <div class="text-caption text-medium-emphasis mt-2">
                    Поддерживаемые форматы: .doc, .docx, .xlsx, .pptx
                  </div>
                </template>
                <template v-else>
                  <div class="text-h6 mb-2">{{ uploadedFile.name }}</div>
                  <div class="text-body-1 text-medium-emphasis">
                    {{ formatFileSize(uploadedFile.size) }}
                  </div>
                </template>
              </div>
            </div>
          </v-card>
        </v-col>
      </v-row>

      <v-row justify="center" class="mt-4">
        <v-col cols="auto">
          <v-btn
            color="grey-darken-2"
            size="large"
            @click="translateDocument"
            :loading="isTranslating"
            :disabled="!uploadedFile"
          >
            Перевести
          </v-btn>
        </v-col>
      </v-row>

      <v-expand-transition>
        <v-row v-if="translatedFile" justify="center" class="mt-4">
          <v-col cols="auto">
            <v-btn
              color="grey-darken-2"
              size="large"
              prepend-icon="mdi-download"
              @click="downloadTranslatedFile"
            >
              Скачать переведенный документ
            </v-btn>
          </v-col>
        </v-row>
      </v-expand-transition>

      <!-- Как это работает -->
      <div class="how-it-works mt-12">
        <h2 class="text-h5 mb-4">Как это работает</h2>
        <v-row>
          <v-col cols="12" md="4">
            <v-card class="step-card">
              <div class="step-number">1</div>
              <h3 class="text-h6 mt-4">Загрузите документ</h3>
              <p class="text-body-2">Выберите файл в формате DOC, DOCX, XLSX или PPTX</p>
            </v-card>
          </v-col>
          <v-col cols="12" md="4">
            <v-card class="step-card">
              <div class="step-number">2</div>
              <h3 class="text-h6 mt-4">Выберите языки</h3>
              <p class="text-body-2">Укажите исходный и целевой языки перевода</p>
            </v-card>
          </v-col>
          <v-col cols="12" md="4">
            <v-card class="step-card">
              <div class="step-number">3</div>
              <h3 class="text-h6 mt-4">Получите результат</h3>
              <p class="text-body-2">Скачайте переведенный документ с сохранением форматирования</p>
            </v-card>
          </v-col>
        </v-row>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useSnackbar } from '@/composables/useSnackbar';

const { showSnackbar } = useSnackbar();

const languages = [
  'Русский',
  'Английский',
  'Немецкий',
  'Французский',
  'Испанский',
  'Итальянский',
  'Китайский',
  'Японский'
];

const sourceLanguage = ref('Русский');
const targetLanguage = ref('Английский');
const uploadedFile = ref(null);
const translatedFile = ref(null);
const isDragging = ref(false);
const isTranslating = ref(false);
const fileInput = ref(null);

const swapLanguages = () => {
  const temp = sourceLanguage.value;
  sourceLanguage.value = targetLanguage.value;
  targetLanguage.value = temp;
};

const triggerFileInput = () => {
  fileInput.value.click();
};

const handleFileSelect = (event) => {
  const file = event.target.files[0];
  if (file) {
    uploadedFile.value = file;
  }
};

const handleFileDrop = (event) => {
  isDragging.value = false;
  const file = event.dataTransfer.files[0];
  if (file) {
    uploadedFile.value = file;
  }
};

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

const translateDocument = async () => {
  if (!uploadedFile.value) return;

  isTranslating.value = true;
  try {
    // Здесь будет API запрос для перевода документа
    await new Promise(resolve => setTimeout(resolve, 2000)); // Имитация запроса
    translatedFile.value = {
      name: `translated_${uploadedFile.value.name}`,
      url: '#' // Здесь будет URL для скачивания
    };
    showSnackbar('Документ успешно переведен', 'success');
  } catch (error) {
    showSnackbar('Произошла ошибка при переводе документа', 'error');
  } finally {
    isTranslating.value = false;
  }
};

const downloadTranslatedFile = () => {
  // Здесь будет логика скачивания файла
  showSnackbar('Начато скачивание файла', 'success');
};
</script>

<style scoped>
.documents-container {
  padding: 24px;
  max-width: 1500px;
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

.upload-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  border: 2px dashed transparent;
}

.upload-card.is-dragging {
  border-color: #424242;
  background-color: rgba(66, 66, 66, 0.05);
}

.upload-content {
  padding: 48px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  min-height: 600px;
}

.file-input {
  display: none;
}

.upload-text {
  color: #424242;
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

.how-it-works {
  margin-top: 48px;
}

.how-it-works h2 {
  color: rgba(0, 0, 0, 0.87);
  font-weight: 500;
}

.step-card {
  background: white;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(0, 0, 0, 0.12);
  position: relative;
  height: 100%;
}

.step-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.step-number {
  width: 40px;
  height: 40px;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.87);
  margin: 0 auto;
}

.step-card h3 {
  color: rgba(0, 0, 0, 0.87);
  font-weight: 500;
  margin-top: 16px;
}

.step-card p {
  color: rgba(0, 0, 0, 0.6);
  margin-top: 8px;
}
</style>
