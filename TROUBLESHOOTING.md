# Guide de Dépannage - Quiz App

## 🔍 Problème : Les images ne s'affichent pas en mode Admin pour quiz 2 et 3

### Diagnostic complet

#### 1. **CAUSE PRINCIPALE IDENTIFIÉE**
Les questions des quiz 2 et 3 étaient créées **sans le champ `image`** dans la base de données.

La fonction `_ensure_15_per_quiz()` dans `quiz-api/routes/quiz_routes.py` créait les questions avec `title`, `text`, `difficulty` mais **oubliait d'ajouter le champ `image`**.

**Preuve :**
```bash
curl -s 'http://localhost:5001/api/questions?quiz_id=2' | jq '.[0].image'
# Résultat : null (au lieu de "/images/questions/q1medium.png")
```

---

### Procédure de Debug Étape par Étape

#### A) **Vérifier l'API Backend**

```bash
# 1. Vérifier que l'API répond
curl http://localhost:5001/health

# 2. Lister les quiz
curl http://localhost:5001/api/quizzes | jq

# 3. Inspecter les questions du quiz 2 (devrait avoir des images)
curl 'http://localhost:5001/api/questions?quiz_id=2' | jq '.[0:3][] | {position, image}'

# 4. Vérifier les logs du conteneur
docker logs quiz-api --tail 50
```

#### B) **Inspecter la Base de Données**

```bash
# Installer sqlite3 dans le container
docker exec -i quiz-api sh -c "apk add --no-cache sqlite"

# Vérifier la structure de la table
docker exec -i quiz-api sqlite3 /app/data/quiz.db ".schema questions"

# Compter les questions par quiz
docker exec -i quiz-api sqlite3 /app/data/quiz.db \
  "SELECT quiz_id, COUNT(*), COUNT(image) FROM questions GROUP BY quiz_id;"

# Voir les URLs d'images
docker exec -i quiz-api sqlite3 /app/data/quiz.db \
  "SELECT id, quiz_id, position, image FROM questions WHERE quiz_id IN (2,3) LIMIT 5;"
```

#### C) **Vérifier les Fichiers Statiques**

```bash
# Lister les images dans le container frontend
docker exec quiz-frontend ls -la /usr/share/nginx/html/images/questions/

# Vérifier qu'une image spécifique existe
docker exec quiz-frontend ls -la /usr/share/nginx/html/images/questions/q1medium.png

# Tester l'accès HTTP
curl -I http://localhost:3000/images/questions/q1medium.png
# Devrait retourner 200 OK
```

#### D) **Vérifier le Frontend (Browser DevTools)**

1. Ouvrir http://localhost:3000/admin
2. Connexion avec mot de passe : `iloveflask`
3. Ouvrir DevTools (F12) → Network
4. Filtrer par "Img"
5. Regarder les requêtes d'images :
   - ✅ Status 200 : OK
   - ❌ Status 404 : Fichier manquant
   - ❌ Status 0 : CORS ou URL invalide

6. Console → chercher les erreurs :
```javascript
// Erreur typique si l'URL est null
Failed to load resource: net::ERR_INVALID_URL
```

#### E) **Vérifier que le Proxy Nginx Fonctionne**

```bash
# Tester l'API via le proxy frontend
curl http://localhost:3000/api/quizzes | jq

# Vérifier la config Nginx dans le container
docker exec quiz-frontend cat /etc/nginx/nginx.conf | grep -A 10 "location /api"
```

---

### ✅ Solution Appliquée

**Fichier modifié :** `quiz-api/routes/quiz_routes.py`

```python
# AVANT (ligne 89-95)
q = Question(
    quiz_id=quiz_id,
    position=pos,
    title=title,
    text=text,
    difficulty=difficulty,
    # ❌ Manque le champ image !
)

# APRÈS (avec correctif)
# Construire l'URL de l'image selon quiz_id et position
image_suffix = 'base' if difficulty == 'easy' else difficulty
image_url = item.get('image') or f"/images/questions/q{pos}{image_suffix}.png"
q = Question(
    quiz_id=quiz_id,
    position=pos,
    title=title,
    text=text,
    difficulty=difficulty,
    image=image_url,  # ✅ Image ajoutée
)
```

**Commandes pour appliquer le correctif :**

```bash
# 1. Rebuild l'API avec le code corrigé
cd /Users/aminesaddik/Documents/ESIEE/E4/ProjetWEB/quiz-app
docker compose up -d --build api

# 2. Vider les questions existantes pour forcer le re-seeding
docker exec -i quiz-api sh -c "apk add --no-cache sqlite && \
  sqlite3 /app/data/quiz.db 'DELETE FROM answers; DELETE FROM choices; DELETE FROM questions;'"

# 3. Relancer l'endpoint pour déclencher le seeding
curl -s 'http://localhost:5001/api/quizzes' > /dev/null

# 4. Vérifier que les images sont présentes
curl 'http://localhost:5001/api/questions?quiz_id=2' | jq '.[0].image'
# Devrait afficher : "/images/questions/q1medium.png"
```

---

### 📋 Checklist de Validation

Après application du correctif, vérifier :

- [ ] Quiz 1 (Base) : 15 questions avec images `/images/questions/q{N}base.png`
- [ ] Quiz 2 (Roland) : 15 questions avec images `/images/questions/q{N}medium.png`
- [ ] Quiz 3 (Avancé) : 15 questions avec images `/images/questions/q{N}hard.png`
- [ ] Mode Admin : toutes les images s'affichent dans la liste
- [ ] Mode Play : toutes les images s'affichent pendant le quiz
- [ ] DevTools Network : aucune erreur 404 sur les images
- [ ] Frontend Docker : images accessibles via http://localhost:3000/images/questions/q1medium.png

```bash
# Commande de validation automatique
for quiz_id in 1 2 3; do
  echo "=== Quiz $quiz_id ==="
  curl -s "http://localhost:5001/api/questions?quiz_id=$quiz_id" | \
    jq -r ".[] | select(.image == null) | \"⚠️  Question \(.position) : image manquante\""
  echo
done
# Si aucun output, toutes les images sont OK ✅
```

---

## 🔄 Mode Développement vs Production

### Mode Développement (Hot-Reload)

**Utiliser `docker-compose.dev.yml` :**

```bash
# Lancer en mode dev avec bind mounts
docker compose -f docker-compose.dev.yml up --build

# Avantages :
# - Modifications du code répercutées instantanément (hot-reload)
# - Pas besoin de rebuild à chaque changement
# - Vite watch + Flask debug activés
```

**Configuration clé dans `docker-compose.dev.yml` :**

```yaml
frontend-dev:
  volumes:
    - ./quiz-ui:/app          # ✅ Bind mount du code source
    - /app/node_modules        # ✅ Exclure node_modules
    - ./quiz-ui/public:/app/public  # ✅ Assets publics
  environment:
    - CHOKIDAR_USEPOLLING=true  # ✅ Pour que Vite détecte les changements
  command: npm run dev -- --host 0.0.0.0 --port 3000
```

**Vite config requis (`quiz-ui/vite.config.js`) :**

```javascript
export default defineConfig({
  server: {
    host: '0.0.0.0',  // ✅ Écouter sur toutes les interfaces
    port: 3000,
    watch: {
      usePolling: true  // ✅ Pour Docker bind mount
    }
  }
})
```

---

### Mode Production (Build Optimisé)

**Utiliser `docker-compose.yml` (standard) :**

```bash
# Build et lancer en mode prod
docker compose up -d --build

# Avantages :
# - Assets minifiés et optimisés
# - Nginx sert les fichiers statiques
# - Performances maximales
```

**Différences clés :**

| Aspect | Dev (bind mount) | Prod (build) |
|--------|------------------|--------------|
| Code source | Monté depuis l'hôte | Copié dans l'image |
| Hot-reload | ✅ Oui (Vite watch) | ❌ Non |
| Assets | Lus depuis `/app/public` | Copiés dans `/usr/share/nginx/html` |
| Performance | Moyenne (overhead watch) | Maximale (minifié) |
| Rebuild | ❌ Pas nécessaire | ✅ Nécessaire après chaque modif |

---

## 🚨 Causes Fréquentes de Divergences Dev/Docker

### 1. **Fichiers manquants dans l'image**
**Symptôme :** Ça marche en local (`npm run dev`) mais pas dans Docker.

**Cause :** Les fichiers dans `public/` ou `src/assets/` ne sont pas copiés dans l'image Docker.

**Solution :**
```dockerfile
# Dans Dockerfile frontend
COPY public/ /app/public/   # ✅ Copier explicitement les assets
```

---

### 2. **Base de données différente**
**Symptôme :** Images présentes en dev local mais pas dans Docker.

**Cause :** Docker utilise une base SQLite vide dans un volume séparé.

**Solution :**
```bash
# Partager le même fichier de base
docker compose down -v  # Supprimer les anciens volumes
docker compose up -d --build  # Recréer avec données fraîches
```

---

### 3. **Chemins absolus vs relatifs**
**Symptôme :** Images chargées avec des URLs absolues qui ne matchent pas.

**Cause :** L'API renvoie des URLs absolues (ex: `https://example.com/images/...`) alors que Docker est sur localhost.

**Solution :**
```python
# Toujours utiliser des chemins relatifs
image_url = "/images/questions/q1base.png"  # ✅ Relatif
# Pas : "http://localhost:3000/images/..."   # ❌ Absolu
```

---

### 4. **Permissions / SELinux**
**Symptôme :** Erreur "Permission denied" dans les logs Docker.

**Cause :** SELinux ou permissions fichiers empêchent l'accès.

**Solution :**
```bash
# Vérifier les permissions
ls -la quiz-ui/public/images/questions/

# Corriger si nécessaire
chmod -R 755 quiz-ui/public/images/
```

---

### 5. **Cache navigateur ou CDN**
**Symptôme :** Images ne se chargent pas malgré correctifs.

**Cause :** Cache navigateur ou proxy garde l'ancienne version.

**Solution :**
```bash
# Forcer le rechargement complet
# Chrome/Firefox : Ctrl + Shift + R (ou Cmd + Shift + R sur Mac)

# Vider le cache Docker
docker compose down
docker system prune -a --volumes
docker compose up --build
```

---

## 📦 Solution Durable pour la Production

### Option A : Object Storage (S3/MinIO) - Recommandée ✅

**Avantages :**
- Scalable (plusieurs instances frontend)
- Sauvegarde automatique
- CDN-ready
- Pas de bind mount nécessaire

**Setup MinIO (S3-compatible) :**

```yaml
# docker-compose.yml
services:
  minio:
    image: minio/minio
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    volumes:
      - minio-data:/data
    command: server /data --console-address ":9001"

volumes:
  minio-data:
```

**Code API modifié :**

```python
import boto3

s3 = boto3.client('s3',
    endpoint_url='http://minio:9000',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin'
)

# Upload image
with open('q1base.png', 'rb') as f:
    s3.upload_fileobj(f, 'quiz-images', 'questions/q1base.png')

# URL publique
image_url = "http://localhost:9000/quiz-images/questions/q1base.png"
```

---

### Option B : Volume Partagé (Simple mais limité)

**Avantages :**
- Simple à mettre en place
- Pas de service externe

**Inconvénients :**
- Ne scale pas (une seule instance)
- Backup manuel

```yaml
services:
  api:
    volumes:
      - shared-images:/app/static/images
  
  frontend:
    volumes:
      - shared-images:/usr/share/nginx/html/images

volumes:
  shared-images:
```

---

## 🏆 Meilleures Pratiques

### 1. **Environnement Dev = Prod (Parity)**
```bash
# Utiliser les mêmes versions Node/Python partout
# Spécifier dans package.json et requirements.txt
```

### 2. **CI/CD Seeding**
```yaml
# .github/workflows/ci.yml
- name: Seed database
  run: |
    docker compose up -d
    docker exec quiz-api python import_questions.py
```

### 3. **Health Checks**
```yaml
# docker-compose.yml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5001/api/quizzes"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### 4. **Validation Automatique**
```bash
# test-images.sh
#!/bin/bash
for quiz_id in 1 2 3; do
  null_count=$(curl -s "http://localhost:5001/api/questions?quiz_id=$quiz_id" | \
    jq '[.[] | select(.image == null)] | length')
  if [ "$null_count" -gt 0 ]; then
    echo "❌ Quiz $quiz_id : $null_count images manquantes"
    exit 1
  fi
done
echo "✅ Toutes les images sont présentes"
```

---

## 📚 Commandes Utiles de Référence

### Docker
```bash
# Rebuild tout
docker compose down -v && docker compose up -d --build

# Voir les logs en temps réel
docker compose logs -f api
docker compose logs -f frontend

# Entrer dans un container
docker exec -it quiz-api sh
docker exec -it quiz-frontend sh

# Lister les fichiers dans un container
docker exec quiz-frontend ls -R /usr/share/nginx/html/images/

# Inspecter une image Docker
docker inspect quiz-app-frontend:latest
```

### API Testing
```bash
# Test complet des endpoints
curl http://localhost:5001/health
curl http://localhost:5001/api/quizzes | jq
curl 'http://localhost:5001/api/questions?quiz_id=1' | jq '.[0]'
curl http://localhost:3000/api/quizzes | jq  # Via proxy Nginx
```

### Database
```bash
# Backup
docker exec quiz-api sqlite3 /app/data/quiz.db ".backup /tmp/backup.db"
docker cp quiz-api:/tmp/backup.db ./backup.db

# Restore
docker cp ./backup.db quiz-api:/tmp/restore.db
docker exec quiz-api sqlite3 /app/data/quiz.db ".restore /tmp/restore.db"

# Query
docker exec quiz-api sqlite3 /app/data/quiz.db \
  "SELECT COUNT(*), COUNT(image) FROM questions;"
```

---

## 🎯 Résumé Exécutif

**Problème :** Images manquantes pour quiz 2 & 3 en mode Admin.

**Cause Racine :** Champ `image` non rempli lors du seeding dans `quiz_routes.py`.

**Solution :** Ajout de la ligne `image=image_url` dans la création des questions.

**Validation :** Rebuild API → vider tables → re-seed → vérifier.

**Prévention Future :**
1. Tests automatisés vérifiant `image != null`
2. Utiliser Object Storage (MinIO/S3) en prod
3. CI/CD qui seed les données de test
4. Health checks vérifiant l'intégrité des données

---

**Date de résolution :** 2025-11-07  
**Version :** Quiz App 1.0  
**Statut :** ✅ Résolu et documenté

