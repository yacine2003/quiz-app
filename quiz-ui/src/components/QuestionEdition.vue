<script setup lang="ts">
import { ref, watch } from 'vue'
import type { Question, Choice } from '@/types/models'

const props = defineProps<{
  question?: Question | null
  isVisible: boolean
}>()

const emit = defineEmits<{
  save: [question: Partial<Question>]
  cancel: []
}>()

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

// Surveiller les changements de la prop pour mettre à jour la copie locale
watch(() => props.question, (newQuestion) => {
  if (newQuestion) {
    localQuestion.value = {
      ...newQuestion,
      tags: [...(newQuestion.tags || [])],
      choices: newQuestion.choices.map(c => ({ ...c }))
    }
  } else {
    // Réinitialiser pour une nouvelle question
    localQuestion.value = {
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
    }
  }
}, { immediate: true, deep: true })

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

function handleSave() {
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

  emit('save', localQuestion.value)
}
</script>

<template>
  <div 
    v-if="isVisible" 
    class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 overflow-y-auto"
    @click.self="emit('cancel')"
  >
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-3xl w-full my-8 max-h-[90vh] overflow-y-auto">
      <!-- Header -->
      <div class="sticky top-0 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4 flex items-center justify-between">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
          {{ question?.id ? 'Éditer la question' : 'Nouvelle question' }}
        </h2>
        <button 
          @click="emit('cancel')"
          class="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 rounded transition-colors"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Form -->
      <div class="p-6 space-y-6">
        <!-- Quiz ID & Position -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Quiz ID
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
            placeholder="Titre de la question"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          />
        </div>

        <!-- Text -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Texte de la question *
          </label>
          <textarea 
            v-model="localQuestion.text"
            rows="3"
            placeholder="Texte complet de la question"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          ></textarea>
        </div>

        <!-- Image -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            URL de l'image (optionnel)
          </label>
          <input 
            v-model="localQuestion.image"
            type="text"
            placeholder="/images/questions/q1base.png"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          />
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
            Conseil : placez vos images dans /public/images/questions/
          </p>
          <img 
            v-if="localQuestion.image" 
            :src="localQuestion.image" 
            alt="Aperçu"
            class="mt-2 max-h-32 rounded border border-gray-200 dark:border-gray-700"
          />
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
            Réponses * (cliquez sur le bouton radio pour marquer la bonne réponse)
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
      </div>

      <!-- Footer -->
      <div class="sticky bottom-0 bg-gray-50 dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 px-6 py-4 flex justify-end gap-3">
        <button 
          @click="emit('cancel')"
          class="px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
        >
          Annuler
        </button>
        <button 
          @click="handleSave"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          {{ question?.id ? 'Enregistrer' : 'Créer' }}
        </button>
      </div>
    </div>
  </div>
</template>

