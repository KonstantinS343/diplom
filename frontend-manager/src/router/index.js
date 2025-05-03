import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import NotFoundView from '../views/NotFoundView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import ProfileView from '../views/ProfileView.vue';
import AboutView from '../views/AboutView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta: { requiresAuth: true }
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView
    },
    {
      path: '/404',
      name: 'not-found',
      component: NotFoundView
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/404'
    },
    {
      path: '/translation-evaluation',
      name: 'translation-evaluation',
      component: () => import('../views/TranslationEvaluationView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/learning',
      name: 'learning',
      component: () => import('../views/LearningView.vue')
    },
    {
      path: '/translation-documents',
      name: 'translation-documents',
      component: () => import('../views/TranslationDocumentsView.vue')
    }
  ]
});

// Навигационный guard для проверки аутентификации
// router.beforeEach((to, from, next) => {
//   const isAuthenticated = localStorage.getItem('token'); // TODO: Заменить на реальную проверку

//   if (to.meta.requiresAuth && !isAuthenticated) {
//     next('/login');
//   } else {
//     next();
//   }
// });

export default router; 