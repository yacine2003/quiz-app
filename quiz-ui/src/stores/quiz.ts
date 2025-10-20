/**
 * Store Pinia pour gérer l'état du quiz
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useLocalStorage } from '@vueuse/core'
import type { Question, Answer, AttemptRequest } from '@/types/models'
import { fetchQuestions, submitAttempt } from '@/services/api'

export const useQuizStore = defineStore('quiz', () => {
  // State
  const quizId = ref<number>(0)
  const playerName = ref<string>('')
  const questions = ref<Question[]>([])
  const currentIndex = ref(0)
  const answers = ref<Map<number, Answer>>(new Map())
  const startTime = ref<number>(0)
  const endTime = ref<number>(0)
  const isCompleted = ref(false)
  const attemptId = ref<number | null>(null)

  // Persistent state (localStorage)
  const savedProgress = useLocalStorage('quiz-progress', {
    quizId: 0,
    currentIndex: 0,
    answers: [] as Answer[],
    startTime: 0
  })

  // Computed
  const currentQuestion = computed(() => questions.value[currentIndex.value])

  const totalQuestions = computed(() => questions.value.length)

  const score = computed(() => {
    return Array.from(answers.value.values()).filter((a) => a.is_correct).length
  })

  const correctAnswers = computed(() => score.value)

  const wrongAnswers = computed(() => answers.value.size - score.value)

  const timeSpent = computed(() => {
    if (!startTime.value) return 0
    const end = endTime.value || Date.now()
    return Math.floor((end - startTime.value) / 1000)
  })

  const progress = computed(() => {
    if (!totalQuestions.value) return 0
    return Math.round((currentIndex.value / totalQuestions.value) * 100)
  })

  const canGoNext = computed(() => {
    return answers.value.has(currentIndex.value)
  })

  const canGoPrevious = computed(() => currentIndex.value > 0)

  const isLastQuestion = computed(() => currentIndex.value === totalQuestions.value - 1)

  const allQuestionsAnswered = computed(() => {
    return answers.value.size === totalQuestions.value
  })

  // Actions
  async function initializeQuiz(id: number, name: string) {
    quizId.value = id
    playerName.value = name

    // Récupérer les questions depuis l'API
    const data = await fetchQuestions(id)
    questions.value = data.sort((a, b) => a.position - b.position)

    // Vérifier s'il y a une progression sauvegardée
    if (savedProgress.value.quizId === id) {
      currentIndex.value = savedProgress.value.currentIndex
      const savedAnswers = new Map<number, Answer>()
      savedProgress.value.answers.forEach((answer, idx) => {
        savedAnswers.set(idx, answer)
      })
      answers.value = savedAnswers
      startTime.value = savedProgress.value.startTime
    } else {
      reset()
      startTime.value = Date.now()
      saveProgress()
    }
  }

  function answerQuestion(choiceId: number) {
    const question = currentQuestion.value
    if (!question) return

    const choice = question.choices.find((c) => c.id === choiceId)
    if (!choice) return

    const answer: Answer = {
      question_id: question.id,
      choice_id: choiceId,
      is_correct: choice.is_correct,
      timestamp: new Date().toISOString()
    }

    answers.value.set(currentIndex.value, answer)
    saveProgress()
  }

  function nextQuestion() {
    if (!isLastQuestion.value) {
      currentIndex.value++
      saveProgress()
    }
  }

  function previousQuestion() {
    if (canGoPrevious.value) {
      currentIndex.value--
    }
  }

  function goToQuestion(index: number) {
    if (index >= 0 && index < totalQuestions.value) {
      currentIndex.value = index
    }
  }

  async function submitQuiz() {
    if (!allQuestionsAnswered.value) {
      throw new Error('Toutes les questions doivent être répondues')
    }

    endTime.value = Date.now()
    isCompleted.value = true

    // Préparer les données pour l'API
    const answersArray = Array.from(answers.value.values())
    const requestData: AttemptRequest = {
      quiz_id: quizId.value,
      player_name: playerName.value,
      answers: answersArray.map((a) => ({
        question_id: a.question_id,
        choice_id: a.choice_id
      })),
      time_spent: timeSpent.value
    }

    // Envoyer les résultats à l'API
    const response = await submitAttempt(requestData)
    attemptId.value = response.id

    // Mettre à jour les informations de correction
    response.correct_answers.forEach((questionId) => {
      const entry = Array.from(answers.value.entries()).find(
        ([_, answer]) => answer.question_id === questionId
      )
      if (entry) {
        const [index, answer] = entry
        answers.value.set(index, { ...answer, is_correct: true })
      }
    })

    // Effacer la progression sauvegardée
    clearProgress()

    return response
  }

  function reset() {
    currentIndex.value = 0
    answers.value.clear()
    startTime.value = 0
    endTime.value = 0
    isCompleted.value = false
    attemptId.value = null
    clearProgress()
  }

  function saveProgress() {
    savedProgress.value = {
      quizId: quizId.value,
      currentIndex: currentIndex.value,
      answers: Array.from(answers.value.values()),
      startTime: startTime.value
    }
  }

  function clearProgress() {
    savedProgress.value = {
      quizId: 0,
      currentIndex: 0,
      answers: [],
      startTime: 0
    }
  }

  function getAnswerForQuestion(index: number): Answer | undefined {
    return answers.value.get(index)
  }

  return {
    // State
    quizId,
    playerName,
    questions,
    currentIndex,
    answers,
    startTime,
    endTime,
    isCompleted,
    attemptId,

    // Computed
    currentQuestion,
    totalQuestions,
    score,
    correctAnswers,
    wrongAnswers,
    timeSpent,
    progress,
    canGoNext,
    canGoPrevious,
    isLastQuestion,
    allQuestionsAnswered,

    // Actions
    initializeQuiz,
    answerQuestion,
    nextQuestion,
    previousQuestion,
    goToQuestion,
    submitQuiz,
    reset,
    getAnswerForQuestion
  }
})

