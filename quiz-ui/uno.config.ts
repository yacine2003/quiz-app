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
    /* Les couleurs directes ne sont plus nécessaires,
       on passe par des variables CSS de thème */
    colors: {}
  },
  shortcuts: {
    'btn-primary': 'px-6 py-3 rounded-lg bg-[var(--accent)] text-white hover:bg-[var(--accent-hover)] transition-colors font-semibold shadow-md hover:shadow-lg active:scale-95',
    'btn-secondary': 'px-6 py-3 rounded-lg bg-[var(--surface-alt)] text-[var(--text)] hover:bg-[color-mix(in_srgb,var(--surface-alt)_90%,black)] border border-[var(--border)] transition-colors font-semibold',
    'card': 'bg-[var(--surface)] text-[var(--text)] rounded-2xl shadow-xl p-8 border border-[var(--border)]',
    'input': 'w-full px-4 py-3 rounded-lg border-2 border-[var(--border)] bg-[var(--surface)] text-[var(--text)] focus:ring-2 focus:ring-[var(--ring)] focus:border-transparent outline-none transition'
  },
  safelist: [
    'i-heroicons-trophy',
    'i-heroicons-clock',
    'i-heroicons-fire',
    'i-heroicons-check-circle',
    'i-heroicons-x-circle',
    'i-heroicons-moon',
    'i-heroicons-sun',
    'i-heroicons-swatch'
  ]
})

