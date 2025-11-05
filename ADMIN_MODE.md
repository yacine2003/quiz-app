# Mode Administrateur - Guide d'utilisation

## 🎯 Vue d'ensemble

Le mode administrateur a été implémenté selon les consignes de votre professeur. Il permet de gérer toutes les questions des quiz de l'application.

## 🔐 Accès

### URL
```
http://localhost:3000/admin
```

### Mot de passe
```
iloveflask
```

Le mot de passe est stocké sous forme de hash MD5 dans le fichier `quiz-api/config.py`.

## 🏗️ Architecture

L'implémentation suit exactement les consignes du professeur avec une navigation claire :

### 1. **Admin.vue** (Page principale - Liste)
- Affichage conditionné par la présence du token dans le localStorage
- **Si le token est "falsy"** : Formulaire de connexion avec champ mot de passe et bouton "Connexion"
- **Si le token est "truthy"** : Dashboard d'administration avec liste des questions
- Statistiques en temps réel par quiz et par difficulté
- Bouton "Créer une question" qui redirige vers `/admin/questions/new`
- Liste cliquable : chaque question redirige vers sa page de détail

### 2. **QuestionDetail.vue** (Page d'affichage d'une question)
- Affichage détaillé d'une question avec tous ses éléments
- Titre de question
- Intitulé de question
- Image (si présente)
- Liste de chaque réponse possible, avec marqueur de la bonne réponse
- Bouton "Éditer" qui redirige vers `/admin/questions/:id/edit`
- Bouton "Supprimer" qui supprime la question et retourne à la liste
- Bouton "Déconnexion" accessible dans toute la zone

### 3. **QuestionEdit.vue** (Page d'édition/création)
- Crée une **copie locale** de la question (principe des props mentionné par le professeur)
- Formulaire complet avec tous les champs :
  - Quiz ID et position (champ "Position" pour modifier la position dans le quiz)
  - Champ "Titre"
  - Champ "Intitulé"
  - **Bouton d'upload d'image** + aperçu de l'image chargée
  - Difficulté (facile, moyen, difficile)
  - 4 réponses avec sélection de la bonne réponse (clic sur le rond)
  - Tags (ajout/suppression dynamique)
  - Explication
- Validation des données avant sauvegarde
- Bouton "Annuler" qui retourne à la page appropriée
- Bouton "Enregistrer" / "Créer"
- Bouton "Déconnexion" toujours accessible

### 4. **QuestionsList.vue** (Composant de liste)
- Affiche toutes les questions avec filtrage par quiz et recherche textuelle
- Chaque item est cliquable et pointe vers la page de détail
- Boutons d'action (Créer, Supprimer, Actualiser)

### 5. **QuestionAdminDisplay.vue** (Composant d'affichage compact)
- Utilisé dans la liste pour afficher chaque question
- Indicateurs visuels (difficulté, quiz, tags)
- Mise en évidence de la bonne réponse

## 🔑 Fonctionnalités

### Authentification
- Le token JWT est stocké dans le **localStorage** après connexion réussie
- Le token est automatiquement ajouté aux requêtes API via un intercepteur Axios
- Durée de validité : 24 heures
- Déconnexion : supprime le token du localStorage

### Navigation
Le parcours utilisateur suit une logique claire :
1. **Liste** (`/admin`) → Clic sur une question → **Détail** (`/admin/questions/:id`)
2. **Détail** → Clic sur "Éditer" → **Édition** (`/admin/questions/:id/edit`)
3. **Édition** → Clic sur "Enregistrer" → Retour au **Détail**
4. **Liste** → Clic sur "Créer une question" → **Création** (`/admin/questions/new`)
5. **Création** → Clic sur "Créer" → Redirection vers le **Détail** de la nouvelle question

### Gestion des questions
- ✅ **Créer** une nouvelle question
- ✅ **Voir le détail** d'une question (page dédiée)
- ✅ **Éditer** une question existante (page dédiée)
- ✅ **Supprimer** une question (avec confirmation)
- ✅ **Filtrer** par quiz (1, 2, 3)
- ✅ **Rechercher** par texte (titre, contenu, tags)
- ✅ **Actualiser** la liste

### Upload d'images
- Bouton d'upload dans le formulaire d'édition/création
- Aperçu en temps réel de l'image sélectionnée
- Suggestion automatique du chemin `/images/questions/`
- Note : les images doivent être placées manuellement dans `/public/images/questions/` pour le moment

### Validation
- Titre requis
- Texte de la question requis
- Au moins une réponse correcte
- Toutes les réponses doivent avoir un texte

## 🎨 Interface utilisateur

### Page de connexion
- Formulaire centré avec icône de cadenas
- Gestion des erreurs de connexion
- Loading state pendant l'authentification
- Lien de retour vers l'accueil

### Dashboard (Page liste)
- **Header sticky** avec navigation et déconnexion
- **Statistiques** : Total questions, répartition par difficulté et par quiz
- **Filtres** : Boutons pour filtrer par quiz avec compteurs
- **Recherche** : Barre de recherche en temps réel
- **Liste cliquable** : Chaque question redirige vers sa page de détail

### Page de détail
- **Navigation claire** : Retour à la liste + Déconnexion
- **Affichage complet** : Titre, intitulé, image, réponses avec marqueur de la bonne
- **Actions** : Éditer et Supprimer en haut de page
- **Tags et explication** : Affichés si présents

### Page d'édition/création
- **Formulaire structuré** : Tous les champs bien organisés
- **Upload d'image** : Zone de drag & drop avec aperçu
- **Sélection de la bonne réponse** : Clic sur le rond vert
- **Validation en temps réel** : Messages d'erreur clairs
- **Actions** : Annuler et Enregistrer/Créer

### Ergonomie (comme demandé)
- Design moderne et responsive
- Dark mode support
- Transitions et animations fluides
- États de chargement (spinners)
- Messages de confirmation
- Validation en temps réel
- **Bouton "Déconnexion" toujours accessible** dans toute la zone d'administration

## 🔧 API utilisée

### Endpoints d'authentification
```
POST /api/auth/login
Body: { "password": "iloveflask" }
Response: { "token": "eyJ..." }
```

### Endpoints de gestion des questions
```
GET    /api/questions           - Liste toutes les questions
GET    /api/questions/:id       - Récupère une question
POST   /api/questions          - Crée une question (auth requise)
PUT    /api/questions/:id      - Met à jour une question (auth requise)
DELETE /api/questions/:id      - Supprime une question (auth requise)
```

## 📊 État actuel

- ✅ 45 questions dans la base de données
- ✅ 3 quiz configurés (Bases du tennis, Roland-Garros, Tennis avancé)
- ✅ Backend et Frontend fonctionnels
- ✅ Authentification opérationnelle
- ✅ Toutes les opérations CRUD fonctionnent

## 🚀 Comment tester

1. **Démarrer les serveurs** (déjà fait)
   ```bash
   ./start-dev.sh
   ```

2. **Accéder à l'interface admin**
   ```
   http://localhost:3000/admin
   ```

3. **Se connecter**
   - Mot de passe : `iloveflask`
   - Observer le champ de type "password" et le bouton "Connexion"
   - En cas d'erreur : message "Mauvais mot de passe"

4. **Tester le parcours complet**
   
   **Liste des questions :**
   - Observer les statistiques (total, par difficulté, par quiz)
   - Tester les filtres par quiz (1, 2, 3)
   - Tester la barre de recherche
   - Cliquer sur "Actualiser"
   - Observer le bouton "Déconnexion" toujours visible
   
   **Voir le détail d'une question :**
   - Cliquer sur n'importe quelle question dans la liste
   - Observer le titre, l'intitulé, l'image (si présente)
   - Observer la liste des réponses avec marqueur de la bonne réponse
   - Tester le bouton "Retour à la liste"
   
   **Éditer une question existante :**
   - Depuis le détail, cliquer sur "Éditer"
   - Modifier le champ "Position"
   - Modifier le champ "Titre"
   - Modifier le champ "Intitulé"
   - Tester l'upload d'image (bouton + aperçu)
   - Changer la réponse correcte (clic sur les ronds)
   - Ajouter/supprimer des tags
   - Cliquer sur "Enregistrer"
   - Vérifier le retour au détail avec les modifications
   
   **Supprimer une question :**
   - Depuis le détail, cliquer sur "Supprimer"
   - Confirmer la suppression
   - Vérifier le retour à la liste
   
   **Créer une nouvelle question :**
   - Depuis la liste, cliquer sur "Créer une question"
   - Remplir tous les champs obligatoires
   - Uploader une image
   - Sélectionner la bonne réponse
   - Cliquer sur "Créer"
   - Vérifier la redirection vers le détail de la nouvelle question
   
   **Déconnexion :**
   - Cliquer sur "Déconnexion" depuis n'importe quelle page admin
   - Vérifier le retour à la page d'accueil
   - Essayer d'accéder à `/admin` → on revoit le formulaire de connexion

## 📝 Notes techniques

### Gestion des props (principe mentionné par le professeur)
Dans `QuestionEdition.vue`, nous créons une **copie locale** de la question reçue via props :
```typescript
watch(() => props.question, (newQuestion) => {
  if (newQuestion) {
    localQuestion.value = {
      ...newQuestion,
      tags: [...(newQuestion.tags || [])],
      choices: newQuestion.choices.map(c => ({ ...c }))
    }
  }
})
```

Cela permet d'éditer les données sans modifier directement les props, respectant ainsi les bonnes pratiques Vue.js.

### Storage du token
```typescript
// Sauvegarde après login
localStorage.setItem('auth_token', response.token)

// Lecture pour vérification
const token = localStorage.getItem('auth_token')

// Suppression à la déconnexion
localStorage.removeItem('auth_token')
```

### Protection des routes
Le router vérifie automatiquement la présence du token pour la route `/admin` :
```typescript
if (to.meta.requiresAuth) {
  const token = localStorage.getItem('auth_token')
  if (!token) {
    next({ name: 'home' })
    return
  }
}
```

### 📁 Fichiers créés/modifiés

**Vues principales :**
- ✅ `/quiz-ui/src/views/Admin.vue` (liste + authentification)
- ✅ `/quiz-ui/src/views/QuestionDetail.vue` (page de détail, nouveau)
- ✅ `/quiz-ui/src/views/QuestionEdit.vue` (page d'édition/création, nouveau)

**Composants :**
- ✅ `/quiz-ui/src/components/QuestionsList.vue` (liste des questions, nouveau)
- ✅ `/quiz-ui/src/components/QuestionAdminDisplay.vue` (affichage compact, nouveau)
- ✅ `/quiz-ui/src/components/QuestionEdition.vue` (formulaire modal, conservé pour compatibilité)

**Services et routing :**
- ✅ `/quiz-ui/src/services/api.ts` (méthodes CRUD ajoutées)
- ✅ `/quiz-ui/src/router/index.ts` (routes admin ajoutées)

**Documentation :**
- ✅ `/ADMIN_MODE.md` (documentation complète)

## 🎓 Conformité avec les consignes

✅ **Bouton "Déconnexion" accessible dans toute la zone d'administration**  
✅ **Page de login** avec champ password + bouton "Connexion" + message potentiel "Mauvais mot de passe"  
✅ **Page de liste des questions** avec bouton "Créer une question" et liste cliquable  
✅ **Page d'affichage de question** avec bouton "Éditer", bouton "Supprimer", titre, intitulé, et marqueur de bonne réponse  
✅ **Page d'édition de question** avec champs Position, Titre, Intitulé, et bouton d'upload d'image + aperçu  
✅ Stocker le token d'authentification dans le local storage  
✅ Architecture avec composant page Admin.vue conditionné par le token  
✅ Copie locale de la question dans QuestionEdit (principe des props)  
✅ Ergonomie soignée  
✅ Notions transposables à d'autres frameworks

## 🎉 Résultat

Le mode administrateur est **entièrement fonctionnel** et prêt à être démontré !

