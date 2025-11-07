<script setup lang="ts">
import { computed } from 'vue'
import { useQuizStore } from '@/stores/quiz'

const quiz = useQuizStore()
// Pinia unwraps getters, on peut lire directement la valeur
const percent = computed(() => {
  const p = (quiz.progress as unknown as number) || 0
  return Math.max(0, Math.min(100, p))
})
</script>

<template>
  <!-- Utilise la hauteur du header via --header-offset définie dans Header.vue -->
  <div class="sticky" :style="{ top: `var(--header-offset, 56px)` }" style="z-index: 40;">
    <div
      class="h-[2px] w-full bg-[var(--border)]"
      role="progressbar"
      :aria-valuemin="0"
      :aria-valuemax="100"
      :aria-valuenow="percent"
      aria-label="Progression du quiz"
    >
      <div
        class="h-full bg-[var(--accent)] transition-[width] duration-150"
        :style="{ width: `${percent}%` }"
      />
    </div>
  </div>
  
</template>

<style scoped>
/* Transitions brèves uniquement */
</style>


