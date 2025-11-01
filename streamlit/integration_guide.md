# 📘 Guide d'Intégration - GreenTech Solutions

Ce guide vous accompagne pas à pas pour intégrer les nouvelles fonctionnalités à votre application existante.

## 📦 Fichiers à ajouter

Voici la liste complète des fichiers que je vous ai fournis :

### 1. Nouveaux modules utilitaires (`utils/`)
- ✅ `utils/data_refresher.py` - Rafraîchissement des données depuis l'API ADEME
- ✅ `utils/model_trainer.py` - Réentraînement des modèles ML
- ✅ `utils/api_client.py` - Client pour interagir avec l'API FastAPI

### 2. Nouvelles pages Streamlit (`pages/`)
- ✅ `pages/refresh_data.py` - Interface de rafraîchissement des données
- ✅ `pages/retrain_models.py` - Interface de réentraînement des modèles
- ✅ `pages/__init__.py` - Fichier d'initialisation des pages

### 3. API FastAPI (`api/`)
- ✅ `api/main.py` - API REST complète avec tous les endpoints

### 4. Configuration Docker
- ✅ `Dockerfile` - Image Docker pour l'application
- ✅ `docker-compose.yml` - Orchestration des services
- ✅ `docker-entrypoint.sh` - Script de démarrage
- ✅ `.dockerignore` - Fichiers à exclure de l'image

### 5. Fichiers de configuration
- ✅ `requirements.txt` - Dépendances Python (mis à jour)
- ✅ `Makefile` - Commandes utiles
- ✅ `app.py` - Application principale (mise à jour)

### 6. Documentation et tests
- ✅ `README.md` - Documentation complète
- ✅ `DEPLOYMENT.md` - Guide de déploiement
- ✅ `test_api.py` - Script de test de l'API

## 🔧 Étapes d'intégration

### Étape 1 : Sauvegarder votre projet actuel

```bash
# Créer une branche de sauvegarde
git checkout -b backup-avant-integration
git add .
git commit -m "Sauvegarde avant intégration nouvelles fonctionnalités"

# Retourner sur main
git checkout main
```

### Étape 2 : Ajouter les nouveaux fichiers

```bash
# Créer la structure si nécessaire
mkdir -p utils api pages

# Copier les nouveaux fichiers dans les bons dossiers
# (Copier chaque fichier fourni dans l'artifact correspondant)
```

### Étape 3 : Mettre à jour `app.py`

Remplacer votre `app.py` actuel par la version mise à jour que je vous ai fournie, ou modifier manuellement :

```python
# Ajouter ces imports en haut
from pages import refresh_data, retrain_models

# Ajouter cette section dans la sidebar
st.markdown("### 🤖 Machine Learning")
ml_page = st.radio(
    "Gestion ML",
    [
        "Aucune",
        "🔄 Rafraîchir données",
        "🎯 Réentraîner modèles"
    ],
    label_visibility="collapsed"
)

# Ajouter cette logique d'affichage
if ml_page != "Aucune":
    if ml_page == "🔄 Rafraîchir données":
        refresh_data.show()
    elif ml_page == "🎯 Réentraîner modèles":
        retrain_models.show()
else:
    # Vos pages existantes...
```

### Étape 4 : Mettre à jour `requirements.txt`

Ajouter les nouvelles dépendances à votre `requirements.txt` existant :

```txt
# API
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.4.2

# Data fetching
requests==2.31.0

# Utilities
python-multipart==0.0.6
```

### Étape 5 : Installer les nouvelles dépendances

```bash
pip install -r requirements.txt
```

### Étape 6 : Vérifier la structure

Votre projet devrait maintenant ressembler à ceci :

```
greentech-solutions/
├── app.py                                    ✅ MODIFIÉ
├── pages/
│   ├── __init__.py                          ✅ NOUVEAU
│   ├── welcome.py                           (existant)
│   ├── home.py                              (existant)
│   ├── analysis.py                          (existant)
│   ├── enedis.py                            (existant)
│   ├── prediction.py                        (existant)
│   ├── compare.py                           (existant)
│   ├── about.py                             (existant)
│   ├── refresh_data.py                      ✅ NOUVEAU
│   └── retrain_models.py                    ✅ NOUVEAU
├── utils/
│   ├── data_loader.py                       (existant)
│   ├── model_utils.py                       (existant)
│   ├── data_refresher.py                    ✅ NOUVEAU
│   ├── model_trainer.py                     ✅ NOUVEAU
│   └── api_client.py                        ✅ NOUVEAU
├── api/
│   └── main.py                              ✅ NOUVEAU
├── models/
│   ├── classification_model.pkl             (existant)
│   ├── regression_model.pkl                 (existant)
│   └── metrics.json                         (sera créé)
├── data/
│   ├── donnees_ademe_finales_nettoyees_69_final_pret.csv  (existant)
│   ├── adresses-69.csv                      (existant)
│   └── metadata.json                        (sera créé)
├── Dockerfile                               ✅ NOUVEAU
├── docker-compose.yml                       ✅ NOUVEAU
├── docker-entrypoint.sh                     ✅ NOUVEAU
├── .dockerignore                            ✅ NOUVEAU
├── Makefile                                 ✅ NOUVEAU
├── requirements.txt                         ✅ MODIFIÉ
├── test_api.py                              ✅ NOUVEAU
├── README.md                                ✅ NOUVEAU
└── DEPLOYMENT.md                            ✅ NOUVEAU
```

### Étape 7 : Tester en local

#### Test 1 : Lancer Streamlit seul
```bash
streamlit run app.py
```

✅ Vérifier que :
- L'application se lance sans erreur
- Les nouvelles pages "🔄 Rafraîchir données" et "🎯 Réentraîner modèles" apparaissent
- Les pages existantes fonctionnent toujours

#### Test 2 : Lancer l'API
```bash
# Dans un nouveau terminal
uvicorn api.main:app --reload
```

✅ Vérifier que :
- L'API démarre sur http://localhost:8000
- La documentation est accessible sur http://localhost:8000/docs
- Le health check répond : http://localhost:8000/health

#### Test 3 : Tester l'API
```bash
python test_api.py
```

✅ Tous les tests devraient passer (si les modèles sont entraînés)

### Étape 8 : Test des nouvelles fonctionnalités

#### A. Rafraîchissement des données

1. Aller dans "🔄 Rafraîchir données"
2. Vérifier l'état actuel des données
3. Lancer un rafraîchissement (mode "Nouveaux DPE uniquement")
4. Vérifier que les nouvelles données sont ajoutées

#### B. Réentraînement des modèles

1. Aller dans "🎯 Réentraîner modèles"
2. Vérifier les métriques actuelles
3. Lancer un réentraînement
4. Vérifier que les nouvelles métriques sont affichées

#### C. Prédictions via l'API

```bash
curl -X POST "http://localhost:8000/predict" \
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

### Étape 9 : Test Docker (optionnel mais recommandé)

```bash
# Construire les images
docker-compose build

# Lancer les services
docker-compose up -d

# Vérifier les logs
docker-compose logs -f

# Tester l'accès
# Streamlit : http://localhost:8501
# API : http://localhost:8000

# Arrêter
docker-compose down
```

## 🐛 Résolution des problèmes courants

### Problème 1 : ImportError dans les pages

**Symptôme** : `ImportError: cannot import name 'refresh_data' from 'pages'`

**Solution** :
```bash
# Vérifier que __init__.py existe dans pages/
touch pages/__init__.py

# Ou ajouter le contenu du fichier __init__.py fourni
```

### Problème 2 : Les modèles ne se chargent pas

**Symptôme** : "Modèles non chargés" dans l'API

**Solution** :
```bash
# Vérifier que les fichiers .pkl existent
ls -la models/

# Si nécessaire, réentraîner via Streamlit
# Ou via l'API :
curl -X POST http://localhost:8000/models/retrain
```

### Problème 3 : Erreur de connexion à l'API depuis Streamlit

**Symptôme** : "API non disponible"

**Solution** :
```bash
# Vérifier que l'API tourne
curl http://localhost:8000/health

# Si non, la lancer :
uvicorn api.main:app --reload
```

### Problème 4 : Dépendances manquantes

**Symptôme** : `ModuleNotFoundError: No module named 'fastapi'`

**Solution** :
```bash
pip install -r requirements.txt
```

### Problème 5 : Port déjà utilisé

**Symptôme** : `OSError: [Errno 48] Address already in use`

**Solution** :
```bash
# Trouver et tuer le processus
lsof -ti:8000 | xargs kill -9  # Pour l'API
lsof -ti:8501 | xargs kill -9  # Pour Streamlit

# Ou utiliser des ports différents
streamlit run app.py --server.port 8502
uvicorn api.main:app --port 8001
```

## ✅ Checklist finale

Avant de considérer l'intégration terminée, vérifiez :

- [ ] Tous les nouveaux fichiers sont en place
- [ ] `app.py` est mis à jour avec les nouvelles pages
- [ ] `requirements.txt` contient toutes les dépendances
- [ ] Streamlit se lance sans erreur
- [ ] L'API se lance sans erreur
- [ ] Les nouvelles pages s'affichent correctement
- [ ] Le rafraîchissement des données fonctionne
- [ ] Le réentraînement des modèles fonctionne
- [ ] Les prédictions via l'API fonctionnent
- [ ] Les tests API passent (`python test_api.py`)
- [ ] Docker fonctionne (optionnel)
- [ ] Documentation à jour

## 📚 Prochaines étapes

Une fois l'intégration terminée :

1. **Commit et push** :
```bash
git add .
git commit -m "Ajout fonctionnalités ML : rafraîchissement données, réentraînement modèles, API FastAPI"
git push origin main
```

2. **Déploiement** : Suivre le guide `DEPLOYMENT.md` pour déployer en production

3. **Formation utilisateurs** : Former les utilisateurs aux nouvelles fonctionnalités

4. **Monitoring** : Mettre en place le monitoring des performances

## 🆘 Support

Si vous rencontrez des problèmes lors de l'intégration :

1. Vérifier les logs : `docker-compose logs` ou logs dans le terminal
2. Vérifier la documentation : `README.md` et `DEPLOYMENT.md`
3. Tester les endpoints API : http://localhost:8000/docs
4. Consulter les exemples de test : `test_api.py`

Bonne intégration ! 🚀