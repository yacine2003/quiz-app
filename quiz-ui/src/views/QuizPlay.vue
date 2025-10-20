<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuizStore } from '@/stores/quiz'
import QuestionCard from '@/components/QuestionCard.vue'

const props = defineProps<{
  quizId: number
}>()

const router = useRouter()
const quizStore = useQuizStore()

const isSubmitting = ref(false)

const currentAnswer = computed(() => {
  return quizStore.getAnswerForQuestion(quizStore.currentIndex)
})

const handleAnswer = (choiceId: number) => {
  quizStore.answerQuestion(choiceId)
}

const handleNext = () => {
  if (quizStore.isLastQuestion) {
    // C'est la dernière question, proposer de terminer
    return
  }
  quizStore.nextQuestion()
}

const handlePrevious = () => {
  quizStore.previousQuestion()
}

const handleSubmit = async () => {
  if (!quizStore.allQuestionsAnswered) {
    return
  }

  isSubmitting.value = true

  try {
    await quizStore.submitQuiz()
    router.push({ name: 'score', params: { id: props.quizId } })
  } catch (error) {
    console.error('Error submitting quiz:', error)
    isSubmitting.value = false
  }
}

// Timer
const elapsedTime = ref(0)
let timerInterval: number | null = null

onMounted(() => {
  timerInterval = window.setInterval(() => {
    elapsedTime.value = quizStore.timeSpent
  }, 1000)
})

onUnmounted(() => {
  if (timerInterval) {
    clearInterval(timerInterval)
  }
})

const formatTime = (seconds: number) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}
</script>

<template>
  <div class="min-h-screen p-6 py-12">
    <div class="max-w-5xl mx-auto">
      <!-- Header with Timer -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h3 class="text-2xl font-black text-gray-900 dark:text-white">
            {{ quizStore.playerName }}
          </h3>
          <p class="text-gray-600 dark:text-gray-400">
            Question {{ quizStore.currentIndex + 1 }} sur {{ quizStore.totalQuestions }}
          </p>
        </div>
        
        <div class="flex items-center gap-4">
          <!-- Timer -->
          <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg px-6 py-3 border border-gray-200 dark:border-gray-700">
            <div class="flex items-center gap-3">
              <span class="text-2xl">⏱️</span>
              <span class="text-2xl font-black text-gray-900 dark:text-white">
                {{ formatTime(elapsedTime) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Question Card -->
      <QuestionCard
        v-if="quizStore.currentQuestion"
        :question="quizStore.currentQuestion"
        :current-index="quizStore.currentIndex"
        :total-questions="quizStore.totalQuestions"
        :selected-choice-id="currentAnswer?.choice_id"
        @answer="handleAnswer"
      />

      <!-- Navigation Buttons -->
      <div class="mt-8 flex items-center justify-between gap-4">
        <button
          @click="handlePrevious"
          class="btn-secondary px-8 py-4 text-lg"
          :class="{ 'opacity-50 cursor-not-allowed': !quizStore.canGoPrevious }"
          :disabled="!quizStore.canGoPrevious"
        >
          ← Précédent
        </button>

        <div class="flex-1 text-center">
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">
            {{ quizStore.answers.size }} / {{ quizStore.totalQuestions }} réponses
          </p>
          <div class="flex items-center justify-center gap-2">
            <div
              v-for="i in quizStore.totalQuestions"
              :key="i"
              class="w-2 h-2 rounded-full transition-all"
              :class="[
                quizStore.answers.has(i - 1)
                  ? 'bg-primary-600 w-3 h-3'
                  : 'bg-gray-300 dark:bg-gray-600'
              ]"
            />
          </div>
        </div>

        <button
          v-if="!quizStore.isLastQuestion"
          @click="handleNext"
          class="btn-primary px-8 py-4 text-lg"
          :class="{ 'opacity-50 cursor-not-allowed': !quizStore.canGoNext }"
          :disabled="!quizStore.canGoNext"
        >
          Suivant →
        </button>

        <button
          v-else
          @click="handleSubmit"
          class="btn-primary px-8 py-4 text-lg bg-green-600 hover:bg-green-700"
          :class="{ 'opacity-50 cursor-not-allowed': !quizStore.allQuestionsAnswered || isSubmitting }"
          :disabled="!quizStore.allQuestionsAnswered || isSubmitting"
        >
          <span v-if="isSubmitting" class="flex items-center gap-3">
            <div class="loading-spinner !w-5 !h-5 !border-2"></div>
            Envoi...
          </span>
          <span v-else>
            Terminer ✓
          </span>
        </button>
      </div>

      <!-- Question Navigator -->
      <div class="mt-12 card bg-gray-50 dark:bg-gray-900">
        <h4 class="text-lg font-black text-gray-900 dark:text-white mb-4">
          Navigation rapide
        </h4>
        <div class="grid grid-cols-5 sm:grid-cols-10 gap-2">
          <button
            v-for="i in quizStore.totalQuestions"
            :key="i"
            @click="quizStore.goToQuestion(i - 1)"
            class="aspect-square rounded-lg font-bold transition-all"
            :class="[
              i - 1 === quizStore.currentIndex
                ? 'bg-primary-600 text-white scale-110 shadow-lg'
                : quizStore.answers.has(i - 1)
                ? 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300 hover:bg-green-200'
                : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300'
            ]"
          >
            {{ i }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

