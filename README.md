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
- 🎨 **3 Modes d'affichage** : Clair, Sombre (noir complet), Roland-Garros (terre battue)
- 📱 **Responsive** : Design mobile-first
- ⚡ **Performance optimisée** : Code splitting, lazy loading
- 🔄 **PWA** : Installation et utilisation hors-ligne
- 🎨 **UI Moderne** : Animations fluides, design épuré avec UnoCSS

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

### Installation et lancement

#### Option 1 — Tout-en-un (script automatique)

```bash
cd /Users/aminesaddik/Documents/ESIEE/E4/ProjetWEB/quiz-app
chmod +x ./start-dev.sh
./start-dev.sh
```

Ce script lance automatiquement le backend et le frontend.

#### Option 2 — Manuellement (2 terminaux séparés)

**Terminal 1 (Backend Flask)**

```bash
cd /Users/aminesaddik/Documents/ESIEE/E4/ProjetWEB/quiz-app
source venv/bin/activate
cd quiz-api
pip install -r requirements.txt
python app_new.py
```

Le backend sera disponible sur `http://localhost:5001`

**Terminal 2 (Frontend Vite)**

```bash
cd /Users/aminesaddik/Documents/ESIEE/E4/ProjetWEB/quiz-app/quiz-ui
npm install
npm run dev
```

Le frontend sera disponible sur `http://localhost:3000`

#### Pour arrêter les serveurs

```bash
# Arrêter le backend (port 5001)
lsof -ti:5001 | xargs kill -9 2>/dev/null

# Arrêter le frontend (port 3000)
lsof -ti:3000 | xargs kill -9 2>/dev/null
```

## 🐳 Docker

### Démarrage Docker (macOS, zsh)

```bash
# 1) Démarrer Docker Desktop
open -a Docker

# 2) Vérifier que le démon est prêt
docker version
docker info
docker ps

# 3) Lancer les services en production locale
cd /Users/aminesaddik/Documents/ESIEE/E4/ProjetWEB/quiz-app
docker compose up -d --build
docker compose ps

# 4) Ouvrir les URLs
open http://localhost:5001/health
open http://localhost:3000

# 5) Logs en direct (si besoin)
docker compose logs -f --tail=100 api frontend

# 6) Mode développement (hot‑reload)
docker compose -f docker-compose.dev.yml up -d --build

# 7) Arrêter et nettoyer
docker compose down
docker compose down -v
docker system prune -f

# 8) Dépannage « Cannot connect to the Docker daemon »
unset DOCKER_HOST
docker context ls
docker context use desktop-linux   # sur Mac avec Docker Desktop
open -a Docker
```

### Build et lancement

```bash
cd /Users/aminesaddik/Documents/ESIEE/E4/ProjetWEB/quiz-app

# Build et démarrage des conteneurs (production)
docker compose up -d --build

# Arrêter les conteneurs
docker compose down

# Nettoyer volumes et images
docker compose down -v
docker system prune -a
```

### Services disponibles

- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:5001
- **Health checks** : 
  - Frontend: http://localhost:3000/health
  - Backend: http://localhost:5001/health

### Variables d'environnement

Les variables sont configurées dans `docker-compose.yml` :

```yaml
# Backend
FLASK_ENV=production
DATABASE_URL=sqlite:////app/data/quiz.db
CORS_ORIGINS=http://localhost:3000,http://localhost:80

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

### Tests Postman

Pour lancer les tests Postman de l'API :

1. Ouvrez Postman
2. Importez la collection de tests fournie
3. **IMPORTANT** : Configurez l'environnement avec la variable suivante :
   - Variable : `baseUrl`
   - Valeur : `http://localhost:5001/api`
4. Assurez-vous que le backend est lancé (port 5001)
5. Lancez les tests

> ⚠️ **Note** : Ne modifiez pas les tests Postman eux-mêmes, seulement la variable d'environnement `baseUrl`.

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

## 📝 Notes importantes

- **Mot de passe admin** : `iloveflask`
- **Thèmes disponibles** : 
  - 🌞 Clair (bleu foncé #0369a1)
  - 🌙 Sombre (noir complet)
  - 🎾 Roland-Garros (terre battue)
- **Tests Postman** : Variable `baseUrl` = `http://localhost:5001/api`
- **Ports par défaut** :
  - Backend : 5001
  - Frontend : 3000 (dev) / 80 (Docker)

**Deadline** : 9 novembre 2025 23h59

🎯 Bon quiz ! 🎾
