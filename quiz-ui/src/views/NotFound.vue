<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <div class="min-h-screen flex items-center justify-center p-6">
    <div class="text-center animate-fade-in">
      <div class="text-9xl mb-8">🤔</div>
      <h1 class="text-7xl font-black text-gray-900 dark:text-white mb-4">
        404
      </h1>
      <p class="text-3xl text-gray-600 dark:text-gray-300 mb-12">
        Page introuvable
      </p>
      <button @click="router.push('/')" class="btn-primary px-12 py-5 text-xl">
        🏠 Retour à l'accueil
      </button>
    </div>
  </div>
</template>

