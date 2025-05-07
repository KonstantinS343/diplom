const API_CONFIG = {
  auth: {
    baseURL: 'http://localhost:1001/v1/api/user',
    endpoints: {
      login: '/login',
      register: '/register',
      logout: '/logout',
      refresh: '/refresh',
      me: '/me'
    }
  },
  translation: {
    baseURL: 'http://localhost:3000/v1/api/translate',
    endpoints: {
      documents: '/docs',
      translate: '/',
      languages: '/langs',
    }
  },
  autocomplete: {
    baseURL: 'http://localhost:1000/v1/api/autocomplete',
    endpoints: {
      autocomplete: '/'
    }
  },
  evaluation: {
    baseURL: 'http://localhost:3001/v1/api/translation',
    endpoints: {
      evaluate: '/quality',
    }
  },
  learning: {
    baseURL: 'http://localhost:3002/v1/api/training',
    endpoints: {
      upload: '/upload',
      dislike: '/dislike',
      like: '/like',
      pairs: '/pairs',
      sections: '/sections',
      section_create: '/section/create',
    }
  }
};

export default API_CONFIG; 