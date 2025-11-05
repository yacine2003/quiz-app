<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { apiClient } from '@/services/api'
import type { Quiz, Question } from '@/types/models'

const router = useRouter()
const route = useRoute()
const quiz = ref<Quiz | null>(null)
const questions = ref<Question[]>([])
const loading = ref(false)

onMounted(async () => {
  await loadQuiz()
})

async function loadQuiz() {
  loading.value = true
  try {
    const quizId = Number(route.params.id)
    quiz.value = await apiClient.fetchQuiz(quizId)
    questions.value = await apiClient.fetchQuestions(quizId)
  } catch (error) {
    console.error('Erreur lors du chargement du quiz:', error)
    alert('Erreur lors du chargement du quiz')
    router.push('/admin')
  } finally {
    loading.value = false
  }
}

async function handleDelete() {
  if (!quiz.value) return
  
  if (!confirm(`Êtes-vous sûr de vouloir supprimer le quiz "${quiz.value.title}" et toutes ses questions ?`)) {
    return
  }

  loading.value = true
  try {
    await apiClient.deleteQuiz(quiz.value.id)
    alert('Quiz supprimé avec succès')
    router.push('/admin?tab=quizzes')
  } catch (error) {
    console.error('Erreur lors de la suppression:', error)
    alert('Erreur lors de la suppression du quiz')
  } finally {
    loading.value = false
  }
}

function handleEdit() {
  if (!quiz.value) return
  router.push(`/admin/quizzes/${quiz.value.id}/edit`)
}

function handleBack() {
  router.push('/admin?tab=quizzes')
}

function handleLogout() {
  localStorage.removeItem('auth_token')
  router.push('/')
}

const difficultyColor = (difficulty: string) => {
  const colors = {
    easy: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400',
    medium: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400',
    hard: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
  }
  return colors[difficulty as keyof typeof colors] || colors.easy
}

const difficultyLabel = (difficulty: string) => {
  const labels = {
    easy: 'Facile',
    medium: 'Moyen',
    hard: 'Difficile'
  }
  return labels[difficulty as keyof typeof labels] || 'Facile'
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Header -->
    <header class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 sticky top-0 z-40">
      <div class="max-w-5xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <button 
            @click="handleBack"
            class="flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            Retour à la liste
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
    </header>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center min-h-[60vh]">
      <div class="text-center">
        <div class="inline-block w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-4"></div>
        <p class="text-gray-600 dark:text-gray-400">Chargement...</p>
      </div>
    </div>

    <!-- Quiz Detail -->
    <div v-else-if="quiz" class="max-w-5xl mx-auto px-6 py-8">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
        <!-- Header with actions -->
        <div class="border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 px-6 py-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <span :class="['text-sm px-3 py-1 rounded-full font-medium', difficultyColor(quiz.difficulty)]">
                {{ difficultyLabel(quiz.difficulty) }}
              </span>
              <span v-if="!quiz.is_published" class="text-sm px-3 py-1 rounded-full bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400">
                Brouillon
              </span>
            </div>
            <div class="flex gap-3">
              <button 
                @click="handleEdit"
                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                Éditer
              </button>
              <button 
                @click="handleDelete"
                class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center gap-2"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                Supprimer
              </button>
            </div>
          </div>
        </div>

        <!-- Quiz Content -->
        <div class="p-6 space-y-6">
          <!-- Title -->
          <div>
            <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
              Titre du quiz
            </h3>
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
              {{ quiz.title }}
            </h1>
          </div>

          <!-- Description -->
          <div>
            <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
              Description
            </h3>
            <p class="text-lg text-gray-700 dark:text-gray-300">
              {{ quiz.description || 'Aucune description' }}
            </p>
          </div>

          <!-- Stats -->
          <div class="grid grid-cols-3 gap-4">
            <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
              <div class="text-blue-600 dark:text-blue-400 text-sm font-medium mb-1">Questions</div>
              <div class="text-2xl font-bold text-blue-900 dark:text-blue-100">{{ quiz.question_count || 0 }}</div>
            </div>
            <div class="bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800 rounded-lg p-4">
              <div class="text-purple-600 dark:text-purple-400 text-sm font-medium mb-1">Statut</div>
              <div class="text-lg font-bold text-purple-900 dark:text-purple-100">
                {{ quiz.is_published ? 'Publié' : 'Brouillon' }}
              </div>
            </div>
            <div class="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
              <div class="text-green-600 dark:text-green-400 text-sm font-medium mb-1">Créé le</div>
              <div class="text-sm font-bold text-green-900 dark:text-green-100">
                {{ new Date(quiz.created_at).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }) }}
              </div>
            </div>
          </div>

          <!-- Questions list -->
          <div v-if="questions.length > 0">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              Questions de ce quiz ({{ questions.length }})
            </h3>
            <div class="space-y-2">
              <div 
                v-for="question in questions" 
                :key="question.id"
                class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors cursor-pointer"
                @click="router.push(`/admin/questions/${question.id}`)"
              >
                <div class="flex items-center gap-3 flex-1">
                  <span class="text-sm font-mono text-gray-500 dark:text-gray-400 w-8">
                    #{{ question.position }}
                  </span>
                  <span class="text-gray-900 dark:text-white font-medium">
                    {{ question.title }}
                  </span>
                </div>
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-12 border border-dashed border-gray-300 dark:border-gray-700 rounded-lg">
            <svg class="w-12 h-12 mx-auto text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <p class="text-gray-600 dark:text-gray-400">Aucune question dans ce quiz</p>
            <button 
              @click="router.push('/admin?tab=questions')"
              class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Ajouter des questions
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

