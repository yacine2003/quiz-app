/**
 * Point d'entrée de l'application Vue
 */
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { VueQueryPlugin } from '@tanstack/vue-query'
import App from './App.vue'
import router from './router'
import { useThemeStore } from './stores/theme'

// Import UnoCSS
import 'uno.css'
import '@unocss/reset/tailwind.css'

// Import styles personnalisés
import './assets/main.css'

const app = createApp(App)

// Plugins
app.use(createPinia())
app.use(router)
app.use(VueQueryPlugin, {
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      cacheTime: 1000 * 60 * 10, // 10 minutes
      refetchOnWindowFocus: false,
      retry: 1
    }
  }
})

// Initialiser le thème AVANT le montage pour éviter le FOUC
const themeStore = useThemeStore()
themeStore.init()

app.mount('#app')

