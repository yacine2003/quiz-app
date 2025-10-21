import { defineConfig, presetUno, presetIcons, presetTypography } from 'unocss'

export default defineConfig({
  presets: [
    presetUno(),
    presetIcons({
      scale: 1.2,
      cdn: 'https://esm.sh/'
    }),
    presetTypography()
  ],
  theme: {
    colors: {
      primary: {
        50: '#f0f9ff',
        100: '#e0f2fe',
        200: '#bae6fd',
        300: '#7dd3fc',
        400: '#38bdf8',
        500: '#0ea5e9',
        600: '#0284c7',
        700: '#0369a1',
        800: '#075985',
        900: '#0c4a6e'
      }
    }
  },
  shortcuts: {
    'btn-primary': 'px-6 py-3 rounded-lg bg-primary-600 text-white hover:bg-primary-700 transition-colors font-semibold shadow-md hover:shadow-lg active:scale-95',
    'btn-secondary': 'px-6 py-3 rounded-lg bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors font-semibold',
    'card': 'bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 border border-gray-100 dark:border-gray-700',
    'input': 'w-full px-4 py-3 rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition'
  },
  safelist: [
    'i-heroicons-trophy',
    'i-heroicons-clock',
    'i-heroicons-fire',
    'i-heroicons-check-circle',
    'i-heroicons-x-circle',
    'i-heroicons-moon',
    'i-heroicons-sun'
  ]
})

