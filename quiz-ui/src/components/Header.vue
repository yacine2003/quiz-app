<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useQuizStore } from '@/stores/quiz'
import { useThemeStore, type ThemeName } from '@/stores/theme'

// Router & Store
const router = useRouter()
const route = useRoute()
const quiz = useQuizStore()

// Header shrink on scroll
const isShrunk = ref(false)
let ticking = false
const lastKnownScrollY = ref(0)

// Header element ref to compute dynamic offset for ProgressBar
const headerRef = ref<HTMLElement | null>(null)
const updateHeaderOffset = () => {
  const h = headerRef.value?.offsetHeight || 56
  document.documentElement.style.setProperty('--header-offset', `${h}px`)
}

const onScroll = () => {
  lastKnownScrollY.value = window.scrollY || 0
  if (!ticking) {
    window.requestAnimationFrame(() => {
      const next = lastKnownScrollY.value > 12
      if (next !== isShrunk.value) {
        isShrunk.value = next
        // Recalcule la hauteur du header après changement de padding
        requestAnimationFrame(updateHeaderOffset)
      }
      ticking = false
    })
    ticking = true
  }
}

// Mobile menu state & focus management
const isMenuOpen = ref(false)
const menuButtonRef = ref<HTMLButtonElement | null>(null)
const menuPanelRef = ref<HTMLDivElement | null>(null)

const openMenu = () => {
  if (isMenuOpen.value) return
  isMenuOpen.value = true
  requestAnimationFrame(() => {
    const firstLink = menuPanelRef.value?.querySelector('a,button') as HTMLElement | null
    firstLink?.focus()
  })
}
const closeMenu = () => {
  if (!isMenuOpen.value) return
  isMenuOpen.value = false
  requestAnimationFrame(() => {
    menuButtonRef.value?.focus()
  })
}
const toggleMenu = () => (isMenuOpen.value ? closeMenu() : openMenu())

const onBackdropClick = (e: MouseEvent) => {
  if (e.target === e.currentTarget) closeMenu()
}
const onMenuLinkClick = () => closeMenu()

// Keyboard shortcuts (global)
function isTypingTarget(target: EventTarget | null): boolean {
  const el = target as HTMLElement | null
  if (!el) return false
  const tag = el.tagName?.toLowerCase()
  return el.isContentEditable || tag === 'input' || tag === 'textarea' || tag === 'select'
}
const goHome = () => router.push({ path: '/' })
const goQuiz = () => router.push({ path: '/quiz' })
const goLeaderboard = () => router.push({ path: '/quiz/1/leaderboard' })
const goAdmin = () => router.push({ path: '/admin' })

const onKeyup = (e: KeyboardEvent) => {
  if (e.altKey || e.ctrlKey || e.metaKey) return
  if (isTypingTarget(e.target)) return
  const key = e.key.toLowerCase()
  if (key === 'h') { e.preventDefault(); goHome() }
  else if (key === 'q') { e.preventDefault(); goQuiz() }
  else if (key === 'l') { e.preventDefault(); goLeaderboard() }
  else if (key === 'a') { e.preventDefault(); goAdmin() }
  else if (key === 'escape' && isMenuOpen.value) { e.preventDefault(); closeMenu() }
}

// Header status area
const player = computed(() => quiz.playerName || 'Invité')
const total = computed(() => quiz.totalQuestions || quiz.questions.length || 0)
const current = computed(() => (total.value ? quiz.currentIndex + 1 : 0))
const elapsed = computed(() => quiz.timeSpent || 0)
const statusText = computed(() => `Joueur: ${player.value} · Q${Math.min(current.value, total.value || 0)}/${total.value || 0} · ${elapsed.value}s`)

// Theme store
const theme = useThemeStore()
const themeLabel = computed(() => {
  return theme.current === 'light'
    ? 'Clair'
    : theme.current === 'dark'
      ? 'Sombre (noir)'
      : 'Roland‑Garros'
})
const setTheme = (t: ThemeName) => theme.setTheme(t)

onMounted(() => {
  updateHeaderOffset()
  window.addEventListener('resize', updateHeaderOffset)
  window.addEventListener('scroll', onScroll, { passive: true })
  window.addEventListener('keyup', onKeyup)
})
onBeforeUnmount(() => {
  window.removeEventListener('resize', updateHeaderOffset)
  window.removeEventListener('scroll', onScroll)
  window.removeEventListener('keyup', onKeyup)
})

watch(isShrunk, () => updateHeaderOffset())
</script>

<template>
  <header
    ref="headerRef"
    class="sticky top-0 z-50 backdrop-blur border-b transition-[padding] duration-150 bg-[color-mix(in_srgb,var(--surface)_85%,transparent)] border-[var(--border)]"
    :class="isShrunk ? 'py-2' : 'py-3'"
    role="banner"
  >
    <div class="mx-auto max-w-6xl px-4 flex items-center justify-between gap-4">
      <!-- Brand -->
      <div class="flex items-center gap-3">
        <button
          type="button"
          class="text-xl font-bold text-[var(--text)] hover:opacity-80 focus:outline-none focus-visible:ring-2 focus-visible:ring-[var(--ring)] rounded"
          aria-label="Aller à l’accueil"
          @click="goHome"
        >
          Tennis Quiz
        </button>
      </div>

      <!-- Desktop nav -->
      <nav
        class="hidden md:flex items-center gap-6 text-sm font-medium"
        aria-label="Navigation principale"
        role="navigation"
      >
        <router-link
          to="/"
          class="px-1 py-1 rounded focus-visible:ring-2 focus-visible:ring-[var(--ring)]"
          :class="route.path === '/' ? 'text-[var(--accent)] underline underline-offset-4' : 'text-[var(--text)] hover:text-[var(--accent)]'"
          :aria-current="route.path === '/' ? 'page' : undefined"
        >Accueil</router-link>

        <router-link
          to="/quiz"
          class="px-1 py-1 rounded focus-visible:ring-2 focus-visible:ring-[var(--ring)]"
          :class="route.path === '/quiz' ? 'text-[var(--accent)] underline underline-offset-4' : 'text-[var(--text)] hover:text-[var(--accent)]'"
          :aria-current="route.path === '/quiz' ? 'page' : undefined"
        >Quiz</router-link>

        <router-link
          to="/quiz/1/leaderboard"
          class="px-1 py-1 rounded focus-visible:ring-2 focus-visible:ring-[var(--ring)]"
          :class="(route.path.startsWith('/quiz') && route.path.includes('/leaderboard')) ? 'text-[var(--accent)] underline underline-offset-4' : 'text-[var(--text)] hover:text-[var(--accent)]'"
          :aria-current="(route.path.startsWith('/quiz') && route.path.includes('/leaderboard')) ? 'page' : undefined"
        >Classement</router-link>

        <router-link
          to="/admin"
          class="px-1 py-1 rounded focus-visible:ring-2 focus-visible:ring-[var(--ring)]"
          :class="(route.path.startsWith('/admin')) ? 'text-[var(--accent)] underline underline-offset-4' : 'text-[var(--text)] hover:text-[var(--accent)]'"
          :aria-current="(route.path.startsWith('/admin')) ? 'page' : undefined"
        >Admin</router-link>
      </nav>

      <!-- Status area + theme selector -->
      <div class="hidden md:flex items-center gap-3">
        <div
          class="hidden md:flex items-center text-xs sm:text-sm text-gray-600 dark:text-gray-300"
          aria-live="polite"
        >
          <span class="inline-flex items-center gap-2">
            <span class="i-heroicons-user text-base" aria-hidden="true" />
            {{ statusText }}
          </span>
        </div>
        <div class="relative">
          <details class="group">
            <summary
              class="list-none inline-flex items-center gap-2 cursor-pointer rounded-md px-3 py-2 bg-[var(--surface-alt)] text-[var(--text)] border border-[var(--border)] hover:bg-[color-mix(in_srgb,var(--surface-alt)_92%,black)]"
              aria-label="Changer de thème"
            >
              <span class="i-heroicons-swatch text-lg" aria-hidden="true" />
              <span class="text-sm font-medium">{{ themeLabel }}</span>
            </summary>
            <div
              class="absolute right-0 mt-2 w-56 bg-[var(--surface)] text-[var(--text)] border border-[var(--border)] rounded-md shadow-lg p-1 z-50"
              role="menu"
            >
              <button class="w-full text-left px-3 py-2 rounded hover:bg-[var(--surface-alt)]" @click="setTheme('light')">Clair</button>
              <button class="w-full text-left px-3 py-2 rounded hover:bg-[var(--surface-alt)]" @click="setTheme('dark')">Sombre (noir)</button>
              <button class="w-full text-left px-3 py-2 rounded hover:bg-[var(--surface-alt)]" @click="setTheme('rg')">Roland‑Garros</button>
            </div>
          </details>
        </div>
      </div>

      <!-- Mobile hamburger -->
      <div class="md:hidden">
        <button
          ref="menuButtonRef"
          type="button"
          class="inline-flex items-center justify-center rounded-md p-2 text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500"
          :aria-expanded="isMenuOpen"
          aria-controls="mobile-menu"
          aria-label="Ouvrir le menu"
          @click="toggleMenu"
        >
          <span class="sr-only">Ouvrir le menu</span>
          <span class="i-heroicons-bars-3 text-2xl" aria-hidden="true" />
        </button>
      </div>
    </div>

    <!-- Mobile menu overlay -->
    <div v-show="isMenuOpen" class="md:hidden fixed inset-0 z-40 bg-black/20" @click="onBackdropClick">
      <div
        ref="menuPanelRef"
        id="mobile-menu"
        class="absolute left-0 right-0 top-0 bg-[var(--surface)] border-b border-[var(--border)] shadow-lg origin-top transition-transform duration-150"
        :style="{ transform: isMenuOpen ? 'translateY(0)' : 'translateY(-8px)' }"
      >
        <div class="px-4 py-3 flex items-center justify-between">
          <span class="text-lg font-semibold">Menu</span>
          <button
            type="button"
            class="rounded p-2 hover:bg-gray-100 dark:hover:bg-gray-800 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500"
            aria-label="Fermer le menu"
            @click="closeMenu"
          >
            <span class="i-heroicons-x-mark text-xl" aria-hidden="true" />
          </button>
        </div>
        <nav class="px-4 pb-4 flex flex-col gap-2" role="navigation" aria-label="Navigation mobile">
          <router-link
            to="/"
            class="px-3 py-2 rounded hover:bg-[var(--surface-alt)] focus-visible:ring-2 focus-visible:ring-[var(--ring)]"
            :class="route.path === '/' ? 'text-[var(--accent)]' : 'text-[var(--text)]'"
            :aria-current="route.path === '/' ? 'page' : undefined"
            @click="onMenuLinkClick"
          >Accueil</router-link>

          <router-link
            to="/quiz"
            class="px-3 py-2 rounded hover:bg-[var(--surface-alt)] focus-visible:ring-2 focus-visible:ring-[var(--ring)]"
            :class="route.path === '/quiz' ? 'text-[var(--accent)]' : 'text-[var(--text)]'"
            :aria-current="route.path === '/quiz' ? 'page' : undefined"
            @click="onMenuLinkClick"
          >Quiz</router-link>

          <router-link
            to="/quiz/1/leaderboard"
            class="px-3 py-2 rounded hover:bg-[var(--surface-alt)] focus-visible:ring-2 focus-visible:ring-[var(--ring)]"
            :class="(route.path.startsWith('/quiz') && route.path.includes('/leaderboard')) ? 'text-[var(--accent)]' : 'text-[var(--text)]'"
            :aria-current="(route.path.startsWith('/quiz') && route.path.includes('/leaderboard')) ? 'page' : undefined"
            @click="onMenuLinkClick"
          >Classement</router-link>

          <router-link
            to="/admin"
            class="px-3 py-2 rounded hover:bg-[var(--surface-alt)] focus-visible:ring-2 focus-visible:ring-[var(--ring)]"
            :class="(route.path.startsWith('/admin')) ? 'text-[var(--accent)]' : 'text-[var(--text)]'"
            :aria-current="(route.path.startsWith('/admin')) ? 'page' : undefined"
            @click="onMenuLinkClick"
          >Admin</router-link>
        </nav>

        <div class="px-4 pb-4 text-sm text-gray-600 dark:text-gray-300" aria-live="polite">
          {{ statusText }}
        </div>
        <div class="px-4 pb-4">
          <div class="grid grid-cols-1 gap-2">
            <button class="px-3 py-2 rounded border border-[var(--border)] hover:bg-[var(--surface-alt)]" @click="setTheme('light')">Clair</button>
            <button class="px-3 py-2 rounded border border-[var(--border)] hover:bg-[var(--surface-alt)]" @click="setTheme('dark')">Sombre (noir)</button>
            <button class="px-3 py-2 rounded border border-[var(--border)] hover:bg-[var(--surface-alt)]" @click="setTheme('rg')">Roland‑Garros</button>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
/* Aucune animation lourde, transitions courtes seulement */
</style>


