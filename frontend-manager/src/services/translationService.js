import api from '@/plugins/axios';

export const translationService = {
  // Получение списка поддерживаемых языков
  getSupportedLanguages() {
    return api.get('/languages');
  },

  // Перевод текста
  translateText(sourceText, sourceLanguage, targetLanguage) {
    return api.post('/translate', {
      text: sourceText,
      source_language: sourceLanguage,
      target_language: targetLanguage
    });
  },

  // Получение альтернативных переводов
  getAlternativeTranslations(text, sourceLanguage, targetLanguage) {
    return api.post('/translate/alternatives', {
      text,
      source_language: sourceLanguage,
      target_language: targetLanguage
    });
  }
}; 