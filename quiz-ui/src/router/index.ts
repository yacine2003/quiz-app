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
      component: () => import('@/views/Admin.vue')
      // Note: L'authentification est gérée dans le composant Admin.vue lui-même
    },
    {
      path: '/admin/questions/new',
      name: 'question-create',
      component: () => import('@/views/QuestionEdit.vue')
    },
    {
      path: '/admin/questions/:id',
      name: 'question-detail',
      component: () => import('@/views/QuestionDetail.vue'),
      props: (route) => ({ id: Number(route.params.id) })
    },
    {
      path: '/admin/questions/:id/edit',
      name: 'question-edit',
      component: () => import('@/views/QuestionEdit.vue'),
      props: (route) => ({ id: Number(route.params.id) })
    },
    {
      path: '/admin/quizzes/new',
      name: 'quiz-create',
      component: () => import('@/views/QuizEdit.vue')
    },
    {
      path: '/admin/quizzes/:id',
      name: 'quiz-detail',
      component: () => import('@/views/QuizDetail.vue'),
      props: (route) => ({ id: Number(route.params.id) })
    },
    {
      path: '/admin/quizzes/:id/edit',
      name: 'quiz-edit',
      component: () => import('@/views/QuizEdit.vue'),
      props: (route) => ({ id: Number(route.params.id) })
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

  // Note: L'authentification admin est gérée dans Admin.vue
  // Pas de guard ici pour permettre l'accès au formulaire de connexion

  next()
})

export default router

