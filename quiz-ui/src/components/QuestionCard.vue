<script setup lang="ts">
import { computed } from 'vue'
import type { Question, Choice } from '@/types/models'

interface Props {
  question: Question
  currentIndex: number
  totalQuestions: number
  selectedChoiceId?: number
}

interface Emits {
  (e: 'answer', choiceId: number): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const progress = computed(() => {
  return ((props.currentIndex + 1) / props.totalQuestions) * 100
})

const selectChoice = (choiceId: number) => {
  emit('answer', choiceId)
}
</script>

<template>
  <div class="card max-w-4xl mx-auto animate-fade-in">
    <!-- Progress Bar -->
    <div class="mb-8">
      <div class="flex justify-between text-sm font-bold text-gray-600 dark:text-gray-400 mb-3">
        <span>Question {{ currentIndex + 1 }} / {{ totalQuestions }}</span>
        <span>{{ Math.round(progress) }}%</span>
      </div>
      <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 overflow-hidden">
        <div
          class="bg-gradient-to-r from-primary-500 to-primary-600 h-full transition-all duration-500 ease-out"
          :style="{ width: `${progress}%` }"
        />
      </div>
    </div>

    <!-- Question Title -->
    <div class="mb-6">
      <div class="flex items-start gap-4 mb-4">
        <div class="flex-shrink-0 w-12 h-12 bg-primary-100 dark:bg-primary-900 rounded-full flex items-center justify-center">
          <span class="text-2xl font-black text-primary-700 dark:text-primary-300">
            {{ currentIndex + 1 }}
          </span>
        </div>
        <h2 class="text-3xl font-black text-gray-900 dark:text-white flex-1">
          {{ question.title }}
        </h2>
      </div>

      <p class="text-xl text-gray-700 dark:text-gray-300 leading-relaxed">
        {{ question.text }}
      </p>
    </div>

    <!-- Question Image -->
    <img
      v-if="question.image"
      :src="question.image"
      :alt="question.title"
      class="w-full rounded-xl mb-8 max-h-96 object-cover shadow-lg"
    />

    <!-- Choices -->
    <div class="space-y-4 mb-8">
      <button
        v-for="(choice, index) in question.choices"
        :key="choice.id"
        class="w-full p-6 rounded-xl border-3 transition-all text-left group relative overflow-hidden"
        :class="[
          selectedChoiceId === choice.id
            ? 'border-primary-600 bg-primary-50 dark:bg-primary-900/30 shadow-lg scale-105'
            : 'border-gray-300 dark:border-gray-600 hover:border-primary-400 bg-white dark:bg-gray-700 hover:shadow-md hover:scale-102'
        ]"
        @click="selectChoice(choice.id)"
      >
        <!-- Choice Number Badge -->
        <div
          class="absolute top-4 left-4 w-10 h-10 rounded-full flex items-center justify-center font-black text-lg transition-all"
          :class="[
            selectedChoiceId === choice.id
              ? 'bg-primary-600 text-white'
              : 'bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-300 group-hover:bg-primary-100 dark:group-hover:bg-primary-900'
          ]"
        >
          {{ String.fromCharCode(65 + index) }}
        </div>

        <!-- Choice Text -->
        <div class="ml-14">
          <span
            class="text-lg font-semibold transition-colors"
            :class="[
              selectedChoiceId === choice.id
                ? 'text-primary-700 dark:text-primary-300'
                : 'text-gray-900 dark:text-white'
            ]"
          >
            {{ choice.text }}
          </span>
        </div>

        <!-- Selection Indicator -->
        <div
          v-if="selectedChoiceId === choice.id"
          class="absolute top-1/2 right-6 -translate-y-1/2"
        >
          <div class="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
            </svg>
          </div>
        </div>
      </button>
    </div>

    <!-- Question Meta -->
    <div class="flex items-center justify-between pt-6 border-t border-gray-200 dark:border-gray-700">
      <span
        class="px-4 py-2 rounded-full text-sm font-bold"
        :class="{
          'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300': question.difficulty === 'easy',
          'bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300': question.difficulty === 'medium',
          'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300': question.difficulty === 'hard'
        }"
      >
        {{ question.difficulty }}
      </span>
      
      <div class="flex gap-2">
        <span
          v-for="tag in question.tags"
          :key="tag"
          class="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg text-sm font-medium"
        >
          #{{ tag }}
        </span>
      </div>
    </div>
  </div>
</template>

