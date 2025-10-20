/**
 * Configuration Vue Router
 */
import { createRouter, createWebHistory } from 'vue-router'
import { useQuizStore } from '@/stores/quiz'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/Home.vue')
    },
    {
      path: '/quiz',
      name: 'quiz-select',
      component: () => import('@/views/QuizSelection.vue')
    },
    {
      path: '/quiz/:id/start',
      name: 'quiz-start',
      component: () => import('@/views/QuizStart.vue'),
      props: (route) => ({ quizId: Number(route.params.id) })
    },
    {
      path: '/quiz/:id/play',
      name: 'quiz-play',
      component: () => import('@/views/QuizPlay.vue'),
      meta: { requiresQuizInit: true },
      props: (route) => ({ quizId: Number(route.params.id) })
    },
    {
      path: '/quiz/:id/score',
      name: 'score',
      component: () => import('@/views/ScorePage.vue'),
      meta: { requiresQuizCompleted: true },
      props: (route) => ({ quizId: Number(route.params.id) })
    },
    {
      path: '/quiz/:id/leaderboard',
      name: 'leaderboard',
      component: () => import('@/views/Leaderboard.vue'),
      props: (route) => ({ quizId: Number(route.params.id) })
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('@/views/Admin.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/NotFound.vue')
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    return { top: 0 }
  }
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const quizStore = useQuizStore()

  // Vérifier si le quiz est initialisé
  if (to.meta.requiresQuizInit) {
    if (!quizStore.playerName || !quizStore.questions.length) {
      next({ name: 'quiz-start', params: to.params })
      return
    }
  }

  // Vérifier si le quiz est complété
  if (to.meta.requiresQuizCompleted) {
    if (!quizStore.isCompleted) {
      next({ name: 'home' })
      return
    }
  }

  // Vérifier l'authentification admin
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('auth_token')
    if (!token) {
      next({ name: 'home' })
      return
    }
  }

  next()
})

export default router

