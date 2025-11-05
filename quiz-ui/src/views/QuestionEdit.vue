<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { apiClient } from '@/services/api'
import type { Question } from '@/types/models'

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const uploadedImagePreview = ref<string>('')

// Mode: 'create' ou 'edit'
const isEditMode = ref(false)

// Copie locale de la question (principe des props)
const localQuestion = ref<Partial<Question>>({
  quiz_id: 1,
  position: 1,
  title: '',
  text: '',
  image: '',
  difficulty: 'easy',
  tags: [],
  explanation: '',
  choices: [
    { id: 0, text: '', is_correct: false },
    { id: 1, text: '', is_correct: false },
    { id: 2, text: '', is_correct: false },
    { id: 3, text: '', is_correct: false }
  ]
})

onMounted(async () => {
  const questionId = route.params.id
  if (questionId && questionId !== 'new') {
    isEditMode.value = true
    await loadQuestion(Number(questionId))
  }
})

async function loadQuestion(id: number) {
  loading.value = true
  try {
    const question = await apiClient.fetchQuestionById(id)
    localQuestion.value = {
      ...question,
      tags: [...(question.tags || [])],
      choices: question.choices.map(c => ({ ...c }))
    }
    uploadedImagePreview.value = question.image || ''
  } catch (error) {
    console.error('Erreur lors du chargement:', error)
    alert('Erreur lors du chargement de la question')
    router.push('/admin')
  } finally {
    loading.value = false
  }
}

// Gestion des tags
const tagInput = ref('')

function addTag() {
  if (tagInput.value.trim() && localQuestion.value.tags) {
    localQuestion.value.tags.push(tagInput.value.trim())
    tagInput.value = ''
  }
}

function removeTag(index: number) {
  localQuestion.value.tags?.splice(index, 1)
}

function setCorrectAnswer(index: number) {
  localQuestion.value.choices?.forEach((choice, i) => {
    choice.is_correct = i === index
  })
}

// Gestion de l'upload d'image
function handleImageUpload(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  
  if (!file) return
  
  // Vérifier que c'est bien une image
  if (!file.type.startsWith('image/')) {
    alert('Veuillez sélectionner un fichier image')
    return
  }
  
  // Créer un aperçu
  const reader = new FileReader()
  reader.onload = (e) => {
    uploadedImagePreview.value = e.target?.result as string
  }
  reader.readAsDataURL(file)
  
  // Pour une vraie implémentation, il faudrait uploader le fichier vers un serveur
  // Ici on simule en suggérant un chemin
  const fileName = file.name
  localQuestion.value.image = `/images/questions/${fileName}`
  
  alert(`Image sélectionnée : ${fileName}\n\nNote : Dans une vraie application, l'image serait uploadée vers le serveur.\nPour le moment, veuillez placer manuellement l'image dans : /public/images/questions/${fileName}`)
}

async function handleSave() {
  // Validation basique
  if (!localQuestion.value.title?.trim()) {
    alert('Le titre est requis')
    return
  }
  if (!localQuestion.value.text?.trim()) {
    alert('Le texte de la question est requis')
    return
  }
  
  const hasCorrectAnswer = localQuestion.value.choices?.some(c => c.is_correct)
  if (!hasCorrectAnswer) {
    alert('Vous devez sélectionner au moins une réponse correcte')
    return
  }

  const hasEmptyChoice = localQuestion.value.choices?.some(c => !c.text?.trim())
  if (hasEmptyChoice) {
    alert('Toutes les réponses doivent avoir un texte')
    return
  }

  loading.value = true
  try {
    if (isEditMode.value && route.params.id) {
      // Mise à jour
      await apiClient.updateQuestion(Number(route.params.id), localQuestion.value)
      alert('Question mise à jour avec succès')
      router.push(`/admin/questions/${route.params.id}`)
    } else {
      // Création
      const result = await apiClient.createQuestion(localQuestion.value)
      alert('Question créée avec succès')
      router.push(`/admin/questions/${result.id}`)
    }
  } catch (error: any) {
    console.error('Erreur lors de la sauvegarde:', error)
    alert(error.response?.data?.error || 'Erreur lors de la sauvegarde de la question')
  } finally {
    loading.value = false
  }
}

function handleCancel() {
  if (isEditMode.value && route.params.id) {
    router.push(`/admin/questions/${route.params.id}`)
  } else {
    router.push('/admin')
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
            {{ isEditMode ? 'Éditer la question' : 'Créer une question' }}
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
        <!-- Quiz ID & Position -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Quiz
            </label>
            <select 
              v-model.number="localQuestion.quiz_id"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            >
              <option :value="1">1 - Bases du tennis</option>
              <option :value="2">2 - Roland-Garros</option>
              <option :value="3">3 - Tennis avancé</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Position
            </label>
            <input 
              v-model.number="localQuestion.position"
              type="number"
              min="1"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            />
            <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
              Position de la question dans le quiz
            </p>
          </div>
        </div>

        <!-- Title -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Titre *
          </label>
          <input 
            v-model="localQuestion.title"
            type="text"
            placeholder="Ex: Qu'est-ce qu'un ace au tennis ?"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          />
        </div>

        <!-- Text -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Intitulé *
          </label>
          <textarea 
            v-model="localQuestion.text"
            rows="3"
            placeholder="Texte complet de la question..."
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          ></textarea>
        </div>

        <!-- Image Upload -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Image
          </label>
          <div class="space-y-3">
            <div class="flex gap-3">
              <input 
                type="file"
                accept="image/*"
                @change="handleImageUpload"
                class="hidden"
                id="image-upload"
              />
              <label 
                for="image-upload"
                class="flex-1 px-4 py-3 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg hover:border-blue-500 dark:hover:border-blue-400 cursor-pointer transition-colors flex items-center justify-center gap-2 text-gray-600 dark:text-gray-400"
              >
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                <span>Cliquez pour uploader une image</span>
              </label>
            </div>
            
            <!-- Image Preview -->
            <div v-if="uploadedImagePreview" class="relative">
              <img 
                :src="uploadedImagePreview" 
                alt="Aperçu"
                class="max-h-64 rounded-lg border border-gray-200 dark:border-gray-700"
              />
              <button
                @click="uploadedImagePreview = ''; localQuestion.image = ''"
                class="absolute top-2 right-2 p-2 bg-red-600 text-white rounded-full hover:bg-red-700 transition-colors"
                type="button"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <p class="text-xs text-gray-500 dark:text-gray-400">
              L'image sera sauvegardée dans /public/images/questions/
            </p>
          </div>
        </div>

        <!-- Difficulty -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Difficulté
          </label>
          <div class="flex gap-3">
            <label class="flex items-center">
              <input 
                v-model="localQuestion.difficulty"
                type="radio"
                value="easy"
                class="mr-2"
              />
              <span class="text-green-600 dark:text-green-400">Facile</span>
            </label>
            <label class="flex items-center">
              <input 
                v-model="localQuestion.difficulty"
                type="radio"
                value="medium"
                class="mr-2"
              />
              <span class="text-yellow-600 dark:text-yellow-400">Moyen</span>
            </label>
            <label class="flex items-center">
              <input 
                v-model="localQuestion.difficulty"
                type="radio"
                value="hard"
                class="mr-2"
              />
              <span class="text-red-600 dark:text-red-400">Difficile</span>
            </label>
          </div>
        </div>

        <!-- Choices -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Réponses possibles * (cliquez pour sélectionner la bonne réponse)
          </label>
          <div class="space-y-3">
            <div 
              v-for="(choice, index) in localQuestion.choices" 
              :key="index"
              class="flex items-center gap-3"
            >
              <button
                @click="setCorrectAnswer(index)"
                :class="[
                  'flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all',
                  choice.is_correct 
                    ? 'border-green-500 bg-green-500' 
                    : 'border-gray-300 dark:border-gray-600 hover:border-green-400'
                ]"
                type="button"
                title="Marquer comme bonne réponse"
              >
                <svg v-if="choice.is_correct" class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
              </button>
              <span class="text-sm font-medium text-gray-600 dark:text-gray-400 w-6">
                {{ String.fromCharCode(65 + index) }}.
              </span>
              <input 
                v-model="choice.text"
                type="text"
                :placeholder="`Réponse ${String.fromCharCode(65 + index)}`"
                class="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              />
            </div>
          </div>
        </div>

        <!-- Tags -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Tags (optionnel)
          </label>
          <div class="flex gap-2 mb-2">
            <input 
              v-model="tagInput"
              @keyup.enter="addTag"
              type="text"
              placeholder="Ajouter un tag"
              class="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            />
            <button 
              @click="addTag"
              type="button"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Ajouter
            </button>
          </div>
          <div class="flex flex-wrap gap-2">
            <span 
              v-for="(tag, index) in localQuestion.tags" 
              :key="index"
              class="inline-flex items-center gap-2 px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full text-sm"
            >
              {{ tag }}
              <button 
                @click="removeTag(index)"
                type="button"
                class="text-gray-500 hover:text-red-600 dark:text-gray-400 dark:hover:text-red-400"
              >
                ×
              </button>
            </span>
          </div>
        </div>

        <!-- Explanation -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Explication (optionnel)
          </label>
          <textarea 
            v-model="localQuestion.explanation"
            rows="2"
            placeholder="Explication de la réponse correcte"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          ></textarea>
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

