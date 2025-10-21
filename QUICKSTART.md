# 🚀 Guide de Démarrage Rapide

## Option 1 : Docker (Recommandé - 2 minutes)

```bash
# À la racine du projet
docker-compose up --build

# En arrière-plan
docker-compose up -d --build
```

**URLs disponibles :**
- Frontend : http://localhost:3000
- Backend API : http://localhost:5001

**Commandes Docker utiles :**
```bash
# Voir les logs
docker-compose logs -f

# Arrêter
docker-compose down

# Nettoyer tout
docker-compose down -v
docker system prune -a
```

## Option 2 : Installation Locale (5 minutes)

### 1. Backend Flask

```bash
cd quiz-api

# Créer environnement virtuel Python
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Installer dépendances
pip install -r requirements.txt

# Importer les 15 questions
python import_questions.py

# Lancer le serveur
python app_new.py
```

✅ API disponible sur http://localhost:5001

### 2. Frontend Vue

**Dans un nouveau terminal :**

```bash
cd quiz-ui

# Installer dépendances
npm install

# Lancer le serveur de développement
npm run dev
```

✅ Application disponible sur http://localhost:3000

## Premiers Pas

### 1. Accéder à l'application

Ouvrir http://localhost:3000 dans le navigateur

### 2. Participer à un quiz

1. Page d'accueil : Cliquer sur "Quiz Tennis"
2. Entrer votre pseudo (2-20 caractères)
3. Cliquer "Démarrer le quiz"
4. Répondre aux 15 questions
5. Voir votre score
6. Consulter le classement

### 3. Administration (optionnel)

**Mot de passe admin :** `iloveflask`

#### Se connecter

```bash
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"password":"iloveflask"}'
```

Réponse : `{"token":"..."}`

#### Créer une question

```bash
curl -X POST http://localhost:5001/api/questions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer VOTRE_TOKEN" \
  -d '{
    "quiz_id": 1,
    "position": 16,
    "title": "Question 16",
    "text": "Nouvelle question?",
    "difficulty": "easy",
    "tags": ["tennis"],
    "explanation": "Explication...",
    "choices": [
      {"text": "Réponse A", "is_correct": true},
      {"text": "Réponse B", "is_correct": false},
      {"text": "Réponse C", "is_correct": false},
      {"text": "Réponse D", "is_correct": false}
    ]
  }'
```

## Tests

### Tests unitaires

```bash
cd quiz-ui
npm run test
```

### Tests E2E

```bash
cd quiz-ui
npx playwright install  # Premier lancement uniquement
npm run test:e2e
```

## Données Incluses

✅ **15 questions de tennis** pré-importées :
- Difficulté : Easy
- Tags : tennis, sport, histoire, règles, etc.
- Format : Multiple choice (A, B, C, D)

## Troubleshooting

### Port 5001 déjà utilisé

```bash
# macOS/Linux
lsof -ti tcp:5001 | xargs kill -9

# Windows
netstat -ano | findstr :5001
taskkill /PID <PID> /F
```

### Port 3000 déjà utilisé

```bash
# macOS/Linux
lsof -ti tcp:3000 | xargs kill -9

# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Erreur "Module not found"

```bash
cd quiz-ui
rm -rf node_modules package-lock.json
npm install
```

### Base de données corrompue

```bash
cd quiz-api
rm quiz.db quiz.db-journal
python import_questions.py
```

## Architecture Rapide

```
Frontend (Vue 3 + TypeScript)
    ↓ HTTP (Axios)
Backend (Flask + SQLite)
    ↓ SQLAlchemy ORM
Database (SQLite)
```

## Fonctionnalités Clés

✅ **Front Office**
- Liste des quiz disponibles
- Démarrage du quiz avec pseudo
- 15 questions interactives
- Timer en temps réel
- Sauvegarde auto de progression
- Page de score animée
- Leaderboard avec podium

✅ **Back Office**
- Authentification JWT
- CRUD questions (API REST)

✅ **Technique**
- PWA (Progressive Web App)
- Mode sombre automatique
- Responsive design
- Performance optimisée
- Tests unitaires + E2E
- Docker ready
- CI/CD GitHub Actions

## Documentation Complète

- **README.md** - Documentation générale
- **DEPLOYMENT.md** - Guide de déploiement production
- **quiz-api/README.md** - Documentation API
- **quiz-ui/README.md** - Documentation Frontend

## Support

📧 Questions ? Ouvrez une issue sur GitHub

🎯 **Bon quiz !**

