import { defineStore } from 'pinia'

export type ThemeName = 'light' | 'dark' | 'rg'
const STORAGE_KEY = 'quiz-theme'

function detectSystemTheme(): ThemeName {
  if (typeof window === 'undefined') return 'light'
  const prefersDark = window.matchMedia?.('(prefers-color-scheme: dark)').matches
  return prefersDark ? 'dark' : 'light'
}

function applyThemeAttribute(theme: ThemeName) {
  const el = document.documentElement
  if (theme === 'light') {
    el.removeAttribute('data-theme')
    el.classList.remove('dark')
  } else {
    el.setAttribute('data-theme', theme)
    // Activer également la classe .dark pour les utilitaires `dark:` existants
    if (theme === 'dark') el.classList.add('dark')
    else el.classList.remove('dark')
  }
}

export const useThemeStore = defineStore('theme', {
  state: () => ({
    current: (localStorage.getItem(STORAGE_KEY) as ThemeName) || detectSystemTheme(),
  }),
  actions: {
    init() {
      applyThemeAttribute(this.current)
    },
    setTheme(theme: ThemeName) {
      this.current = theme
      localStorage.setItem(STORAGE_KEY, theme)
      applyThemeAttribute(theme)
    },
    cycle() {
      const order: ThemeName[] = ['light', 'dark', 'rg']
      const idx = order.indexOf(this.current)
      const next = order[(idx + 1) % order.length]
      this.setTheme(next)
    }
  }
})


