<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useQuery } from '@tanstack/vue-query'
import { fetchLeaderboard } from '@/services/api'
import { useQuizStore } from '@/stores/quiz'
import type { LeaderboardEntry } from '@/types/models'

const props = defineProps<{
  quizId: number
}>()

const router = useRouter()
const quizStore = useQuizStore()

// Contrôles
const selectedQuizId = ref<number>(props.quizId || 1)
const period = ref<'global' | 'today' | 'week' | 'month'>('global')
const searchQuery = ref<string>('')
const sortAscTime = ref<boolean>(true) // temps ascendant en cas d'égalité
const showExport = ref<boolean>(false)
const exportIncludeHeader = ref<boolean>(true)
const exportSeparator = ref<string>(',')
const exportScope = ref<'filtered' | 'page'>('filtered')

// Requête (recharge quand l'id change)
const { data, isLoading, error, refetch, isFetching } = useQuery({
  queryKey: computed(() => ['leaderboard', selectedQuizId.value]),
  queryFn: () => fetchLeaderboard(selectedQuizId.value),
  refetchInterval: 10000
})

watch(() => props.quizId, (v) => {
  if (typeof v === 'number' && v > 0) selectedQuizId.value = v
})

// Helpers
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

// Filtres / tri
const rawLeaderboard = computed<LeaderboardEntry[]>(() => data?.value ?? [])

function isInPeriod(d: Date) {
  const now = new Date()
  if (period.value === 'global') return true
  if (period.value === 'today') {
    return d.toDateString() === now.toDateString()
  }
  if (period.value === 'week') {
    const diff = (now.getTime() - d.getTime()) / (1000 * 60 * 60 * 24)
    return diff <= 7
  }
  if (period.value === 'month') {
    const sameYear = d.getFullYear() === now.getFullYear()
    const sameMonth = d.getMonth() === now.getMonth()
    return sameYear && sameMonth
  }
  return true
}

const filteredLeaderboard = computed<LeaderboardEntry[]>(() => {
  const q = searchQuery.value.trim().toLowerCase()
  return rawLeaderboard.value.filter((e) => {
    const inPeriod = e.created_at ? isInPeriod(new Date(e.created_at)) : true
    const matches = q ? e.player_name.toLowerCase().includes(q) : true
    return inPeriod && matches
  })
})

const finalLeaderboard = computed<LeaderboardEntry[]>(() => {
  const copy = [...filteredLeaderboard.value]
  copy.sort((a, b) => {
    if (b.score !== a.score) return b.score - a.score
    if (a.time_spent !== b.time_spent) return sortAscTime.value ? a.time_spent - b.time_spent : b.time_spent - a.time_spent
    const da = a.created_at ? new Date(a.created_at).getTime() : 0
    const db = b.created_at ? new Date(b.created_at).getTime() : 0
    return da - db // plus ancien devant
  })
  return copy
})

// "Ta position" et ancre
const myRank = computed(() => {
  const name = (quizStore.playerName || '').toLowerCase()
  if (!name) return null
  const idx = finalLeaderboard.value.findIndex((e) => e.player_name.toLowerCase() === name)
  return idx >= 0 ? idx + 1 : null
})

function locateMe() {
  if (myRank.value == null) return
  const row = document.querySelector(`[data-rank='${myRank.value}']`)
  if (row) row.scrollIntoView({ behavior: 'smooth', block: 'center' })
}

// Export CSV simple (résultats filtrés par défaut)
function exportCsv() {
  const rows = exportScope.value === 'page' ? finalLeaderboard.value : finalLeaderboard.value
  const sep = exportSeparator.value
  const header = ['Rang','Joueur','Score','Pourcentage','Temps','DateISO','Mode']
  const lines: string[] = []
  if (exportIncludeHeader.value) lines.push(header.join(sep))
  rows.forEach((e, i) => {
    const pct = (e.percentage ?? (e.total_questions ? (e.score / e.total_questions * 100) : 0)).toFixed(2)
    const mm = Math.floor((e.time_spent || 0) / 60)
    const ss = (e.time_spent || 0) % 60
    const time = `${String(mm).padStart(2,'0')}:${String(ss).padStart(2,'0')}`
    const line = [
      String(i + 1),
      e.player_name,
      `${e.score}/${e.total_questions}`,
      pct,
      time,
      e.created_at ?? '',
      selectedQuizId.value === 1 ? 'Easy' : selectedQuizId.value === 2 ? 'Medium' : 'Hard'
    ].join(sep)
    lines.push(line)
  })
  const blob = new Blob([lines.join('\n')], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  const now = new Date()
  const pad = (n:number) => String(n).padStart(2,'0')
  const name = `leaderboard_${selectedQuizId.value}_${now.getFullYear()}${pad(now.getMonth()+1)}${pad(now.getDate())}-${pad(now.getHours())}${pad(now.getMinutes())}.csv`
  a.href = url
  a.download = name
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
  showExport.value = false
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

      <!-- Barre de contrôles sticky -->
      <div class="sticky top-0 z-10 mb-6 bg-white/80 dark:bg-gray-800/80 backdrop-blur border-b border-gray-200 dark:border-gray-700">
        <div class="max-w-6xl mx-auto px-4 py-3 flex flex-wrap items-center gap-3">
          <!-- Modes -->
          <div class="inline-flex rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700">
            <button class="px-4 py-2 text-sm font-bold" :class="selectedQuizId===1?'bg-green-50 text-green-700 dark:bg-green-900/30':'text-gray-700 dark:text-gray-300'" @click="selectedQuizId=1; router.push({name:'leaderboard', params:{id:1}});">
              ● Easy
            </button>
            <button class="px-4 py-2 text-sm font-bold border-l border-gray-200 dark:border-gray-700" :class="selectedQuizId===2?'bg-amber-50 text-amber-700 dark:bg-amber-900/30':'text-gray-700 dark:text-gray-300'" @click="selectedQuizId=2; router.push({name:'leaderboard', params:{id:2}});">
              ▲ Medium
            </button>
            <button class="px-4 py-2 text-sm font-bold border-l border-gray-200 dark:border-gray-700" :class="selectedQuizId===3?'bg-red-50 text-red-700 dark:bg-red-900/30':'text-gray-700 dark:text-gray-300'" @click="selectedQuizId=3; router.push({name:'leaderboard', params:{id:3}});">
              ◆ Hard
            </button>
          </div>

          <!-- Période -->
          <div class="inline-flex rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700 ml-2">
            <button class="px-3 py-2 text-sm" :class="period==='today'?'bg-gray-100 dark:bg-gray-700 font-bold':''" @click="period='today'">Aujourd’hui</button>
            <button class="px-3 py-2 text-sm border-l border-gray-200 dark:border-gray-700" :class="period==='week'?'bg-gray-100 dark:bg-gray-700 font-bold':''" @click="period='week'">Semaine</button>
            <button class="px-3 py-2 text-sm border-l border-gray-200 dark:border-gray-700" :class="period==='month'?'bg-gray-100 dark:bg-gray-700 font-bold':''" @click="period='month'">Mois</button>
            <button class="px-3 py-2 text-sm border-l border-gray-200 dark:border-gray-700" :class="period==='global'?'bg-gray-100 dark:bg-gray-700 font-bold':''" @click="period='global'">Global</button>
          </div>

          <!-- Recherche -->
          <div class="flex-1 min-w-[180px]">
            <input v-model="searchQuery" type="search" placeholder="Rechercher un joueur…" class="w-full px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800" />
          </div>

          <!-- Tri & Export -->
          <button class="px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-700" :title="'Trier (Score ↓, Temps '+(sortAscTime?'↑':'↓')+', Date ↑)'" @click="sortAscTime=!sortAscTime">⇅</button>
          <button class="btn-primary px-4 py-2" @click="showExport=true">⤓ Exporter CSV</button>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="isLoading || isFetching" class="text-center py-12">
        <div class="loading-spinner mx-auto"></div>
        <p class="text-gray-600 dark:text-gray-400 mt-4">Chargement du classement...</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="text-center py-12">
        <div class="text-6xl mb-4">⚠️</div>
        <p class="text-red-600 text-lg mb-4">Erreur de chargement du classement</p>
        <button @click="() => refetch()" class="btn-primary">
          Réessayer
        </button>
      </div>

      <!-- Leaderboard Table -->
      <div v-else-if="finalLeaderboard && finalLeaderboard.length > 0" class="card p-0 overflow-hidden animate-fade-in">
        <!-- Podium Top 3 -->
        <div v-if="finalLeaderboard.length >= 3" class="bg-gradient-to-r from-yellow-50 to-orange-50 dark:from-yellow-900/20 dark:to-orange-900/20 p-8 mb-6">
          <div class="grid grid-cols-3 gap-6 max-w-4xl mx-auto">
            <!-- 2nd Place -->
            <div class="text-center transform -translate-y-2">
              <div class="text-6xl mb-2">🥈</div>
              <div class="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-lg">
                <div class="font-black text-2xl text-gray-900 dark:text-white mb-1">
                  {{ finalLeaderboard[1].player_name }}
                </div>
                <div class="text-3xl font-black text-primary-600 dark:text-primary-400">
                  {{ finalLeaderboard[1].percentage }}%
                </div>
                <div class="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  {{ finalLeaderboard[1].time_spent }}s
                </div>
              </div>
            </div>

            <!-- 1st Place -->
            <div class="text-center transform -translate-y-8">
              <div class="text-8xl mb-2 animate-pulse">🥇</div>
              <div class="bg-gradient-to-br from-yellow-100 to-yellow-200 dark:from-yellow-900 dark:to-yellow-800 rounded-xl p-6 shadow-2xl border-4 border-yellow-400">
                <div class="font-black text-3xl text-gray-900 dark:text-white mb-2">
                  {{ finalLeaderboard[0].player_name }}
                </div>
                <div class="text-5xl font-black text-yellow-700 dark:text-yellow-300">
                  {{ finalLeaderboard[0].percentage }}%
                </div>
                <div class="text-sm text-gray-700 dark:text-gray-300 mt-2 font-bold">
                  {{ finalLeaderboard[0].time_spent }}s
                </div>
              </div>
            </div>

            <!-- 3rd Place -->
            <div class="text-center transform -translate-y-2">
              <div class="text-6xl mb-2">🥉</div>
              <div class="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-lg">
                <div class="font-black text-2xl text-gray-900 dark:text-white mb-1">
                  {{ finalLeaderboard[2].player_name }}
                </div>
                <div class="text-3xl font-black text-primary-600 dark:text-primary-400">
                  {{ finalLeaderboard[2].percentage }}%
                </div>
                <div class="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  {{ finalLeaderboard[2].time_spent }}s
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
                v-for="(entry, index) in finalLeaderboard"
                :key="entry.id"
                class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
                :class="[getRowClass(index + 1), (quizStore.playerName && entry.player_name===quizStore.playerName)?'ring-2 ring-primary-400 relative':'']"
                :data-rank="index + 1"
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

        <!-- Actions secondaires -->
        <div class="flex items-center justify-between p-4">
          <div class="text-sm text-gray-500" v-if="myRank">Ta position: #{{ myRank }}</div>
          <div class="flex items-center gap-3 ml-auto">
            <button class="btn-secondary" @click="locateMe">Me localiser</button>
          </div>
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

  <!-- Modal Export -->
  <div v-if="showExport" class="fixed inset-0 bg-black/40 flex items-center justify-center p-4">
    <div class="bg-white dark:bg-gray-800 rounded-2xl w-full max-w-lg p-6 shadow-xl">
      <h3 class="text-xl font-black mb-4">Exporter en CSV</h3>
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-bold mb-2">Portée</label>
          <div class="flex gap-3">
            <label class="inline-flex items-center gap-2"><input type="radio" value="filtered" v-model="exportScope" /> Résultats filtrés</label>
            <label class="inline-flex items-center gap-2"><input type="radio" value="page" v-model="exportScope" /> Page courante</label>
          </div>
        </div>
        <div class="flex items-center gap-4">
          <label class="inline-flex items-center gap-2"><input type="checkbox" v-model="exportIncludeHeader" /> Inclure l’en‑tête</label>
          <label class="inline-flex items-center gap-2">Séparateur
            <select v-model="exportSeparator" class="ml-2 border rounded px-2 py-1">
              <option value=",">,</option>
              <option value=";">;</option>
            </select>
          </label>
        </div>
      </div>
      <div class="mt-6 flex justify-end gap-3">
        <button class="btn-secondary" @click="showExport=false">Annuler</button>
        <button class="btn-primary" @click="exportCsv">Exporter</button>
      </div>
    </div>
  </div>
</template>

