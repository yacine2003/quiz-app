<script setup lang="ts">
import { useRouter } from 'vue-router'

type QuizCard = {
  id: string
  numericId: number
  title: string
  description: string
  difficulty: 'easy' | 'medium' | 'hard'
}

const router = useRouter()

const quizzes: QuizCard[] = [
  {
    id: 'bases',
    numericId: 1,
    title: 'Bases du tennis',
    description: 'Règles et notions essentielles pour débuter.',
    difficulty: 'easy'
  },
  {
    id: 'roland',
    numericId: 2,
    title: 'Roland-Garros',
    description: 'Le tournoi parisien sur terre battue et sa culture.',
    difficulty: 'medium'
  },
  {
    id: 'avance',
    numericId: 3,
    title: 'Tennis avancé',
    description: 'Stratégies, grips, effets et notions techniques.',
    difficulty: 'hard'
  }
]

function start(quiz: QuizCard) {
  router.push({ name: 'quiz-start', params: { id: quiz.numericId } })
}
</script>

<template>
  <main class="min-h-screen p-6 pt-16">
    <div class="max-w-5xl mx-auto">
      <header class="mb-8">
        <h1 class="text-3xl font-black text-gray-900 dark:text-white">Choisissez votre quiz</h1>
        <p class="text-gray-600 dark:text-gray-300">Trois parcours disponibles.</p>
      </header>

      <section class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <article
          v-for="q in quizzes"
          :key="q.id"
          class="card hover:shadow-lg transition-all cursor-pointer"
          @click="start(q)"
        >
          <h2 class="text-xl font-bold mb-2 text-gray-900 dark:text-white">{{ q.title }}</h2>
          <p class="text-gray-600 dark:text-gray-300 mb-4">{{ q.description }}</p>
          <div class="flex items-center justify-between">
            <span
              class="px-3 py-1 rounded-full text-xs font-semibold"
              :class="{
                'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300': q.difficulty === 'easy',
                'bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300': q.difficulty === 'medium',
                'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300': q.difficulty === 'hard'
              }"
            >{{ q.difficulty }}</span>
            <button class="btn-primary">Démarrer →</button>
          </div>
        </article>
      </section>
    </div>
  </main>
</template>


