# 🎯 Quiz App - Application de Quiz Interactive

Application web full-stack moderne permettant de créer, participer et gérer des quiz interactifs avec système de classement.

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Stack Technique](#-stack-technique)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Docker](#-docker)
- [Développement](#-développement)
- [Tests](#-tests)
- [Déploiement](#-déploiement)
- [API Documentation](#-api-documentation)

## ✨ Fonctionnalités

### Front Office (Public)
- 🏠 **Page d'accueil** : Liste des quiz disponibles
- 🚀 **Démarrage du quiz** : Saisie du pseudo et informations du quiz
- ❓ **Questions interactives** : Choix multiples avec navigation fluide
- 📊 **Page de score** : Résultats détaillés avec animations
- 🏆 **Leaderboard** : Classement en temps réel avec podium

### Back Office (Admin)
- 🔐 **Authentification** : Protection par mot de passe (`iloveflask`)
- ✏️ **CRUD Questions** : Gestion complète des questions

### Fonctionnalités techniques
- 💾 **Sauvegarde automatique** : Progression sauvegardée en localStorage
- 🌙 **Mode sombre** : Thème adaptatif automatique
- 📱 **Responsive** : Design mobile-first
- ⚡ **Performance optimisée** : Code splitting, lazy loading
- 🔄 **PWA** : Installation et utilisation hors-ligne
- 🎨 **UI Moderne** : Animations fluides, design épuré

## 🛠 Stack Technique

### Backend
- **Framework** : Flask 2.3.3 (Python 3.13)
- **ORM** : SQLAlchemy 2.0.43
- **Database** : SQLite
- **Auth** : JWT (PyJWT 2.5.0)
- **CORS** : Flask-CORS 6.0.1

### Frontend
- **Framework** : Vue 3.5.22 (Composition API)
- **Build Tool** : Vite 7.1.7
- **Language** : TypeScript 5.9.3
- **State Management** : Pinia 3.0.3
- **Routing** : Vue Router 4.5.1
- **Data Fetching** : TanStack Query 5.90.5
- **HTTP Client** : Axios 1.12.2
- **CSS Framework** : UnoCSS 0.66.5
- **Utilities** : VueUse 12.0.0
- **Validation** : Zod 4.1.12

### DevOps
- **Containerization** : Docker & Docker Compose
- **CI/CD** : GitHub Actions
- **Web Server** : Nginx (production)

## 🏗 Architecture

```
quiz-app/
├── quiz-api/           # Backend Flask
│   ├── routes/        # Blueprints API
│   ├── models.py      # Modèles SQLAlchemy
│   ├── config.py      # Configuration
│   ├── app_new.py     # Application factory
│   └── Dockerfile
├── quiz-ui/           # Frontend Vue
│   ├── src/
│   │   ├── components/  # Composants réutilisables
│   │   ├── views/       # Pages/routes
│   │   ├── stores/      # Pinia stores
│   │   ├── services/    # API clients
│   │   ├── types/       # TypeScript types
│   │   └── router/      # Vue Router config
│   ├── Dockerfile
│   └── nginx.conf
├── data/              # Données quiz (JSON/CSV)
├── docker-compose.yml
└── .github/workflows/ # CI/CD pipelines
```

### Schéma de base de données

```sql
quizzes
├── id (PK)
├── title
├── description
├── difficulty
└── is_published

questions
├── id (PK)
├── quiz_id (FK)
├── position
├── title
├── text
├── image
├── difficulty
├── tags (JSON)
└── explanation

choices
├── id (PK)
├── question_id (FK)
├── text
└── is_correct

attempts
├── id (PK)
├── quiz_id (FK)
├── player_name
├── score
├── total_questions
├── time_spent
└── created_at

answers
├── id (PK)
├── attempt_id (FK)
├── question_id (FK)
├── choice_id (FK)
├── is_correct
└── timestamp
```

## 🚀 Installation

### Prérequis

- Python 3.13+
- Node.js 20+ ou 22+
- npm ou pnpm
- Docker & Docker Compose (optionnel)

### Installation locale

#### Backend

```bash
cd quiz-api

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Importer les questions
python import_questions.py

# Lancer le serveur
python app_new.py
```

Le backend sera disponible sur `http://localhost:5001`

#### Frontend

```bash
cd quiz-ui

# Installer les dépendances
npm install

# Lancer le serveur de développement
npm run dev
```

Le frontend sera disponible sur `http://localhost:3000`

## 🐳 Docker

### Build et lancement

```bash
# Build et démarrage des conteneurs
docker-compose up --build

# En arrière-plan
docker-compose up -d --build

# Arrêter les conteneurs
docker-compose down

# Nettoyer volumes et images
docker-compose down -v
docker system prune -a
```

### Services disponibles

- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:5001
- **Health checks** : 
  - Frontend: http://localhost:3000/health
  - Backend: http://localhost:5001/health

### Variables d'environnement

Créer un fichier `.env` à la racine :

```env
# Backend
FLASK_ENV=development
DATABASE_URL=sqlite:///quiz.db
JWT_SECRET_KEY=Groupe 2
CORS_ORIGINS=http://localhost:3000

# Frontend
VITE_API_URL=http://localhost:5001/api
```

## 💻 Développement

### Backend

```bash
cd quiz-api

# Linter
autopep8 --in-place --recursive .

# Tests
python -m pytest

# Créer une migration
# (SQLAlchemy crée automatiquement les tables au démarrage)
```

### Frontend

```bash
cd quiz-ui

# Linter
npm run lint

# Type checking
npm run typecheck

# Tests unitaires
npm run test

# Tests E2E
npm run test:e2e

# Build
npm run build

# Preview du build
npm run preview
```

## 🧪 Tests

### Tests unitaires (Vitest)

```bash
cd quiz-ui
npm run test
npm run test:ui  # Interface graphique
```

### Tests E2E (Playwright)

```bash
cd quiz-ui
npx playwright install  # Premier lancement
npm run test:e2e
```

## 📦 Déploiement

### Docker Hub

Les images sont automatiquement construites et poussées sur Docker Hub via GitHub Actions lors d'un push sur `main`.

```bash
# Pull des images
docker pull <username>/quiz-api:latest
docker pull <username>/quiz-frontend:latest

# Lancement
docker-compose -f docker-compose.prod.yml up -d
```

### Configuration production

#### Backend
- Activer HTTPS
- Configurer PostgreSQL au lieu de SQLite
- Activer rate limiting
- Configurer les logs
- Variables d'environnement sécurisées

#### Frontend
- Build optimisé (`npm run build`)
- Compression Gzip/Brotli activée
- Cache des assets statiques
- CSP headers configurés

## 📚 API Documentation

### Endpoints publics

#### Quizzes

```http
GET /api/quizzes
GET /api/quizzes/:id
GET /api/quizzes/:id/questions
```

#### Questions

```http
GET /api/questions?quiz_id=:id
GET /api/questions/:id
GET /api/questions?position=:pos  # Legacy
```

#### Attempts

```http
POST /api/attempts
Body: {
  "quiz_id": number,
  "player_name": string,
  "answers": [{ "question_id": number, "choice_id": number }],
  "time_spent": number
}

GET /api/attempts/:id
GET /api/attempts/player/:player_name
```

#### Leaderboard

```http
GET /api/leaderboard/:quiz_id?limit=50
GET /api/leaderboard?limit=50  # Global
```

### Endpoints admin (nécessitent JWT)

#### Auth

```http
POST /api/auth/login
Body: { "password": "iloveflask" }
Response: { "token": "..." }
```

#### CRUD Quizzes

```http
POST /api/quizzes       # Créer
PUT /api/quizzes/:id    # Modifier
DELETE /api/quizzes/:id # Supprimer
```

#### CRUD Questions

```http
POST /api/questions       # Créer
PUT /api/questions/:id    # Modifier
DELETE /api/questions/:id # Supprimer
```

## 🎨 UI/UX

### Design System

- **Couleurs** : Palette Primary (bleu), Success (vert), Warning (jaune), Error (rouge)
- **Typography** : Inter (système de fallbacks)
- **Spacing** : Scale 4px (0.25rem)
- **Border Radius** : 0.5rem, 0.75rem, 1rem, 1.5rem
- **Shadows** : sm, md, lg, xl, 2xl

### Composants clés

- `QuestionCard` : Affichage question + choix
- `LeaderboardTable` : Classement avec podium
- `Timer` : Chronomètre temps réel

## 📄 Licence

Projet académique - ESIEE Paris - Groupe 2

## 👥 Contributeurs

- Équipe Groupe 2

## 📞 Support

Pour toute question ou problème :
- Ouvrir une issue sur GitHub
- Contacter l'équipe de développement

---

**Note** : Mot de passe admin par défaut : `iloveflask`  
**Deadline** : 9 novembre 2025 23h59

🎯 Bon quiz !
