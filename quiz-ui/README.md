# Quiz UI - Frontend Vue 3 + TypeScript

Interface utilisateur moderne et responsive pour l'application Quiz.

## Démarrage rapide

```bash
# Installer les dépendances
npm install

# Lancer le serveur de développement
npm run dev
```

Application disponible sur http://localhost:3000

## Scripts

```bash
npm run dev          # Serveur de développement
npm run build        # Build production
npm run preview      # Preview du build
npm run lint         # Linter ESLint
npm run typecheck    # Vérification TypeScript
npm run test         # Tests unitaires (Vitest)
npm run test:e2e     # Tests E2E (Playwright)
```

## Structure

```
src/
├── components/      # Composants réutilisables
├── views/          # Pages/routes
├── stores/         # Pinia stores
├── services/       # API clients
├── types/          # TypeScript types
├── router/         # Vue Router
└── assets/         # CSS, images
```

## Technologies

- **Vue 3** - Framework progressif
- **TypeScript** - Type safety
- **Pinia** - State management
- **Vue Router** - Routing
- **TanStack Query** - Data fetching
- **UnoCSS** - Utility-first CSS
- **Vite** - Build tool

## Configuration

Variables d'environnement (`.env.local`) :

```
VITE_API_URL=http://localhost:5001/api
```

## Thèmes (Light, Sombre noir, Roland‑Garros)

- Sélecteur de thème dans le Header (Clair / Sombre (noir) / Roland‑Garros).
- Persistance via localStorage (`quiz-theme`).
- Les couleurs sont centralisées via variables CSS:
  - Light (par défaut) → `:root`
  - Dark noir → `[data-theme="dark"]`
  - Roland‑Garros → `[data-theme="rg"]`

Pour ajouter un 4e thème, ajoutez une section `[data-theme="nom"]` dans `src/assets/main.css` et appelez `useThemeStore().setTheme('nom')`.

## Features

- 🎨 Design moderne avec UnoCSS
- 🌙 Mode sombre automatique
- 📱 Responsive mobile-first
- ⚡ Performance optimisée
- 🔄 PWA ready
- 💾 Sauvegarde automatique
