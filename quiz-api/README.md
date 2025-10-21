# Quiz API - Backend Flask

API REST pour l'application Quiz avec authentification JWT et gestion complète des quiz.

## Démarrage rapide

```bash
# Installer les dépendances
pip install -r requirements.txt

# Importer les questions
python import_questions.py

# Lancer le serveur
python app_new.py
```

API disponible sur http://localhost:5001

## Endpoints

### Public
- `GET /api/quizzes` - Liste des quiz
- `GET /api/questions` - Questions d'un quiz
- `POST /api/attempts` - Soumettre une tentative
- `GET /api/leaderboard/:id` - Classement

### Admin (JWT requis)
- `POST /api/auth/login` - Authentification
- `POST /api/questions` - Créer question
- `PUT /api/questions/:id` - Modifier question
- `DELETE /api/questions/:id` - Supprimer question

## Authentification

Mot de passe admin : `iloveflask`

```bash
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"password":"iloveflask"}'
```

## Structure

```
quiz-api/
├── routes/          # Blueprints API
├── models.py        # Modèles SQLAlchemy
├── config.py        # Configuration
├── middleware.py    # Authentification
├── app_new.py       # Application factory
└── import_questions.py  # Script import
```

## Configuration

Variables d'environnement (`.env`) :

```
FLASK_ENV=development
DATABASE_URL=sqlite:///quiz.db
JWT_SECRET_KEY=Groupe 2
CORS_ORIGINS=http://localhost:3000
```

