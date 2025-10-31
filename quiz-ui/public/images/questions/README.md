# Images des questions

## 📍 Emplacement
Mettez toutes vos images dans ce dossier : `/quiz-ui/public/images/questions/`

## 📝 Convention de nommage

Vos images sont nommées : `q1base`, `q2base`, ... `q15base`

Ces images correspondent aux questions avec les IDs :
- `q1base` → question `bases-1`
- `q2base` → question `bases-2`
- ...
- `q15base` → question `bases-15`

## 🎯 Actions à faire

1. **Copiez vos images** dans ce dossier avec leurs extensions :
   ```
   q1base.jpg (ou .png, .webp selon le format)
   q2base.jpg
   ...
   q15base.jpg
   ```

2. **Dans la base de données ou questions.json**, vous pouvez référencer les images de deux façons :
   
   **Option A : Utiliser directement vos noms actuels**
   - Ajouter dans chaque question : `"image": "/images/questions/q1base.jpg"`
   
   **Option B : Renommer les fichiers pour correspondre aux IDs**
   - Renommer `q1base.jpg` → `bases-1.jpg`
   - Puis utiliser : `"image": "/images/questions/bases-1.jpg"`

## ✅ Formats acceptés
- `.jpg` / `.jpeg`
- `.png`
- `.webp`
- `.svg`

## 💡 Note
Les images dans `/public/` sont copiées directement dans le build et accessibles via `/images/questions/nom-image.ext`

