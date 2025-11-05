<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { apiClient } from '@/services/api'
import type { Question, Quiz } from '@/types/models'
import QuestionsList from '@/components/QuestionsList.vue'
import QuizList from '@/components/QuizList.vue'

const router = useRouter()
const route = useRoute()
const isAuthenticated = ref(false)
const password = ref('')
const loginError = ref('')
const loading = ref(false)

const questions = ref<Question[]>([])
const quizzes = ref<Quiz[]>([])
const activeTab = ref<'questions' | 'quizzes'>('questions')

onMounted(() => {
  checkAuthentication()
  // Lire le tab depuis l'URL
  const tabParam = route.query.tab as string
  if (tabParam === 'quizzes') {
    activeTab.value = 'quizzes'
  }
})

// Watch pour synchroniser le tab avec l'URL
watch(() => route.query.tab, (newTab) => {
  if (newTab === 'quizzes') {
    activeTab.value = 'quizzes'
  } else {
    activeTab.value = 'questions'
  }
})

// Watch pour charger les données quand on change d'onglet
watch(activeTab, (newTab) => {
  if (newTab === 'questions' && questions.value.length === 0) {
    loadQuestions()
  } else if (newTab === 'quizzes' && quizzes.value.length === 0) {
    loadQuizzes()
  }
})

function checkAuthentication() {
  const token = localStorage.getItem('auth_token')
  isAuthenticated.value = !!token
  
  if (isAuthenticated.value) {
    if (activeTab.value === 'questions') {
      loadQuestions()
    } else {
      loadQuizzes()
    }
  }
}

function switchTab(tab: 'questions' | 'quizzes') {
  activeTab.value = tab
  router.push({ query: { tab: tab === 'quizzes' ? 'quizzes' : undefined } })
}

async function handleLogin() {
  if (!password.value.trim()) {
    loginError.value = 'Veuillez entrer un mot de passe'
    return
  }

  loading.value = true
  loginError.value = ''

  try {
    const response = await apiClient.login(password.value)
    localStorage.setItem('auth_token', response.token)
    isAuthenticated.value = true
    password.value = ''
    await loadQuestions()
  } catch (error: any) {
    console.error('Erreur de connexion:', error)
    loginError.value = error.response?.data?.error || 'Mot de passe incorrect'
  } finally {
    loading.value = false
  }
}

function handleLogout() {
  localStorage.removeItem('auth_token')
  isAuthenticated.value = false
  questions.value = []
  router.push('/')
}

async function loadQuestions() {
  loading.value = true
  try {
    questions.value = await apiClient.fetchAllQuestions()
  } catch (error) {
    console.error('Erreur lors du chargement des questions:', error)
    alert('Erreur lors du chargement des questions')
  } finally {
    loading.value = false
  }
}

async function loadQuizzes() {
  loading.value = true
  try {
    quizzes.value = await apiClient.fetchQuizzes()
  } catch (error) {
    console.error('Erreur lors du chargement des quiz:', error)
    alert('Erreur lors du chargement des quiz')
  } finally {
    loading.value = false
  }
}

function handleCreateQuestion() {
  router.push('/admin/questions/new')
}

function handleEditQuestion(question: Question) {
  router.push(`/admin/questions/${question.id}`)
}

async function handleDeleteQuestion(question: Question) {
  if (!confirm(`Êtes-vous sûr de vouloir supprimer la question "${question.title}" ?`)) {
    return
  }

  loading.value = true
  try {
    await apiClient.deleteQuestion(question.id)
    await loadQuestions()
    alert('Question supprimée avec succès')
  } catch (error) {
    console.error('Erreur lors de la suppression:', error)
    alert('Erreur lors de la suppression de la question')
  } finally {
    loading.value = false
  }
}

// Handlers pour les quiz
function handleCreateQuiz() {
  router.push('/admin/quizzes/new')
}

function handleViewQuiz(quiz: Quiz) {
  router.push(`/admin/quizzes/${quiz.id}`)
}

function handleEditQuiz(quiz: Quiz) {
  router.push(`/admin/quizzes/${quiz.id}/edit`)
}

async function handleDeleteQuiz(quiz: Quiz) {
  if (!confirm(`Êtes-vous sûr de vouloir supprimer le quiz "${quiz.title}" et toutes ses questions ?`)) {
    return
  }

  loading.value = true
  try {
    await apiClient.deleteQuiz(quiz.id)
    await loadQuizzes()
    alert('Quiz supprimé avec succès')
  } catch (error) {
    console.error('Erreur lors de la suppression:', error)
    alert('Erreur lors de la suppression du quiz')
  } finally {
    loading.value = false
  }
}

const questionStats = computed(() => {
  return {
    total: questions.value.length,
    byQuiz: {
      1: questions.value.filter(q => q.quiz_id === 1).length,
      2: questions.value.filter(q => q.quiz_id === 2).length,
      3: questions.value.filter(q => q.quiz_id === 3).length
    },
    byDifficulty: {
      easy: questions.value.filter(q => q.difficulty === 'easy').length,
      medium: questions.value.filter(q => q.difficulty === 'medium').length,
      hard: questions.value.filter(q => q.difficulty === 'hard').length
    }
  }
})
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Login Form -->
    <div v-if="!isAuthenticated" class="min-h-screen flex items-center justify-center p-6">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full p-8">
        <div class="text-center mb-8">
          <div class="inline-flex items-center justify-center w-16 h-16 bg-blue-100 dark:bg-blue-900/30 rounded-full mb-4">
            <svg class="w-8 h-8 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Administration
          </h1>
          <p class="text-gray-600 dark:text-gray-400">
            Connectez-vous pour accéder au panneau d'administration
          </p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Mot de passe
            </label>
            <input 
              v-model="password"
              type="password"
              placeholder="Entrez le mot de passe admin"
              class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              :disabled="loading"
              autofocus
            />
          </div>

          <div v-if="loginError" class="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
            <p class="text-sm text-red-600 dark:text-red-400">{{ loginError }}</p>
          </div>

          <button 
            type="submit"
            :disabled="loading"
            class="w-full px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium flex items-center justify-center gap-2"
          >
            <svg v-if="loading" class="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span>{{ loading ? 'Connexion...' : 'Se connecter' }}</span>
          </button>
        </form>

        <div class="mt-6 text-center">
          <button 
            @click="router.push('/')"
            class="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
          >
            ← Retour à l'accueil
          </button>
        </div>
      </div>
    </div>

    <!-- Admin Dashboard -->
    <div v-else class="min-h-screen">
      <!-- Header -->
      <header class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 sticky top-0 z-40">
        <div class="max-w-7xl mx-auto px-6 py-4">
          <div class="flex items-center justify-between">
            <div>
              <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
                Panneau d'administration
              </h1>
              <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
                Gestion des questions du quiz
              </p>
            </div>
            <div class="flex items-center gap-4">
              <button 
                @click="router.push('/')"
                class="px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
              >
                ← Accueil
              </button>
              <button 
                @click="handleLogout"
                class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center gap-2"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                Déconnexion
              </button>
            </div>
          </div>
        </div>
      </header>

      <!-- Tabs -->
      <div class="max-w-7xl mx-auto px-6 pt-6">
        <div class="border-b border-gray-200 dark:border-gray-700 mb-6">
          <nav class="flex gap-8">
            <button 
              @click="switchTab('questions')"
              :class="[
                'py-4 px-2 border-b-2 font-medium text-sm transition-colors',
                activeTab === 'questions' 
                  ? 'border-blue-600 text-blue-600 dark:border-blue-400 dark:text-blue-400' 
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
              ]"
            >
              Questions
            </button>
            <button 
              @click="switchTab('quizzes')"
              :class="[
                'py-4 px-2 border-b-2 font-medium text-sm transition-colors',
                activeTab === 'quizzes' 
                  ? 'border-blue-600 text-blue-600 dark:border-blue-400 dark:text-blue-400' 
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
              ]"
            >
              Quiz
            </button>
          </nav>
        </div>
      </div>

      <!-- Stats (Questions uniquement) -->
      <div v-if="activeTab === 'questions'" class="max-w-7xl mx-auto px-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-gray-600 dark:text-gray-400">Total questions</p>
                <p class="text-3xl font-bold text-gray-900 dark:text-white mt-1">{{ questionStats.total }}</p>
              </div>
              <div class="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
            </div>
          </div>

          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">Par difficulté</p>
            <div class="space-y-1">
              <div class="flex items-center justify-between text-sm">
                <span class="text-green-600 dark:text-green-400">Facile</span>
                <span class="font-semibold text-gray-900 dark:text-white">{{ questionStats.byDifficulty.easy }}</span>
              </div>
              <div class="flex items-center justify-between text-sm">
                <span class="text-yellow-600 dark:text-yellow-400">Moyen</span>
                <span class="font-semibold text-gray-900 dark:text-white">{{ questionStats.byDifficulty.medium }}</span>
              </div>
              <div class="flex items-center justify-between text-sm">
                <span class="text-red-600 dark:text-red-400">Difficile</span>
                <span class="font-semibold text-gray-900 dark:text-white">{{ questionStats.byDifficulty.hard }}</span>
              </div>
            </div>
          </div>

          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 md:col-span-2">
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">Par quiz</p>
            <div class="grid grid-cols-3 gap-4">
              <div class="text-center">
                <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ questionStats.byQuiz[1] }}</p>
                <p class="text-xs text-gray-600 dark:text-gray-400 mt-1">Quiz 1</p>
              </div>
              <div class="text-center">
                <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ questionStats.byQuiz[2] }}</p>
                <p class="text-xs text-gray-600 dark:text-gray-400 mt-1">Quiz 2</p>
              </div>
              <div class="text-center">
                <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ questionStats.byQuiz[3] }}</p>
                <p class="text-xs text-gray-600 dark:text-gray-400 mt-1">Quiz 3</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Questions List -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <QuestionsList
            :questions="questions"
            :loading="loading"
            @create="handleCreateQuestion"
            @edit="handleEditQuestion"
            @delete="handleDeleteQuestion"
            @refresh="loadQuestions"
          />
        </div>
      </div>

      <!-- Quiz Section -->
      <div v-if="activeTab === 'quizzes'" class="max-w-7xl mx-auto px-6 pb-6">
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <QuizList
            :quizzes="quizzes"
            :loading="loading"
            @create="handleCreateQuiz"
            @view="handleViewQuiz"
            @edit="handleEditQuiz"
            @delete="handleDeleteQuiz"
            @refresh="loadQuizzes"
          />
        </div>
      </div>
    </div>
  </div>
</template>

