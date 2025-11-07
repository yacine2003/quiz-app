<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { apiClient } from '@/services/api'
import type { Quiz } from '@/types/models'

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const isEditMode = ref(false)

// Copie locale du quiz
const localQuiz = ref<Partial<Quiz>>({
  title: '',
  description: '',
  difficulty: 'easy',
  is_published: true
})

onMounted(async () => {
  const quizId = route.params.id
  if (quizId && quizId !== 'new') {
    isEditMode.value = true
    await loadQuiz(Number(quizId))
  }
})

async function loadQuiz(id: number) {
  loading.value = true
  try {
    const quiz = await apiClient.fetchQuiz(id)
    localQuiz.value = {
      title: quiz.title,
      description: quiz.description,
      difficulty: quiz.difficulty,
      is_published: quiz.is_published
    }
  } catch (error) {
    console.error('Erreur lors du chargement:', error)
    alert('Erreur lors du chargement du quiz')
    router.push('/admin?tab=quizzes')
  } finally {
    loading.value = false
  }
}

async function handleSave() {
  // Validation
  if (!localQuiz.value.title?.trim()) {
    alert('Le titre est requis')
    return
  }

  loading.value = true
  try {
    if (isEditMode.value && route.params.id) {
      // Mise à jour
      await apiClient.updateQuiz(Number(route.params.id), localQuiz.value)
      alert('Quiz mis à jour avec succès')
      router.push(`/admin/quizzes/${route.params.id}`)
    } else {
      // Création
      const result = await apiClient.createQuiz(localQuiz.value)
      alert('Quiz créé avec succès')
      router.push(`/admin/quizzes/${result.id}`)
    }
  } catch (error: any) {
    console.error('Erreur lors de la sauvegarde:', error)
    alert(error.response?.data?.error || 'Erreur lors de la sauvegarde du quiz')
  } finally {
    loading.value = false
  }
}

function handleCancel() {
  if (isEditMode.value && route.params.id) {
    router.push(`/admin/quizzes/${route.params.id}`)
  } else {
    router.push('/admin?tab=quizzes')
  }
}

function handleLogout() {
  localStorage.removeItem('auth_token')
  router.push('/')
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Header -->
    <header class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 sticky top-0 z-40">
      <div class="max-w-4xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
            {{ isEditMode ? 'Éditer le quiz' : 'Créer un quiz' }}
          </h1>
          <button 
            @click="handleLogout"
            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center gap-2"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            Déconnexion
          </button>
        </div>
      </div>
    </header>

    <!-- Form -->
    <div class="max-w-4xl mx-auto px-6 py-8">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 space-y-6">
        <!-- Title -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Titre du quiz *
          </label>
          <input 
            v-model="localQuiz.title"
            type="text"
            placeholder="Ex: Les bases du tennis"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          />
        </div>

        <!-- Description -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Description
          </label>
          <textarea 
            v-model="localQuiz.description"
            rows="4"
            placeholder="Décrivez le contenu et les objectifs de ce quiz..."
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          ></textarea>
        </div>

        <!-- Difficulty -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Difficulté
          </label>
          <div class="flex gap-3">
            <label class="flex items-center">
              <input 
                v-model="localQuiz.difficulty"
                type="radio"
                value="easy"
                class="mr-2"
              />
              <span class="text-green-600 dark:text-green-400">Facile</span>
            </label>
            <label class="flex items-center">
              <input 
                v-model="localQuiz.difficulty"
                type="radio"
                value="medium"
                class="mr-2"
              />
              <span class="text-yellow-600 dark:text-yellow-400">Moyen</span>
            </label>
            <label class="flex items-center">
              <input 
                v-model="localQuiz.difficulty"
                type="radio"
                value="hard"
                class="mr-2"
              />
              <span class="text-red-600 dark:text-red-400">Difficile</span>
            </label>
          </div>
        </div>

        <!-- Published -->
        <div>
          <label class="flex items-center gap-2 cursor-pointer">
            <input 
              v-model="localQuiz.is_published"
              type="checkbox"
              class="w-5 h-5 text-blue-600 rounded"
            />
            <span class="text-sm font-medium text-gray-700 dark:text-gray-300">
              Publier ce quiz (le rendre visible aux utilisateurs)
            </span>
          </label>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1 ml-7">
            Un quiz non publié reste en mode brouillon et n'est pas accessible aux participants
          </p>
        </div>

        <!-- Info box -->
        <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
          <div class="flex gap-3">
            <svg class="w-5 h-5 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div class="text-sm text-blue-900 dark:text-blue-100">
              <p class="font-medium mb-1">Information</p>
              <p>Après avoir créé le quiz, vous pourrez y ajouter des questions depuis la page de gestion des questions.</p>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex justify-end gap-3 pt-4 border-t border-gray-200 dark:border-gray-700">
          <button 
            @click="handleCancel"
            type="button"
            class="px-6 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          >
            Annuler
          </button>
          <button 
            @click="handleSave"
            :disabled="loading"
            class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
          >
            <svg v-if="loading" class="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span>{{ loading ? 'Enregistrement...' : isEditMode ? 'Enregistrer' : 'Créer' }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

