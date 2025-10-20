<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isAuthenticated = ref(false)

// Placeholder admin page
const handleLogout = () => {
  localStorage.removeItem('auth_token')
  router.push('/')
}
</script>

<template>
  <div class="min-h-screen p-6">
    <div class="max-w-4xl mx-auto">
      <div class="card">
        <h1 class="text-4xl font-black text-gray-900 dark:text-white mb-6">
          Administration
        </h1>
        <p class="text-gray-600 dark:text-gray-400 mb-8">
          Interface d'administration - En construction
        </p>
        <button @click="handleLogout" class="btn-secondary">
          Déconnexion
        </button>
      </div>
    </div>
  </div>
</template>

