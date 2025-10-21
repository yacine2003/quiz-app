/**
 * Tests unitaires pour le store Quiz
 */
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useQuizStore } from '@/stores/quiz'
import type { Question } from '@/types/models'

// Mock de l'API
vi.mock('@/services/api', () => ({
  fetchQuestions: vi.fn(() =>
    Promise.resolve([
      {
        id: 1,
        quiz_id: 1,
        position: 1,
        title: 'Question 1',
        text: 'Test question?',
        difficulty: 'easy',
        tags: ['test'],
        choices: [
          { id: 1, text: 'Choice A', is_correct: true },
          { id: 2, text: 'Choice B', is_correct: false }
        ]
      },
      {
        id: 2,
        quiz_id: 1,
        position: 2,
        title: 'Question 2',
        text: 'Test question 2?',
        difficulty: 'easy',
        tags: ['test'],
        choices: [
          { id: 3, text: 'Choice C', is_correct: false },
          { id: 4, text: 'Choice D', is_correct: true }
        ]
      }
    ] as Question[])
  ),
  submitAttempt: vi.fn(() =>
    Promise.resolve({
      id: 1,
      score: 1,
      total_questions: 2,
      percentage: 50,
      time_spent: 30,
      correct_answers: [1]
    })
  )
}))

describe('useQuizStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('initialise correctement le store', () => {
    const store = useQuizStore()

    expect(store.quizId).toBe(0)
    expect(store.playerName).toBe('')
    expect(store.questions).toEqual([])
    expect(store.currentIndex).toBe(0)
    expect(store.score).toBe(0)
  })

  it('initialise le quiz avec les données de l API', async () => {
    const store = useQuizStore()

    await store.initializeQuiz(1, 'TestPlayer')

    expect(store.quizId).toBe(1)
    expect(store.playerName).toBe('TestPlayer')
    expect(store.questions).toHaveLength(2)
    expect(store.startTime).toBeGreaterThan(0)
  })

  it('enregistre une réponse correctement', async () => {
    const store = useQuizStore()
    await store.initializeQuiz(1, 'TestPlayer')

    store.answerQuestion(1) // Choice A (correct)

    const answer = store.getAnswerForQuestion(0)
    expect(answer).toBeDefined()
    expect(answer?.choice_id).toBe(1)
    expect(answer?.is_correct).toBe(true)
  })

  it('calcule le score correctement', async () => {
    const store = useQuizStore()
    await store.initializeQuiz(1, 'TestPlayer')

    // Répondre correctement à la première question
    store.answerQuestion(1)
    // Répondre incorrectement à la deuxième
    store.nextQuestion()
    store.answerQuestion(3)

    expect(store.answers.size).toBe(2)
    expect(store.score).toBe(1)
    expect(store.correctAnswers).toBe(1)
    expect(store.wrongAnswers).toBe(1)
  })

  it('gère la navigation entre questions', async () => {
    const store = useQuizStore()
    await store.initializeQuiz(1, 'TestPlayer')

    expect(store.currentIndex).toBe(0)
    expect(store.isLastQuestion).toBe(false)

    store.nextQuestion()
    expect(store.currentIndex).toBe(1)
    expect(store.isLastQuestion).toBe(true)

    store.previousQuestion()
    expect(store.currentIndex).toBe(0)

    store.goToQuestion(1)
    expect(store.currentIndex).toBe(1)
  })

  it('empêche de passer à la question suivante sans répondre', async () => {
    const store = useQuizStore()
    await store.initializeQuiz(1, 'TestPlayer')

    expect(store.canGoNext).toBe(false)

    store.answerQuestion(1)
    expect(store.canGoNext).toBe(true)
  })

  it('calcule le progrès en pourcentage', async () => {
    const store = useQuizStore()
    await store.initializeQuiz(1, 'TestPlayer')

    expect(store.progress).toBe(0)

    store.nextQuestion()
    expect(store.progress).toBe(50)
  })

  it('détecte quand toutes les questions sont répondues', async () => {
    const store = useQuizStore()
    await store.initializeQuiz(1, 'TestPlayer')

    expect(store.allQuestionsAnswered).toBe(false)

    store.answerQuestion(1)
    expect(store.allQuestionsAnswered).toBe(false)

    store.nextQuestion()
    store.answerQuestion(4)
    expect(store.allQuestionsAnswered).toBe(true)
  })

  it('soumet le quiz correctement', async () => {
    const store = useQuizStore()
    await store.initializeQuiz(1, 'TestPlayer')

    // Répondre à toutes les questions
    store.answerQuestion(1)
    store.nextQuestion()
    store.answerQuestion(4)

    const response = await store.submitQuiz()

    expect(store.isCompleted).toBe(true)
    expect(response.id).toBe(1)
    expect(response.score).toBe(1)
    expect(response.total_questions).toBe(2)
  })

  it('réinitialise correctement le store', async () => {
    const store = useQuizStore()
    await store.initializeQuiz(1, 'TestPlayer')

    store.answerQuestion(1)
    store.nextQuestion()

    store.reset()

    expect(store.currentIndex).toBe(0)
    expect(store.answers.size).toBe(0)
    expect(store.startTime).toBe(0)
    expect(store.isCompleted).toBe(false)
  })
})

