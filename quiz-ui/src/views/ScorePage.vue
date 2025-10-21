<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useQuizStore } from '@/stores/quiz'

const props = defineProps<{
  quizId: number
}>()

const router = useRouter()
const quizStore = useQuizStore()

const scorePercentage = computed(() => {
  if (!quizStore.totalQuestions) return 0
  return Math.round((quizStore.score / quizStore.totalQuestions) * 100)
})

const scoreColor = computed(() => {
  if (scorePercentage.value >= 80) return 'text-green-600 dark:text-green-400'
  if (scorePercentage.value >= 60) return 'text-yellow-600 dark:text-yellow-400'
  return 'text-red-600 dark:text-red-400'
})

const scoreMessage = computed(() => {
  if (scorePercentage.value >= 80) return 'Excellent ! 🎉'
  if (scorePercentage.value >= 60) return 'Bien joué ! 👍'
  return 'Continuez à vous entraîner ! 💪'
})

const scoreBorderColor = computed(() => {
  if (scorePercentage.value >= 80) return 'border-green-600'
  if (scorePercentage.value >= 60) return 'border-yellow-600'
  return 'border-red-600'
})

const viewLeaderboard = () => {
  router.push({ name: 'leaderboard', params: { id: props.quizId } })
}

const restartQuiz = () => {
  quizStore.reset()
  router.push({ name: 'quiz-start', params: { id: props.quizId } })
}

const goHome = () => {
  quizStore.reset()
  router.push({ name: 'home' })
}

// Animation du cercle de score
const circumference = 2 * Math.PI * 88
const dashOffset = computed(() => {
  return circumference * (1 - scorePercentage.value / 100)
})
</script>

<template>
  <div class="min-h-screen flex items-center justify-center p-6">
    <div class="card max-w-3xl w-full text-center animate-fade-in">
      <div class="mb-8">
        <h1 class="text-5xl font-black text-gray-900 dark:text-white mb-4">
          Quiz terminé !
        </h1>
        <p class="text-3xl font-bold" :class="scoreColor">
          {{ scoreMessage }}
        </p>
      </div>

      <!-- Score Circle -->
      <div class="flex justify-center mb-12">
        <div class="relative w-64 h-64">
          <svg class="transform -rotate-90 w-64 h-64">
            <circle
              cx="128"
              cy="128"
              r="88"
              stroke="currentColor"
              stroke-width="16"
              fill="transparent"
              class="text-gray-200 dark:text-gray-700"
            />
            <circle
              cx="128"
              cy="128"
              r="88"
              stroke="currentColor"
              stroke-width="16"
              fill="transparent"
              :stroke-dasharray="circumference"
              :stroke-dashoffset="dashOffset"
              class="transition-all duration-2000 ease-out"
              :class="scoreColor"
              stroke-linecap="round"
            />
          </svg>
          <div class="absolute inset-0 flex flex-col items-center justify-center">
            <span class="text-7xl font-black" :class="scoreColor">
              {{ scorePercentage }}%
            </span>
            <span class="text-xl text-gray-600 dark:text-gray-400 font-bold mt-2">
              {{ quizStore.score }} / {{ quizStore.totalQuestions }}
            </span>
          </div>
        </div>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-3 gap-6 mb-12">
        <div class="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/30 dark:to-green-800/30 rounded-2xl p-6 border-2" :class="scoreBorderColor">
          <div class="text-5xl font-black text-green-600 dark:text-green-400 mb-2">
            {{ quizStore.correctAnswers }}
          </div>
          <div class="text-lg font-bold text-gray-700 dark:text-gray-300">
            ✓ Correctes
          </div>
        </div>

        <div class="bg-gradient-to-br from-red-50 to-red-100 dark:from-red-900/30 dark:to-red-800/30 rounded-2xl p-6 border-2 border-red-300 dark:border-red-700">
          <div class="text-5xl font-black text-red-600 dark:text-red-400 mb-2">
            {{ quizStore.wrongAnswers }}
          </div>
          <div class="text-lg font-bold text-gray-700 dark:text-gray-300">
            ✗ Incorrectes
          </div>
        </div>

        <div class="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/30 dark:to-blue-800/30 rounded-2xl p-6 border-2 border-blue-300 dark:border-blue-700">
          <div class="text-5xl font-black text-blue-600 dark:text-blue-400 mb-2">
            {{ quizStore.timeSpent }}s
          </div>
          <div class="text-lg font-bold text-gray-700 dark:text-gray-300">
            ⏱️ Temps
          </div>
        </div>
      </div>

      <!-- Player Name -->
      <div class="mb-10 py-4 px-6 bg-primary-50 dark:bg-primary-900/30 rounded-xl inline-block">
        <span class="text-gray-600 dark:text-gray-400 font-semibold">Joueur :</span>
        <span class="text-2xl font-black text-primary-700 dark:text-primary-300 ml-3">
          {{ quizStore.playerName }}
        </span>
      </div>

      <!-- Actions -->
      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <button class="btn-primary px-8 py-4 text-lg bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800" @click="viewLeaderboard">
          📊 Voir le classement
        </button>
        <button class="btn-secondary px-8 py-4 text-lg" @click="restartQuiz">
          🔄 Recommencer
        </button>
        <button class="btn-secondary px-8 py-4 text-lg" @click="goHome">
          🏠 Accueil
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.duration-2000 {
  transition-duration: 2000ms;
}
</style>
