<script setup lang="ts">
import { computed } from 'vue'
import type { Question } from '@/types/models'

const props = defineProps<{
  question: Question
}>()

const emit = defineEmits<{
  edit: [question: Question]
  delete: [question: Question]
}>()

const difficultyColor = computed(() => {
  const colors = {
    easy: 'text-green-600 bg-green-100 dark:text-green-400 dark:bg-green-900/30',
    medium: 'text-yellow-600 bg-yellow-100 dark:text-yellow-400 dark:bg-yellow-900/30',
    hard: 'text-red-600 bg-red-100 dark:text-red-400 dark:bg-red-900/30'
  }
  return colors[props.question.difficulty] || colors.easy
})

const difficultyLabel = computed(() => {
  const labels = {
    easy: 'Facile',
    medium: 'Moyen',
    hard: 'Difficile'
  }
  return labels[props.question.difficulty] || 'Facile'
})

// Fallback image (au cas où l'API renverrait image = null)
const adminImageSrc = computed(() => {
  const q = props.question
  const diff = (q.difficulty || 'easy').toLowerCase()
  const suffix = diff === 'easy' ? 'base' : diff
  return q.image || `/images/questions/q${q.position}${suffix}.png`
})
</script>

<template>
  <div class="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-md transition-shadow">
    <!-- Header -->
    <div class="flex items-start justify-between mb-3">
      <div class="flex-1">
        <div class="flex items-center gap-2 mb-1">
          <span class="text-sm font-mono text-gray-500 dark:text-gray-400">
            #{{ question.position }}
          </span>
          <span :class="['text-xs px-2 py-1 rounded-full font-medium', difficultyColor]">
            {{ difficultyLabel }}
          </span>
          <span v-if="question.quiz_id" class="text-xs px-2 py-1 rounded-full bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400">
            Quiz {{ question.quiz_id }}
          </span>
        </div>
        <h3 class="font-semibold text-gray-900 dark:text-white">
          {{ question.title }}
        </h3>
      </div>
      
      <!-- Actions -->
      <div class="flex gap-2 ml-4">
        <button 
          @click="emit('edit', question)"
          class="p-2 text-blue-600 hover:bg-blue-50 dark:text-blue-400 dark:hover:bg-blue-900/30 rounded transition-colors"
          title="Éditer"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
        </button>
        <button 
          @click="emit('delete', question)"
          class="p-2 text-red-600 hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-900/30 rounded transition-colors"
          title="Supprimer"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Question text -->
    <p class="text-gray-700 dark:text-gray-300 mb-3">
      {{ question.text }}
    </p>

    <!-- Image preview -->
    <div v-if="adminImageSrc" class="mb-3">
      <img 
        :src="adminImageSrc" 
        :alt="question.title"
        class="max-h-32 rounded border border-gray-200 dark:border-gray-700"
      />
    </div>

    <!-- Choices -->
    <div class="space-y-2 mb-3">
      <div 
        v-for="(choice, index) in question.choices" 
        :key="choice.id"
        :class="[
          'p-2 rounded text-sm border',
          choice.is_correct 
            ? 'bg-green-50 border-green-300 text-green-800 dark:bg-green-900/20 dark:border-green-700 dark:text-green-300' 
            : 'bg-gray-50 border-gray-200 text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-300'
        ]"
      >
        <span class="font-medium">{{ String.fromCharCode(65 + index) }}.</span>
        {{ choice.text }}
        <span v-if="choice.is_correct" class="ml-2 text-green-600 dark:text-green-400">✓</span>
      </div>
    </div>

    <!-- Tags -->
    <div v-if="question.tags && question.tags.length > 0" class="flex flex-wrap gap-1 mb-2">
      <span 
        v-for="tag in question.tags" 
        :key="tag"
        class="text-xs px-2 py-1 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 rounded"
      >
        {{ tag }}
      </span>
    </div>

    <!-- Explanation -->
    <div v-if="question.explanation" class="text-sm text-gray-600 dark:text-gray-400 italic border-t border-gray-200 dark:border-gray-700 pt-2 mt-2">
      <strong>Explication :</strong> {{ question.explanation }}
    </div>
  </div>
</template>

