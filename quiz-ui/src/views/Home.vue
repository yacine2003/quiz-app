<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useQuery } from '@tanstack/vue-query'
import { fetchQuizzes } from '@/services/api'

const router = useRouter()

const { data: quizzes, isLoading, error } = useQuery({
  queryKey: ['quizzes'],
  queryFn: fetchQuizzes
})

const startQuiz = (quizId: number) => {
  router.push({ name: 'quiz-start', params: { id: quizId } })
}
</script>

<template>
  <div class="min-h-screen p-6">
    <div class="max-w-6xl mx-auto">
      <header class="text-center mb-16 pt-16 animate-fade-in">
        <div class="mb-6">
          <div class="inline-block text-8xl animate-pulse">🎯</div>
        </div>
        <h1 class="text-6xl font-black text-gray-900 dark:text-white mb-4">
          Quiz App
        </h1>
        <p class="text-2xl text-gray-600 dark:text-gray-300">
          Testez vos connaissances et défiez le leaderboard !
        </p>
      </header>

      <!-- Loading -->
      <div v-if="isLoading" class="text-center py-12">
        <div class="loading-spinner mx-auto"></div>
        <p class="text-gray-600 dark:text-gray-400 mt-4">Chargement des quiz...</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="text-center py-12">
        <div class="text-6xl mb-4">⚠️</div>
        <p class="text-red-600 text-lg">Erreur de chargement des quiz</p>
      </div>

      <!-- Quiz List -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 animate-fade-in">
        <article
          v-for="quiz in quizzes"
          :key="quiz.id"
          class="card hover:shadow-2xl transition-all cursor-pointer group transform hover:scale-105"
          @click="startQuiz(quiz.id)"
        >
          <div class="flex items-start justify-between mb-6">
            <h2 class="text-3xl font-black text-gray-900 dark:text-white group-hover:text-primary-600 transition-colors">
              {{ quiz.title }}
            </h2>
            <span class="px-4 py-2 bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300 rounded-full text-sm font-bold">
              {{ quiz.question_count }} Q
            </span>
          </div>
          
          <p class="text-gray-600 dark:text-gray-300 mb-6 text-lg">
            {{ quiz.description }}
          </p>
          
          <div class="flex items-center justify-between pt-4 border-t border-gray-200 dark:border-gray-700">
            <span
              class="px-3 py-1 rounded-full text-sm font-medium"
              :class="{
                'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300': quiz.difficulty === 'easy',
                'bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300': quiz.difficulty === 'medium',
                'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300': quiz.difficulty === 'hard'
              }"
            >
              {{ quiz.difficulty }}
            </span>
            <button class="btn-primary">
              Commencer →
            </button>
          </div>
        </article>
      </div>

      <!-- No quizzes -->
      <div v-if="!isLoading && quizzes && quizzes.length === 0" class="text-center py-20">
        <div class="text-8xl mb-6">📝</div>
        <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Aucun quiz disponible
        </h3>
        <p class="text-gray-600 dark:text-gray-400">
          Revenez plus tard ou contactez l'administrateur.
        </p>
      </div>
    </div>
  </div>
</template>

