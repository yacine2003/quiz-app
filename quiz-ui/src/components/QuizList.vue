<script setup lang="ts">
import { computed } from 'vue'
import type { Quiz } from '@/types/models'

const props = defineProps<{
  quizzes: Quiz[]
  loading?: boolean
}>()

const emit = defineEmits<{
  view: [quiz: Quiz]
  edit: [quiz: Quiz]
  delete: [quiz: Quiz]
  create: []
  refresh: []
}>()

const difficultyColor = (difficulty: string) => {
  const colors = {
    easy: 'text-green-600 bg-green-100 dark:text-green-400 dark:bg-green-900/30',
    medium: 'text-yellow-600 bg-yellow-100 dark:text-yellow-400 dark:bg-yellow-900/30',
    hard: 'text-red-600 bg-red-100 dark:text-red-400 dark:bg-red-900/30'
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

const totalQuestions = computed(() => {
  return props.quizzes.reduce((sum, quiz) => sum + (quiz.question_count || 0), 0)
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
          Gestion des quiz
        </h2>
        <p class="text-gray-600 dark:text-gray-400 mt-1">
          {{ quizzes.length }} quiz · {{ totalQuestions }} questions au total
        </p>
      </div>
      <div class="flex gap-3">
        <button 
          @click="emit('refresh')"
          class="px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors flex items-center gap-2"
          :disabled="loading"
        >
          <svg 
            :class="['w-5 h-5', loading && 'animate-spin']" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Actualiser
        </button>
        <button 
          @click="emit('create')"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Nouveau quiz
        </button>
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
      <p class="text-gray-600 dark:text-gray-400 mt-4">Chargement des quiz...</p>
    </div>

    <!-- Empty state -->
    <div v-else-if="quizzes.length === 0" class="text-center py-12 border border-dashed border-gray-300 dark:border-gray-700 rounded-lg">
      <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
      </svg>
      <p class="text-gray-600 dark:text-gray-400 text-lg">Aucun quiz trouvé</p>
      <button 
        @click="emit('create')"
        class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
      >
        Créer le premier quiz
      </button>
    </div>

    <!-- Quiz list -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div 
        v-for="quiz in quizzes" 
        :key="quiz.id"
        class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 hover:shadow-lg transition-shadow cursor-pointer"
        @click="emit('view', quiz)"
      >
        <!-- Header -->
        <div class="flex items-start justify-between mb-4">
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-2">
              <span :class="['text-xs px-2 py-1 rounded-full font-medium', difficultyColor(quiz.difficulty)]">
                {{ difficultyLabel(quiz.difficulty) }}
              </span>
              <span v-if="!quiz.is_published" class="text-xs px-2 py-1 rounded-full bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400">
                Brouillon
              </span>
            </div>
            <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">
              {{ quiz.title }}
            </h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
              {{ quiz.description || 'Aucune description' }}
            </p>
          </div>
        </div>

        <!-- Stats -->
        <div class="flex items-center gap-4 mb-4 text-sm text-gray-600 dark:text-gray-400">
          <div class="flex items-center gap-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{{ quiz.question_count || 0 }} questions</span>
          </div>
          <div class="flex items-center gap-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{{ new Date(quiz.created_at).toLocaleDateString('fr-FR') }}</span>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex gap-2 pt-4 border-t border-gray-200 dark:border-gray-700" @click.stop>
          <button 
            @click="emit('edit', quiz)"
            class="flex-1 px-3 py-2 text-blue-600 hover:bg-blue-50 dark:text-blue-400 dark:hover:bg-blue-900/30 rounded transition-colors text-sm font-medium"
            title="Éditer"
          >
            Éditer
          </button>
          <button 
            @click="emit('delete', quiz)"
            class="flex-1 px-3 py-2 text-red-600 hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-900/30 rounded transition-colors text-sm font-medium"
            title="Supprimer"
          >
            Supprimer
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

