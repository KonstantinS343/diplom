import { translationApi, autocompleteApi, API_CONFIG } from '@/plugins/axios';

export const translationService = {
  // Получение списка поддерживаемых языков
  getSupportedLanguages() {
    return translationApi.get(API_CONFIG.translation.endpoints.languages);
  },

  // Перевод текста
  translateText(sourceText, sourceLanguage, targetLanguage, signal) {
    return translationApi.post(API_CONFIG.translation.endpoints.translate, {
      text: sourceText,
      source_lang: sourceLanguage,
      target_lang: targetLanguage
    }, { signal });
  },

  // Автодополнение
  autocomplete(text, cursorPosition, language) {
    return autocompleteApi.post(API_CONFIG.autocomplete.endpoints.autocomplete, {
      text: text,
      position: cursorPosition,
      language: language
    });
  },

  // Получение альтернативных переводов
  getAlternativeTranslations(text, sourceLanguage, targetLanguage) {
    return translationApi.post(API_CONFIG.translation.endpoints.alternatives, {
      text,
      source_lang: sourceLanguage,
      target_lang: targetLanguage
    });
  },

  // Перевод документа
  translateDocument(file, sourceLanguage, targetLanguage) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('source_lang', sourceLanguage);
    formData.append('target_lang', targetLanguage);

    return translationApi.post(API_CONFIG.translation.endpoints.documents, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      responseType: 'blob'
    });
  }
}; 