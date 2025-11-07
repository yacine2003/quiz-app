<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { apiClient } from '@/services/api'
import type { Question } from '@/types/models'

const router = useRouter()
const route = useRoute()
const question = ref<Question | null>(null)
const loading = ref(false)

onMounted(async () => {
  await loadQuestion()
})

async function loadQuestion() {
  loading.value = true
  try {
    const questionId = Number(route.params.id)
    question.value = await apiClient.fetchQuestionById(questionId)
  } catch (error) {
    console.error('Erreur lors du chargement de la question:', error)
    alert('Erreur lors du chargement de la question')
    router.push('/admin')
  } finally {
    loading.value = false
  }
}

async function handleDelete() {
  if (!question.value) return
  
  if (!confirm(`Êtes-vous sûr de vouloir supprimer la question "${question.value.title}" ?`)) {
    return
  }

  loading.value = true
  try {
    await apiClient.deleteQuestion(question.value.id)
    alert('Question supprimée avec succès')
    router.push('/admin')
  } catch (error) {
    console.error('Erreur lors de la suppression:', error)
    alert('Erreur lors de la suppression de la question')
  } finally {
    loading.value = false
  }
}

function handleEdit() {
  if (!question.value) return
  router.push(`/admin/questions/${question.value.id}/edit`)
}

function handleBack() {
  router.push('/admin')
}

function handleLogout() {
  localStorage.removeItem('auth_token')
  router.push('/')
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Header -->
    <header class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 sticky top-0 z-40">
      <div class="max-w-4xl mx-auto px-6 py-4">
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

    <!-- Question Detail -->
    <div v-else-if="question" class="max-w-4xl mx-auto px-6 py-8">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
        <!-- Header with actions -->
        <div class="border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 px-6 py-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <span class="text-sm font-mono text-gray-500 dark:text-gray-400">
                Question #{{ question.position }}
              </span>
              <span class="text-xs px-2 py-1 rounded-full bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400">
                Quiz {{ question.quiz_id }}
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

        <!-- Question Content -->
        <div class="p-6 space-y-6">
          <!-- Title -->
          <div>
            <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
              Titre de la question
            </h3>
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
              {{ question.title }}
            </h1>
          </div>

          <!-- Question text -->
          <div>
            <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
              Intitulé de la question
            </h3>
            <p class="text-lg text-gray-700 dark:text-gray-300">
              {{ question.text }}
            </p>
          </div>

          <!-- Image -->
          <div v-if="question.image">
            <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
              Image
            </h3>
            <img 
              :src="question.image" 
              :alt="question.title"
              class="max-w-full h-auto rounded-lg border border-gray-200 dark:border-gray-700"
            />
          </div>

          <!-- Difficulty -->
          <div>
            <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
              Difficulté
            </h3>
            <span 
              :class="[
                'inline-flex px-3 py-1 rounded-full text-sm font-medium',
                question.difficulty === 'easy' ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' :
                question.difficulty === 'medium' ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400' :
                'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
              ]"
            >
              {{ question.difficulty === 'easy' ? 'Facile' : question.difficulty === 'medium' ? 'Moyen' : 'Difficile' }}
            </span>
          </div>

          <!-- Possible answers -->
          <div>
            <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">
              Liste des réponses possibles
            </h3>
            <div class="space-y-3">
              <div 
                v-for="(choice, index) in question.choices" 
                :key="choice.id"
                :class="[
                  'p-4 rounded-lg border-2 transition-all',
                  choice.is_correct 
                    ? 'border-green-500 bg-green-50 dark:bg-green-900/20' 
                    : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800'
                ]"
              >
                <div class="flex items-start gap-3">
                  <div :class="[
                    'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center font-semibold text-sm',
                    choice.is_correct 
                      ? 'bg-green-500 text-white' 
                      : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
                  ]">
                    {{ String.fromCharCode(65 + index) }}
                  </div>
                  <div class="flex-1">
                    <p :class="[
                      'text-base',
                      choice.is_correct 
                        ? 'text-green-900 dark:text-green-100 font-medium' 
                        : 'text-gray-700 dark:text-gray-300'
                    ]">
                      {{ choice.text }}
                    </p>
                    <p v-if="choice.is_correct" class="text-sm text-green-600 dark:text-green-400 mt-1 flex items-center gap-1">
                      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                      </svg>
                      Bonne réponse
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Tags -->
          <div v-if="question.tags && question.tags.length > 0">
            <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
              Tags
            </h3>
            <div class="flex flex-wrap gap-2">
              <span 
                v-for="tag in question.tags" 
                :key="tag"
                class="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full text-sm"
              >
                {{ tag }}
              </span>
            </div>
          </div>

          <!-- Explanation -->
          <div v-if="question.explanation">
            <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
              Explication
            </h3>
            <div class="p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
              <p class="text-gray-700 dark:text-gray-300">
                {{ question.explanation }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

