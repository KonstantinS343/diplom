const API_CONFIG = {
  auth: {
    baseURL: 'http://localhost:8000/api/auth',
    endpoints: {
      login: '/login',
      register: '/register',
      logout: '/logout',
      refresh: '/refresh'
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
    baseURL: 'http://localhost:8003/api/learning',
    endpoints: {
      courses: '/courses',
      lessons: '/lessons',
      progress: '/progress'
    }
  }
};

export default API_CONFIG; 