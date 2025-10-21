<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useQuery } from '@tanstack/vue-query'
import { useQuizStore } from '@/stores/quiz'
import { fetchQuiz } from '@/services/api'
import { z } from 'zod'

const props = defineProps<{
  quizId: number
}>()

const router = useRouter()
const quizStore = useQuizStore()

const playerName = ref('')
const error = ref('')
const isStarting = ref(false)

const { data: quiz, isLoading } = useQuery({
  queryKey: ['quiz', props.quizId],
  queryFn: () => fetchQuiz(props.quizId)
})

const nameSchema = z
  .string()
  .min(2, 'Minimum 2 caractères')
  .max(20, 'Maximum 20 caractères')
  .regex(/^[a-zA-Z0-9\s]+$/, 'Caractères alphanumériques uniquement')

const startQuiz = async () => {
  try {
    nameSchema.parse(playerName.value)
    error.value = ''
    isStarting.value = true
    
    await quizStore.initializeQuiz(props.quizId, playerName.value)
    router.push({ name: 'quiz-play', params: { id: props.quizId } })
  } catch (e) {
    isStarting.value = false
    if (e instanceof z.ZodError) {
      error.value = e.errors[0].message
    } else {
      error.value = 'Erreur lors du démarrage du quiz'
    }
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center p-6">
    <div class="card max-w-2xl w-full animate-fade-in">
      <!-- Loading -->
      <div v-if="isLoading" class="text-center py-8">
        <div class="loading-spinner mx-auto"></div>
      </div>

      <!-- Quiz Info -->
      <div v-else-if="quiz">
        <div class="text-center mb-8">
          <div class="text-7xl mb-4">🚀</div>
          <h1 class="text-4xl font-black text-gray-900 dark:text-white mb-4">
            {{ quiz.title }}
          </h1>
          <p class="text-xl text-gray-600 dark:text-gray-300 mb-6">
            {{ quiz.description }}
          </p>

          <div class="flex items-center justify-center gap-4 text-gray-600 dark:text-gray-400">
            <div class="flex items-center gap-2">
              <span class="text-2xl">📝</span>
              <span class="font-semibold">{{ quiz.question_count }} questions</span>
            </div>
            <div class="w-1 h-6 bg-gray-300 dark:bg-gray-700"></div>
            <div class="flex items-center gap-2">
              <span class="text-2xl">⏱️</span>
              <span class="font-semibold">~{{ quiz.question_count * 30 }}s</span>
            </div>
            <div class="w-1 h-6 bg-gray-300 dark:bg-gray-700"></div>
            <div>
              <span
                class="px-3 py-1 rounded-full text-sm font-bold"
                :class="{
                  'bg-green-100 text-green-700': quiz.difficulty === 'easy',
                  'bg-yellow-100 text-yellow-700': quiz.difficulty === 'medium',
                  'bg-red-100 text-red-700': quiz.difficulty === 'hard'
                }"
              >
                {{ quiz.difficulty }}
              </span>
            </div>
          </div>
        </div>

        <div class="border-t border-gray-200 dark:border-gray-700 pt-8">
          <form @submit.prevent="startQuiz" class="space-y-6">
            <div>
              <label for="name" class="block text-lg font-bold text-gray-900 dark:text-white mb-3">
                Entrez votre pseudo
              </label>
              <input
                id="name"
                v-model="playerName"
                type="text"
                placeholder="Votre pseudo"
                class="input text-lg"
                :class="{ 'border-red-500': error }"
                autofocus
                maxlength="20"
              />
              <p v-if="error" class="text-red-600 text-sm mt-2 font-semibold">
                ⚠️ {{ error }}
              </p>
              <p v-else class="text-gray-500 dark:text-gray-400 text-sm mt-2">
                Votre pseudo apparaîtra dans le classement
              </p>
            </div>

            <button
              type="submit"
              class="w-full btn-primary py-4 text-xl"
              :class="{ 'opacity-50 cursor-not-allowed': !playerName || isStarting }"
              :disabled="!playerName || isStarting"
            >
              <span v-if="isStarting" class="flex items-center justify-center gap-3">
                <div class="loading-spinner !w-6 !h-6 !border-2"></div>
                Préparation...
              </span>
              <span v-else>
                Démarrer le quiz 🎯
              </span>
            </button>
          </form>
        </div>

        <div class="mt-6 text-center">
          <button
            @click="router.push('/')"
            class="text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
          >
            ← Retour aux quiz
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

