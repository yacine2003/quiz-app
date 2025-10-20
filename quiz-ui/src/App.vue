<script setup lang="ts">
import Header from '@/components/Header.vue'
import { RouterView } from 'vue-router'
</script>

<template>
  <div id="app" class="min-h-screen bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100">
    <Header />
    <RouterView v-slot="{ Component }">
      <Transition name="fade" mode="out-in">
        <component :is="Component" />
      </Transition>
    </RouterView>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
