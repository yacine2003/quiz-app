# Guide de Déploiement

## Table des matières

- [Docker Deployment](#docker-deployment)
- [Production Checklist](#production-checklist)
- [CI/CD Setup](#cicd-setup)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

## Docker Deployment

### 1. Build des images

```bash
# Build backend
docker build -t quiz-api:latest ./quiz-api

# Build frontend
docker build -t quiz-frontend:latest \
  --build-arg VITE_API_URL=https://api.votre-domaine.com/api \
  ./quiz-ui
```

### 2. Push sur Docker Hub

```bash
# Tag images
docker tag quiz-api:latest <username>/quiz-api:latest
docker tag quiz-frontend:latest <username>/quiz-frontend:latest

# Push
docker push <username>/quiz-api:latest
docker push <username>/quiz-frontend:latest
```

### 3. Déploiement

```bash
# Pull et démarrer
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d

# Vérifier les logs
docker-compose logs -f

# Vérifier la santé
curl http://localhost:3000/health
curl http://localhost:5001/health
```

## Production Checklist

### Backend

- [ ] Passer `FLASK_ENV=production`
- [ ] Utiliser PostgreSQL au lieu de SQLite
- [ ] Configurer secrets sécurisés (JWT_SECRET_KEY)
- [ ] Activer rate limiting
- [ ] Configurer HTTPS (reverse proxy)
- [ ] Activer logs structurés
- [ ] Backup automatique de la DB
- [ ] Monitoring (Sentry, Prometheus)

### Frontend

- [ ] Build optimisé (`npm run build`)
- [ ] Configurer CDN pour assets
- [ ] Activer compression (Gzip/Brotli)
- [ ] Configurer CSP headers
- [ ] Optimiser images (WebP)
- [ ] Cache des assets statiques
- [ ] Monitoring (Sentry, Google Analytics)

### Infrastructure

- [ ] Configurer firewall
- [ ] SSL/TLS certificates (Let's Encrypt)
- [ ] Backup/restore strategy
- [ ] Load balancing (si nécessaire)
- [ ] CDN (Cloudflare, AWS CloudFront)
- [ ] Health checks
- [ ] Auto-scaling (si nécessaire)

## CI/CD Setup

### GitHub Secrets requis

```
DOCKERHUB_USERNAME  # Votre username Docker Hub
DOCKERHUB_TOKEN     # Token d'accès Docker Hub
VITE_API_URL       # URL de l'API en production (optionnel)
```

### Workflow GitHub Actions

Le fichier `.github/workflows/ci-cd.yml` gère :

1. **Tests** : Lint + Type check + Tests unitaires
2. **Build** : Construction des images Docker
3. **Push** : Publication sur Docker Hub
4. **Deploy** : Déploiement automatique (optionnel)

### Activer CI/CD

```bash
# 1. Créer secrets GitHub
# Repository > Settings > Secrets > New repository secret

# 2. Push sur main
git add .
git commit -m "Setup CI/CD"
git push origin main

# 3. Vérifier Actions
# Repository > Actions
```

## Monitoring

### Health Checks

```bash
# Frontend
curl http://localhost:3000/health
# Expected: 200 OK

# Backend
curl http://localhost:5001/health
# Expected: {"status":"healthy"}
```

### Logs

```bash
# Voir tous les logs
docker-compose logs -f

# Logs backend uniquement
docker-compose logs -f api

# Logs frontend uniquement
docker-compose logs -f frontend

# Dernières 100 lignes
docker-compose logs --tail=100
```

### Métriques

Endpoints de monitoring à implémenter :

- `/metrics` - Prometheus metrics
- `/api/stats` - Statistiques applicatives

## Troubleshooting

### Backend ne démarre pas

```bash
# Vérifier les logs
docker-compose logs api

# Vérifier la base de données
docker exec -it quiz-api ls -la /app/data

# Recreer la DB
docker-compose down -v
docker-compose up --build
```

### Frontend ne charge pas l'API

```bash
# Vérifier la config VITE_API_URL
docker exec -it quiz-frontend cat /usr/share/nginx/html/assets/*.js | grep -o 'http[s]*://[^"]*'

# Rebuild avec bon VITE_API_URL
docker build --build-arg VITE_API_URL=http://localhost:5001/api -t quiz-frontend ./quiz-ui
```

### CORS Errors

Vérifier `CORS_ORIGINS` dans le backend :

```python
# quiz-api/config.py
CORS_ORIGINS = "http://localhost:3000,https://votre-domaine.com"
```

### Performance lente

```bash
# Vérifier ressources Docker
docker stats

# Limiter ressources si nécessaire (docker-compose.yml)
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
```

### Base de données corrompue

```bash
# Backup
docker cp quiz-api:/app/data/quiz.db ./backup-quiz.db

# Reset
docker-compose down -v
docker-compose up --build

# Restore
docker cp ./backup-quiz.db quiz-api:/app/data/quiz.db
docker-compose restart api
```

## Scaling

### Horizontal Scaling (plusieurs instances)

Nécessite :
1. Base de données externe (PostgreSQL)
2. Sessions partagées (Redis)
3. Load balancer (Nginx, HAProxy)

```yaml
# docker-compose.scale.yml
services:
  api:
    image: quiz-api:latest
    deploy:
      replicas: 3
  
  nginx-lb:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx-lb.conf:/etc/nginx/nginx.conf
```

### Vertical Scaling (plus de ressources)

```yaml
# docker-compose.prod.yml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

## Sécurité

### Secrets Management

Utiliser Docker secrets ou variables d'environnement chiffrées.

```bash
# Créer secret
echo "super-secret-key" | docker secret create jwt_secret -

# Utiliser dans compose
services:
  api:
    secrets:
      - jwt_secret
```

### SSL/TLS

Configurer un reverse proxy (Nginx, Traefik) avec Let's Encrypt.

```nginx
server {
    listen 443 ssl http2;
    server_name votre-domaine.com;
    
    ssl_certificate /etc/letsencrypt/live/votre-domaine.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/votre-domaine.com/privkey.pem;
    
    location / {
        proxy_pass http://frontend:80;
    }
    
    location /api {
        proxy_pass http://api:5001;
    }
}
```

## Support

Pour toute question : [ouvrir une issue](https://github.com/votre-repo/issues)

