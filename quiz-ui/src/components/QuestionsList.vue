<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Question } from '@/types/models'
import QuestionAdminDisplay from './QuestionAdminDisplay.vue'

const props = defineProps<{
  questions: Question[]
  loading?: boolean
}>()

const emit = defineEmits<{
  edit: [question: Question]
  delete: [question: Question]
  create: []
  refresh: []
}>()

const filterQuizId = ref<number | null>(null)
const searchQuery = ref('')

const filteredQuestions = computed(() => {
  let result = [...(props.questions || [])]
  
  // Filtrer par quiz
  if (filterQuizId.value !== null) {
    result = result.filter(q => q.quiz_id === filterQuizId.value)
  }
  
  // Recherche textuelle
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(q => 
      q.title.toLowerCase().includes(query) ||
      q.text.toLowerCase().includes(query) ||
      q.tags?.some(tag => tag.toLowerCase().includes(query))
    )
  }
  
  return result
})

const quizStats = computed(() => {
  const stats = [
    { id: null, label: 'Tous', count: props.questions.length },
    { id: 1, label: 'Quiz 1', count: 0 },
    { id: 2, label: 'Quiz 2', count: 0 },
    { id: 3, label: 'Quiz 3', count: 0 }
  ]
  
  props.questions.forEach(q => {
    const quiz = stats.find(s => s.id === q.quiz_id)
    if (quiz) quiz.count++
  })
  
  return stats
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
          Gestion des questions
        </h2>
        <p class="text-gray-600 dark:text-gray-400 mt-1">
          {{ filteredQuestions.length }} question(s)
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
          class="px-4 py-2 bg-[var(--accent)] text-white rounded-lg hover:bg-[var(--accent-hover)] transition-colors flex items-center gap-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Nouvelle question
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="flex flex-col sm:flex-row gap-4">
      <!-- Quiz filter -->
      <div class="flex gap-2">
        <button
          v-for="stat in quizStats"
          :key="stat.id || 'all'"
          @click="filterQuizId = stat.id"
          :class="[
            'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
            filterQuizId === stat.id
              ? 'bg-[var(--accent)] text-white'
              : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
          ]"
        >
          {{ stat.label }}
          <span class="ml-1 opacity-75">({{ stat.count }})</span>
        </button>
      </div>

      <!-- Search -->
      <div class="flex-1">
        <div class="relative">
          <svg 
            class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input 
            v-model="searchQuery"
            type="text"
            placeholder="Rechercher une question..."
            class="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          />
        </div>
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block w-8 h-8 border-4 border-[var(--accent)] border-t-transparent rounded-full animate-spin"></div>
      <p class="text-gray-600 dark:text-gray-400 mt-4">Chargement des questions...</p>
    </div>

    <!-- Empty state -->
    <div v-else-if="filteredQuestions.length === 0" class="text-center py-12 border border-dashed border-gray-300 dark:border-gray-700 rounded-lg">
      <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <p class="text-gray-600 dark:text-gray-400 text-lg">Aucune question trouvée</p>
      <button 
        @click="emit('create')"
        class="mt-4 px-4 py-2 bg-[var(--accent)] text-white rounded-lg hover:bg-[var(--accent-hover)] transition-colors"
      >
        Créer la première question
      </button>
    </div>

    <!-- Questions list -->
    <div v-else class="space-y-4">
      <QuestionAdminDisplay
        v-for="question in filteredQuestions"
        :key="question.id"
        :question="question"
        @edit="emit('edit', question)"
        @delete="emit('delete', question)"
      />
    </div>
  </div>
</template>

