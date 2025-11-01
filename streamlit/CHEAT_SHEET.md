# 📝 Cheat Sheet - GreenTech Solutions

Commandes et astuces essentielles pour GreenTech Solutions

---

## 🚀 Démarrage Rapide

```bash
# Vérifier l'installation
python setup_checker.py

# Installer les dépendances
pip install -r requirements.txt

# Lancer Streamlit
streamlit run app.py

# Lancer l'API
uvicorn api.main:app --reload

# Lancer les deux (avec Makefile)
make run-both
```

---

## 🐳 Commandes Docker

```bash
# Construire les images
docker-compose build

# Démarrer les services
docker-compose up -d

# Arrêter les services
docker-compose down

# Voir les logs
docker-compose logs -f

# Voir les logs d'un service spécifique
docker-compose logs -f streamlit
docker-compose logs -f api

# Redémarrer un service
docker-compose restart api

# Voir l'état des services
docker-compose ps

# Entrer dans un conteneur
docker-compose exec streamlit bash
docker-compose exec api bash

# Reconstruire et redémarrer
docker-compose up -d --build

# Nettoyer tout
docker-compose down -v
```

---

## 🔌 API - Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Prédiction individuelle
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "conso_auxiliaires_ef": 500.0,
    "cout_eclairage": 80.0,
    "conso_5_usages_par_m2_ef": 200.0,
    "conso_5_usages_ef": 20000.0,
    "surface_habitable_logement": 100.0,
    "cout_ecs": 300.0,
    "type_batiment": "maison",
    "conso_ecs_ef": 2000.0,
    "conso_refroidissement_ef": 0.0,
    "type_energie_recodee": "Electricite"
  }'
```

### Métriques des modèles
```bash
curl http://localhost:8000/models/metrics
```

### Info sur les modèles
```bash
curl http://localhost:8000/models/info
```

### Rafraîchir les données
```bash
# Mode incrémental
curl -X POST http://localhost:8000/data/refresh

# Mode complet
curl -X POST "http://localhost:8000/data/refresh?full_reload=true"
```

### Réentraîner les modèles
```bash
curl -X POST http://localhost:8000/models/retrain
```

---

## 🧪 Tests

```bash
# Tester l'API
python test_api.py

# Vérifier l'installation
python setup_checker.py

# Tests avec pytest (si configuré)
pytest tests/

# Tests de charge avec locust (si configuré)
locust -f tests/load_test.py --host http://localhost:8000
```

---

## 📊 Données

```bash
# Vérifier les données
ls -lh data/

# Taille du fichier de données
du -h data/donnees_ademe_finales_nettoyees_69_final_pret.csv

# Compter les lignes
wc -l data/donnees_ademe_finales_nettoyees_69_final_pret.csv

# Voir les métadonnées
cat data/metadata.json | python -m json.tool

# Backup des données
cp data/donnees_ademe_finales_nettoyees_69_final_pret.csv \
   data/backup_$(date +%Y%m%d_%H%M%S).csv
```

---

## 🤖 Modèles ML

```bash
# Vérifier les modèles
ls -lh models/

# Taille des modèles
du -h models/*.pkl

# Voir les métriques
cat models/metrics.json | python -m json.tool

# Backup des modèles
cp models/classification_model.pkl \
   models/classification_model_$(date +%Y%m%d).pkl
```

---

## 🔍 Debugging

```bash
# Logs détaillés de l'API
uvicorn api.main:app --reload --log-level debug

# Logs de Streamlit
streamlit run app.py --logger.level debug

# Vérifier les ports utilisés
lsof -i :8501  # Streamlit
lsof -i :8000  # API

# Tuer un processus sur un port
lsof -ti:8501 | xargs kill -9

# Vérifier les imports Python
python -c "from pages import refresh_data, retrain_models; print('OK')"

# Vérifier les dépendances
pip list | grep streamlit
pip list | grep fastapi
```

---

## 📦 Python - Environnement Virtuel

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer (Linux/Mac)
source venv/bin/activate

# Activer (Windows)
venv\Scripts\activate

# Désactiver
deactivate

# Installer les dépendances
pip install -r requirements.txt

# Geler les dépendances
pip freeze > requirements.txt

# Mettre à jour pip
pip install --upgrade pip
```

---

## 🗂️ Structure des Fichiers

```bash
# Voir l'arbre des fichiers
tree -L 2

# Voir uniquement les fichiers Python
find . -name "*.py" -type f

# Compter les lignes de code
find . -name "*.py" -type f -exec wc -l {} + | tail -1

# Rechercher dans le code
grep -r "DataRefresher" --include="*.py"

# Voir les fichiers modifiés récemment
ls -lt | head -20
```

---

## 🧹 Nettoyage

```bash
# Nettoyer les fichiers Python
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete

# Avec le Makefile
make clean

# Nettoyer Docker
docker system prune -a
docker volume prune
```

---

## 🔒 Sécurité

```bash
# Générer une clé secrète
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Vérifier les vulnérabilités
pip audit

# Mettre à jour les dépendances
pip install --upgrade -r requirements.txt
```

---

## 📊 Monitoring

```bash
# Voir l'utilisation CPU/RAM
docker stats

# Voir les logs en temps réel
tail -f logs/app.log

# Voir les dernières erreurs
grep ERROR logs/app.log | tail -20

# Espace disque
df -h

# Utilisation des dossiers
du -sh data/ models/ logs/
```

---

## 🌐 URLs Importantes

```bash
# Application
http://localhost:8501                 # Streamlit

# API
http://localhost:8000                 # API
http://localhost:8000/docs            # Documentation Swagger
http://localhost:8000/redoc           # Documentation ReDoc
http://localhost:8000/health          # Health Check
http://localhost:8000/openapi.json    # Schéma OpenAPI
```

---

## 🔄 Git

```bash
# Statut
git status

# Ajouter tous les fichiers
git add .

# Commit
git commit -m "Ajout fonctionnalités ML"

# Push
git push origin main

# Voir les modifications
git diff

# Créer une branche
git checkout -b feature/nouvelle-fonctionnalite

# Voir l'historique
git log --oneline --graph
```

---

## 📝 Variables d'Environnement

```bash
# Définir une variable
export API_BASE_URL=http://localhost:8000

# Voir toutes les variables
env | grep GREENTECH

# Charger depuis .env
export $(cat .env | xargs)

# Avec Docker
docker-compose up -d --env-file .env.production
```

---

## 🎨 Streamlit

```bash
# Lancer avec config personnalisée
streamlit run app.py --server.port 8502

# Désactiver le cache
streamlit run app.py --server.enableCORS false

# Mode headless (sans navigateur)
streamlit run app.py --server.headless true

# Nettoyer le cache Streamlit
streamlit cache clear
```

---

## 🚑 Dépannage Rapide

### Problème : Module introuvable
```bash
pip install -r requirements.txt
python setup_checker.py
```

### Problème : Port occupé
```bash
lsof -ti:8501 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

### Problème : Modèles non chargés
```bash
# Via interface Streamlit : page "Réentraîner modèles"
# Ou via API :
curl -X POST http://localhost:8000/models/retrain
```

### Problème : Données manquantes
```bash
# Vérifier les données
ls -lh data/
# Via interface : page "Rafraîchir données"
```

### Problème : Docker ne démarre pas
```bash
docker-compose down
docker-compose up -d --build
docker-compose logs -f
```

---

## 💡 Astuces

```bash
# Lancer en arrière-plan
nohup streamlit run app.py &
nohup uvicorn api.main:app &

# Voir les processus en cours
ps aux | grep streamlit
ps aux | grep uvicorn

# Créer un alias (ajouter à ~/.bashrc ou ~/.zshrc)
alias gt-start="make run-both"
alias gt-stop="lsof -ti:8501 | xargs kill -9; lsof -ti:8000 | xargs kill -9"
alias gt-logs="tail -f logs/app.log"

# Surveillance continue
watch -n 5 'curl -s http://localhost:8000/health | python -m json.tool'
```

---

## 📚 Documentation

```bash
# Voir l'aide Streamlit
streamlit --help

# Voir l'aide Uvicorn
uvicorn --help

# Voir l'aide Docker Compose
docker-compose --help

# Voir l'aide Makefile
make help
```

---

## 🎯 Workflow Typique

```bash
# 1. Démarrer la journée
cd greentech-solutions
source venv/bin/activate
git pull
docker-compose up -d

# 2. Développement
streamlit run app.py
# Faire des modifications...

# 3. Tester
python test_api.py
python setup_checker.py

# 4. Commit
git add .
git commit -m "Description des changements"
git push

# 5. Fin de journée
docker-compose down
deactivate
```

---

**Note** : Remplacez `localhost` par votre domaine en production !