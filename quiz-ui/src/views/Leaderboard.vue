<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useQuery } from '@tanstack/vue-query'
import { fetchLeaderboard } from '@/services/api'

const props = defineProps<{
  quizId: number
}>()

const router = useRouter()

const { data: leaderboard, isLoading, error, refetch } = useQuery({
  queryKey: ['leaderboard', props.quizId],
  queryFn: () => fetchLeaderboard(props.quizId),
  refetchInterval: 10000 // Rafraîchir toutes les 10s
})

const getMedalEmoji = (rank: number) => {
  if (rank === 1) return '🥇'
  if (rank === 2) return '🥈'
  if (rank === 3) return '🥉'
  return `${rank}`
}

const getRowClass = (rank: number) => {
  if (rank === 1) return 'bg-yellow-50 dark:bg-yellow-900/20 border-l-4 border-yellow-500'
  if (rank === 2) return 'bg-gray-50 dark:bg-gray-700/50 border-l-4 border-gray-400'
  if (rank === 3) return 'bg-orange-50 dark:bg-orange-900/20 border-l-4 border-orange-500'
  return ''
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('fr-FR', {
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}
</script>

<template>
  <div class="min-h-screen p-6 py-12">
    <div class="max-w-6xl mx-auto">
      <header class="text-center mb-12 animate-fade-in">
        <div class="text-8xl mb-6">🏆</div>
        <h1 class="text-6xl font-black text-gray-900 dark:text-white mb-4">
          Classement
        </h1>
        <p class="text-2xl text-gray-600 dark:text-gray-300">
          Les meilleurs scores
        </p>
      </header>

      <!-- Loading -->
      <div v-if="isLoading" class="text-center py-12">
        <div class="loading-spinner mx-auto"></div>
        <p class="text-gray-600 dark:text-gray-400 mt-4">Chargement du classement...</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="text-center py-12">
        <div class="text-6xl mb-4">⚠️</div>
        <p class="text-red-600 text-lg mb-4">Erreur de chargement du classement</p>
        <button @click="refetch" class="btn-primary">
          Réessayer
        </button>
      </div>

      <!-- Leaderboard Table -->
      <div v-else-if="leaderboard && leaderboard.length > 0" class="card p-0 overflow-hidden animate-fade-in">
        <!-- Podium Top 3 -->
        <div v-if="leaderboard.length >= 3" class="bg-gradient-to-r from-yellow-50 to-orange-50 dark:from-yellow-900/20 dark:to-orange-900/20 p-8 mb-6">
          <div class="grid grid-cols-3 gap-6 max-w-4xl mx-auto">
            <!-- 2nd Place -->
            <div class="text-center transform -translate-y-2">
              <div class="text-6xl mb-2">🥈</div>
              <div class="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-lg">
                <div class="font-black text-2xl text-gray-900 dark:text-white mb-1">
                  {{ leaderboard[1].player_name }}
                </div>
                <div class="text-3xl font-black text-primary-600 dark:text-primary-400">
                  {{ leaderboard[1].percentage }}%
                </div>
                <div class="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  {{ leaderboard[1].time_spent }}s
                </div>
              </div>
            </div>

            <!-- 1st Place -->
            <div class="text-center transform -translate-y-8">
              <div class="text-8xl mb-2 animate-pulse">🥇</div>
              <div class="bg-gradient-to-br from-yellow-100 to-yellow-200 dark:from-yellow-900 dark:to-yellow-800 rounded-xl p-6 shadow-2xl border-4 border-yellow-400">
                <div class="font-black text-3xl text-gray-900 dark:text-white mb-2">
                  {{ leaderboard[0].player_name }}
                </div>
                <div class="text-5xl font-black text-yellow-700 dark:text-yellow-300">
                  {{ leaderboard[0].percentage }}%
                </div>
                <div class="text-sm text-gray-700 dark:text-gray-300 mt-2 font-bold">
                  {{ leaderboard[0].time_spent }}s
                </div>
              </div>
            </div>

            <!-- 3rd Place -->
            <div class="text-center transform -translate-y-2">
              <div class="text-6xl mb-2">🥉</div>
              <div class="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-lg">
                <div class="font-black text-2xl text-gray-900 dark:text-white mb-1">
                  {{ leaderboard[2].player_name }}
                </div>
                <div class="text-3xl font-black text-primary-600 dark:text-primary-400">
                  {{ leaderboard[2].percentage }}%
                </div>
                <div class="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  {{ leaderboard[2].time_spent }}s
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Full Table -->
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-50 dark:bg-gray-900">
              <tr>
                <th class="text-left py-4 px-6 font-black text-gray-700 dark:text-gray-300">Rang</th>
                <th class="text-left py-4 px-6 font-black text-gray-700 dark:text-gray-300">Joueur</th>
                <th class="text-right py-4 px-6 font-black text-gray-700 dark:text-gray-300">Score</th>
                <th class="text-right py-4 px-6 font-black text-gray-700 dark:text-gray-300">Temps</th>
                <th class="text-right py-4 px-6 font-black text-gray-700 dark:text-gray-300">Date</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(entry, index) in leaderboard"
                :key="entry.id"
                class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
                :class="getRowClass(index + 1)"
              >
                <td class="py-4 px-6">
                  <span class="text-2xl font-black">
                    {{ getMedalEmoji(index + 1) }}
                  </span>
                </td>
                <td class="py-4 px-6">
                  <span class="font-bold text-lg text-gray-900 dark:text-white">
                    {{ entry.player_name }}
                  </span>
                </td>
                <td class="py-4 px-6 text-right">
                  <div class="font-black text-xl text-primary-600 dark:text-primary-400">
                    {{ entry.percentage }}%
                  </div>
                  <div class="text-sm text-gray-500">
                    {{ entry.score }} / {{ entry.total_questions }}
                  </div>
                </td>
                <td class="py-4 px-6 text-right">
                  <span class="font-bold text-gray-700 dark:text-gray-300">
                    {{ entry.time_spent }}s
                  </span>
                </td>
                <td class="py-4 px-6 text-right text-sm text-gray-500">
                  {{ formatDate(entry.created_at) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- No entries -->
      <div v-else class="text-center py-20">
        <div class="text-8xl mb-6">📊</div>
        <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Aucun score encore
        </h3>
        <p class="text-gray-600 dark:text-gray-400 mb-8">
          Soyez le premier à tenter le quiz !
        </p>
        <button @click="router.push({ name: 'quiz-start', params: { id: quizId } })" class="btn-primary">
          Démarrer le quiz
        </button>
      </div>

      <!-- Back Button -->
      <div class="mt-12 text-center">
        <button @click="router.push('/')" class="btn-secondary px-8 py-4 text-lg">
          ← Retour à l'accueil
        </button>
      </div>
    </div>
  </div>
</template>

