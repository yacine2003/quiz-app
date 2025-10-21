/**
 * Types pour les modèles de données de l'application Quiz
 */

export interface Quiz {
  id: number
  title: string
  description?: string
  difficulty: 'easy' | 'medium' | 'hard'
  is_published: boolean
  question_count: number
  created_at: string
}

export interface Choice {
  id: number
  text: string
  is_correct?: boolean // Seulement pour l'admin
}

export interface Question {
  id: number
  quiz_id: number
  position: number
  title: string
  text: string
  image?: string
  difficulty: 'easy' | 'medium' | 'hard'
  tags: string[]
  explanation?: string
  choices: Choice[]
}

export interface Answer {
  question_id: number
  choice_id: number
  is_correct?: boolean
  timestamp?: string
}

export interface Attempt {
  id: number
  quiz_id: number
  player_name: string
  score: number
  total_questions: number
  percentage: number
  time_spent: number
  created_at: string
  answers?: Answer[]
}

export interface AttemptRequest {
  quiz_id: number
  player_name: string
  answers: {
    question_id: number
    choice_id: number
  }[]
  time_spent: number
}

export interface AttemptResponse {
  id: number
  score: number
  total_questions: number
  percentage: number
  time_spent: number
  correct_answers: number[]
}

export interface LeaderboardEntry {
  id: number
  player_name: string
  score: number
  total_questions: number
  percentage: number
  time_spent: number
  created_at: string
}

