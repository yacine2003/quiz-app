# 🔍 Debug - Images non visibles

## ✅ État actuel

Les images SONT bien dans la base de données :
- Quiz ID 4 "Quiz Tennis" contient 15 questions avec images
- Les chemins sont corrects : `/images/questions/q1base.png` etc.
- Le backend répond correctement sur http://localhost:5001

## 🚨 Problème identifié

Vous essayez d'accéder à **localhost:3001** mais le frontend doit être sur **localhost:3000**

## 🚀 Solution - Démarrer correctement

### Option 1 : Script automatique
```bash
./start-dev.sh
```

### Option 2 : Manuellement

**Terminal 1 - Backend (Port 5001)**
```bash
cd quiz-api
source ../venv/bin/activate
python app_new.py
```

**Terminal 2 - Frontend (Port 3000)**
```bash
cd quiz-ui
npm run dev
```

## 🌐 URLs correctes

- ✅ **Frontend:** http://localhost:3000
- ✅ **Backend:** http://localhost:5001
- ❌ **Ne pas utiliser:** http://localhost:3001

## 🧪 Test des images

1. Ouvrir http://localhost:3000
2. Sélectionner le quiz **"Quiz Tennis"** (ID 4)
3. Les 15 premières questions doivent afficher leurs images

### Test direct d'une image
- URL: http://localhost:3000/images/questions/q1base.png
- Cette URL doit afficher l'image directement

## 📋 Vérifications

### Backend fonctionne ?
```bash
curl http://localhost:5001/health
# Devrait retourner: {"status":"healthy"}
```

### Images dans la base ?
```bash
curl "http://localhost:5001/api/questions?quiz_id=4" | grep -o '"image":"[^"]*"'
# Devrait retourner: "image":"/images/questions/q1base.png"
```

### Images accessibles ?
```bash
# Dans le dossier quiz-ui
ls -la public/images/questions/q1base.png
# Le fichier doit exister
```

## ⚠️ Problèmes courants

1. **ERR_CONNECTION_REFUSED sur localhost:3001**
   - ➡️ Utiliser localhost:3000 (pas 3001)

2. **Port 5001 occupé**
   - ➡️ Arrêter les processus : `lsof -ti:5001 | xargs kill -9`

3. **Images en 404**
   - ➡️ Vérifier que les images sont dans `quiz-ui/public/images/questions/`
   - ➡️ Vérifier que le frontend tourne sur le port 3000

4. **Quiz sans images**
   - ➡️ Utiliser le quiz ID 4 "Quiz Tennis" (pas les autres quiz)

