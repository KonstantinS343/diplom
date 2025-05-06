import { learningApi, API_CONFIG } from '@/plugins/axios';

export const languagePairsService = {
  async getLanguageSections() {
    return learningApi.get(API_CONFIG.learning.endpoints.sections);
  },

  async createLanguageSection(sourceLanguage, targetLanguage) {
    return learningApi.post(API_CONFIG.learning.endpoints.section_create, {
      source_lang: sourceLanguage,
      target_lang: targetLanguage
    });
  },

  async uploadDataset(sourceLanguage, targetLanguage, dataset) {
    const formData = new FormData();
    formData.append('file', dataset);
    formData.append('source_lang', sourceLanguage);
    formData.append('target_lang', targetLanguage);

    return learningApi.post(API_CONFIG.learning.endpoints.upload, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      responseType: 'blob'
    });
  },

  async getCards(sourceLang, targetLang) {
    return learningApi.get(API_CONFIG.learning.endpoints.pairs, {
      params: {
        source_lang: sourceLang,
        target_lang: targetLang
      }
    });
  },

}; 