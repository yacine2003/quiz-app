/**
 * Client API pour communiquer avec le backend
 */
import axios, { type AxiosInstance } from 'axios'
import type {
  Quiz,
  Question,
  AttemptRequest,
  AttemptResponse,
  LeaderboardEntry
} from '@/types/models'

class ApiClient {
  private client: AxiosInstance

  constructor() {
    // En dev, on passe toujours par le proxy Vite (/api) → backend 5001
    // Cela évite les soucis de variables d'environnement non prises en compte
    const baseURL = '/api'

    this.client = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json'
      }
    })

    // Intercepteur pour ajouter le token JWT si présent
    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('auth_token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    })
  }

  // Quizzes
  async fetchQuizzes(): Promise<Quiz[]> {
    const response = await this.client.get('/quizzes')
    return response.data
  }

  async fetchQuiz(id: number): Promise<Quiz> {
    const response = await this.client.get(`/quizzes/${id}`)
    return response.data
  }

  // Questions
  async fetchQuestions(quizId: number): Promise<Question[]> {
    const response = await this.client.get('/questions', {
      params: { quiz_id: quizId }
    })
    return response.data
  }

  async fetchQuestionByPosition(position: number): Promise<Question> {
    const response = await this.client.get('/questions', {
      params: { position }
    })
    return response.data
  }

  // Attempts
  async submitAttempt(data: AttemptRequest): Promise<AttemptResponse> {
    const response = await this.client.post('/attempts', data)
    return response.data
  }

  async fetchAttempt(id: number) {
    const response = await this.client.get(`/attempts/${id}`)
    return response.data
  }

  // Leaderboard
  async fetchLeaderboard(quizId: number, limit = 50): Promise<LeaderboardEntry[]> {
    const response = await this.client.get(`/leaderboard/${quizId}`, {
      params: { limit }
    })
    return response.data
  }

  // Auth
  async login(password: string): Promise<{ token: string }> {
    const response = await this.client.post('/auth/login', { password })
    return response.data
  }
}

export const apiClient = new ApiClient()

// Export des fonctions pour TanStack Query
export const fetchQuizzes = () => apiClient.fetchQuizzes()
export const fetchQuiz = (id: number) => apiClient.fetchQuiz(id)
export const fetchQuestions = (quizId: number) => apiClient.fetchQuestions(quizId)
export const submitAttempt = (data: AttemptRequest) => apiClient.submitAttempt(data)
export const fetchLeaderboard = (quizId: number) => apiClient.fetchLeaderboard(quizId)

