# 🚀 Guide de Déploiement - GreenTech Solutions

Ce guide décrit les différentes méthodes de déploiement de l'application GreenTech Solutions.

## 📋 Pré-requis

### Pour déploiement local
- Python 3.10+
- pip
- Git

### Pour déploiement Docker
- Docker 20.10+
- Docker Compose 2.0+

### Pour déploiement cloud
- Compte sur une plateforme cloud (AWS, Azure, GCP, etc.)
- CLI de la plateforme installé

## 🖥️ Déploiement Local

### 1. Cloner le projet
```bash
git clone <votre-repo>
cd greentech-solutions
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Préparer les données et modèles
```bash
# Créer les dossiers nécessaires
mkdir -p data models logs

# Placer vos données dans data/
# Si vous avez déjà des modèles entraînés, les placer dans models/
```

### 5. Lancer l'application

#### Option A : Utiliser le Makefile
```bash
# Lancer Streamlit uniquement
make run-streamlit

# Lancer l'API uniquement
make run-api

# Lancer les deux en parallèle
make run-both
```

#### Option B : Manuellement
```bash
# Terminal 1 : Streamlit
streamlit run app.py

# Terminal 2 : API FastAPI
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

## 🐳 Déploiement Docker

### 1. Construire les images
```bash
docker-compose build
```

### 2. Lancer les conteneurs
```bash
docker-compose up -d
```

### 3. Vérifier les services
```bash
# Voir les logs
docker-compose logs -f

# Vérifier le statut
docker-compose ps
```

### 4. Accéder aux services
- Streamlit : http://localhost:8501
- API : http://localhost:8000
- Documentation API : http://localhost:8000/docs

### 5. Arrêter les services
```bash
docker-compose down
```

## ☁️ Déploiement Cloud

### Option 1 : Docker Hub + VM

#### 1. Pousser l'image vers Docker Hub
```bash
# Build et tag
docker build -t votre-username/greentech-solutions:latest .

# Login Docker Hub
docker login

# Push
docker push votre-username/greentech-solutions:latest
```

#### 2. Déployer sur une VM
```bash
# Sur la VM
docker pull votre-username/greentech-solutions:latest

# Lancer avec docker-compose
docker-compose up -d
```

### Option 2 : AWS ECS (Elastic Container Service)

#### 1. Créer un repository ECR
```bash
aws ecr create-repository --repository-name greentech-solutions
```

#### 2. Pousser l'image vers ECR
```bash
# Récupérer les credentials
aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.eu-west-1.amazonaws.com

# Tag et push
docker tag greentech-solutions:latest <account-id>.dkr.ecr.eu-west-1.amazonaws.com/greentech-solutions:latest
docker push <account-id>.dkr.ecr.eu-west-1.amazonaws.com/greentech-solutions:latest
```

#### 3. Créer un cluster ECS et déployer

### Option 3 : Azure Container Instances

```bash
# Login Azure
az login

# Créer un groupe de ressources
az group create --name greentech-rg --location westeurope

# Créer un registry
az acr create --resource-group greentech-rg --name greentechregistry --sku Basic

# Push l'image
az acr build --registry greentechregistry --image greentech-solutions:latest .

# Déployer le conteneur
az container create \
  --resource-group greentech-rg \
  --name greentech-app \
  --image greentechregistry.azurecr.io/greentech-solutions:latest \
  --ports 8501 8000 \
  --dns-name-label greentech-app \
  --cpu 2 \
  --memory 4
```

### Option 4 : Google Cloud Run

```bash
# Build et push vers GCR
gcloud builds submit --tag gcr.io/PROJECT-ID/greentech-solutions

# Déployer sur Cloud Run - Streamlit
gcloud run deploy greentech-streamlit \
  --image gcr.io/PROJECT-ID/greentech-solutions \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --port 8501

# Déployer sur Cloud Run - API
gcloud run deploy greentech-api \
  --image gcr.io/PROJECT-ID/greentech-solutions \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --port 8000 \
  --set-env-vars SERVICE_MODE=api
```

## 🔒 Configuration Production

### 1. Variables d'environnement

Créer un fichier `.env` :
```env
# API Configuration
API_BASE_URL=https://votre-api.com
API_KEY=votre-cle-api-secrete

# Database (si applicable)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Sécurité
SECRET_KEY=votre-secret-key-tres-securisee
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com

# Logging
LOG_LEVEL=INFO
```

### 2. Configuration Nginx (reverse proxy)

```nginx
# /etc/nginx/sites-available/greentech

# Streamlit
server {
    listen 80;
    server_name app.votre-domaine.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# API
server {
    listen 80;
    server_name api.votre-domaine.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. Certificats SSL (Let's Encrypt)

```bash
# Installer Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtenir les certificats
sudo certbot --nginx -d app.votre-domaine.com -d api.votre-domaine.com

# Renouvellement automatique
sudo certbot renew --dry-run
```

### 4. Sécurité CORS pour l'API

Modifier `api/main.py` :
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.votre-domaine.com"],  # Domaines autorisés
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### 5. Authentification API (optionnel)

Ajouter une authentification JWT :
```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

security = HTTPBearer()

@app.post("/predict")
async def predict(
    features: DPEFeatures,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # Vérifier le token JWT
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        # Continuer avec la prédiction
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")
```

## 📊 Monitoring et Logs

### 1. Logs centralisés

Utiliser un service comme :
- ELK Stack (Elasticsearch, Logstash, Kibana)
- AWS CloudWatch
- Google Cloud Logging
- Datadog

### 2. Monitoring des performances

```python
# Ajouter dans api/main.py
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

### 3. Health checks

Configurer des health checks réguliers :
```bash
# Avec curl
*/5 * * * * curl -f http://localhost:8000/health || systemctl restart greentech-api

# Avec uptimerobot.com ou pingdom.com
```

## 🔄 CI/CD Pipeline

### Exemple avec GitHub Actions

Créer `.github/workflows/deploy.yml` :
```yaml
name: Deploy GreenTech Solutions

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Build Docker image
      run: docker build -t greentech-solutions .
    
    - name: Push to Docker Hub
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker tag greentech-solutions:latest ${{ secrets.DOCKER_USERNAME }}/greentech-solutions:latest
        docker push ${{ secrets.DOCKER_USERNAME }}/greentech-solutions:latest
    
    - name: Deploy to server
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.SERVER_HOST }}
        username: ${{ secrets.SERVER_USER }}
        key: ${{ secrets.SSH_PRIVATE_KEY }}
        script: |
          cd /app/greentech-solutions
          docker-compose pull
          docker-compose up -d
```

## 🧪 Tests avant déploiement

```bash
# Tests unitaires
pytest tests/

# Tests de l'API
python test_api.py

# Tests de charge (avec locust)
locust -f tests/load_test.py --host http://localhost:8000
```

## 📝 Checklist de déploiement

- [ ] Variables d'environnement configurées
- [ ] Données et modèles en place
- [ ] Certificats SSL configurés
- [ ] CORS correctement configuré
- [ ] Authentification activée (si nécessaire)
- [ ] Logs centralisés configurés
- [ ] Monitoring en place
- [ ] Backups automatiques configurés
- [ ] Health checks actifs
- [ ] Tests passés avec succès

## 🆘 Dépannage

### L'API ne démarre pas
```bash
# Vérifier les logs
docker-compose logs api

# Vérifier que le port n'est pas occupé
lsof -i :8000

# Redémarrer le service
docker-compose restart api
```

### Streamlit ne se connecte pas à l'API
```bash
# Vérifier la connectivité
curl http://localhost:8000/health

# Vérifier les CORS dans les logs API
docker-compose logs api | grep CORS
```

### Les modèles ne se chargent pas
```bash
# Vérifier que les fichiers existent
ls -la models/

# Vérifier les permissions
chmod 644 models/*.pkl

# Réentraîner si nécessaire
curl -X POST http://localhost:8000/models/retrain
```

## 📞 Support

Pour toute question sur le déploiement, contactez l'équipe technique.