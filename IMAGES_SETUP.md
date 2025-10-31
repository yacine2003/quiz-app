# Configuration des images pour les questions

## ✅ Implémentation terminée

Les images sont maintenant intégrées dans le système de quiz et s'affichent automatiquement.

### Structure mise en place

```
quiz-ui/public/images/questions/
  ├── q1base.png  → Question bases-1
  ├── q2base.png  → Question bases-2
  ├── ...
  └── q15base.png → Question bases-15
```

### Fonctionnement

1. **Stockage** : Les images sont dans `quiz-ui/public/images/questions/`
2. **Base de données** : Le champ `image` contient le chemin `/images/questions/qXbase.png`
3. **Affichage** : `QuestionCard.vue` affiche automatiquement les images quand elles sont présentes
4. **Import** : Le script `import_questions.py` lit le champ `image` depuis `questions.json`

### Comment ajouter de nouvelles images

1. Placer l'image dans `quiz-ui/public/images/questions/`
2. Ajouter le champ `"image":"/images/questions/nom-fichier.ext"` dans `data/questions.json`
3. Réimporter les questions :
   ```bash
   cd quiz-api
   source ../venv/bin/activate
   python import_questions.py
   ```

### Formats supportés

- PNG ✅
- JPEG/JPG ✅
- WebP ✅
- SVG ✅
- GIF ✅

### Test

Pour tester que les images s'affichent :

1. Lancer le serveur backend :
   ```bash
   cd quiz-api
   source ../venv/bin/activate
   python app_new.py
   ```

2. Lancer le serveur frontend :
   ```bash
   cd quiz-ui
   npm run dev
   ```

3. Ouvrir http://localhost:3000 et jouer le quiz "bases"
4. Les 15 premières questions doivent afficher leurs images

### Notes techniques

- Les images dans `/public/` sont servies statiquement par Vite/Nginx
- Pas de limite de taille configurée actuellement
- Les images sont cachées 1 an par Nginx en production
- Le champ `image` est optionnel (les questions sans image s'affichent normalement)

## État actuel

✅ 15 images ajoutées pour le quiz "bases" (q1base.png à q15base.png)
✅ Questions importées dans la base de données avec les références d'images
✅ Frontend prêt à afficher les images
✅ Système complètement fonctionnel

