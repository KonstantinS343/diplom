import { evaluationApi, API_CONFIG } from '@/plugins/axios';

export const evaluationService = {
  // Оценка качества перевода
  evaluateTranslation(sourceText, translatedText, sourceLanguage, targetLanguage) {
    return evaluationApi.post(API_CONFIG.evaluation.endpoints.evaluate, {
      source_text: sourceText,
      translated_text: translatedText,
      source_lang: sourceLanguage,
      target_lang: targetLanguage
    });
  },
}; 