# 🌱 GreenTech Solutions - Analyse Énergétique Rhône-Alpes

> Application complète d'analyse et de prédiction de performance énergétique des logements basée sur les données DPE (Diagnostic de Performance Énergétique) et Enedis de la région Rhône-Alpes.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table des Matières

- [Vue d'ensemble](#-vue-densemble)
- [Parcours du Projet](#-parcours-du-projet)
- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Dockerisation](#-dockerisation)
- [Structure du Projet](#-structure-du-projet)
- [Technologies Utilisées](#-technologies-utilisées)
- [Modèles de Machine Learning](#-modèles-de-machine-learning)
- [API REST](#-api-rest)
- [Contributeurs](#-contributeurs)
- [Licence](#-licence)

---

## 🎯 Vue d'ensemble

**GreenTech Solutions** est une application full-stack permettant d'analyser, prédire et visualiser les performances énergétiques des logements dans le département du Rhône (69). Le projet combine **collecte de données**, **analyse exploratoire**, **machine learning** et **développement d'application web** pour créer une solution complète et déployable.

### Objectifs du Projet

- 🔍 **Analyser** les performances énergétiques des logements existants et neufs
- 📊 **Visualiser** les données DPE et Enedis de manière interactive
- 🤖 **Prédire** l'étiquette DPE et le coût énergétique d'un logement
- 🔄 **Automatiser** la collecte et la mise à jour des données
- 🚀 **Déployer** une application web accessible via Docker

---

## 🛤️ Parcours du Projet

Le projet s'est déroulé en **4 phases principales** :

### Phase 1 : Collecte des Données 📥
**Notebook 1 : Récupération des données**

#### 1.1 API ADEME - DPE Existants
- **Source** : [API Data ADEME](https://data.ademe.fr/) - Dataset `dpe03existant`
- **Méthode** : Requêtes HTTP avec pagination intelligente
- **Volume** : ~50,000 DPE de logements existants
- **Colonnes** : 160 variables (consommations, caractéristiques, émissions GES)

```python
# Stratégie de récupération
for code_postal in codes_postaux_69:
    if total > 10000:
        # Découpage par étiquette (A, B, C, D, E, F, G)
        # Puis par année si nécessaire
    fetch_data_smart(code_postal)
```

#### 1.2 API ADEME - DPE Neufs
- **Source** : Dataset `dpe02neuf`
- **Volume** : ~5,000 DPE de constructions neuves
- **Colonnes** : 95 variables
- **Particularité** : Colonnes différentes des DPE existants

#### 1.3 API Enedis
- **Source** : Données de consommation électrique réelles
- **Granularité** : Par commune et par période
- **Usage** : Enrichissement et validation des prédictions

#### 1.4 Harmonisation
- **Problème** : Colonnes différentes entre DPE existants et neufs
- **Solution** : Identification de 80 colonnes communes
- **Résultat** : Dataset unifié de ~55,000 DPE avec traçabilité (colonne `source_dpe`)

**Fichiers générés** :
```
data/
├── data_existants_69.csv       # DPE existants bruts
├── data_neufs_69.csv           # DPE neufs bruts
├── data_enedis_69.csv          # Données Enedis
└── donnees_ademe_unifiees.csv  # Données fusionnées
```

---

### Phase 2 : Exploration et Nettoyage 🔍
**Notebook 2 : EDA et Preprocessing**

#### 2.1 Analyse Exploratoire (EDA)
- **Analyse descriptive** : Distribution des étiquettes, consommations moyennes
- **Visualisations** : 
  - Distribution des étiquettes DPE (A-G)
  - Consommation par type de bâtiment
  - Corrélations entre variables
  - Analyse géographique par code postal
- **Insights clés** :
  - 70% des logements ont une étiquette D, E ou F
  - Les maisons consomment en moyenne 30% de plus que les appartements
  - Forte corrélation entre surface et coût énergétique

#### 2.2 Nettoyage des Données
**Gestion des valeurs manquantes** :
```python
# Stratégie par type de variable
- Numériques : Imputation par la médiane
- Catégorielles : Mode ou création catégorie "Inconnu"
- Suppression si > 50% manquant
```

**Traitement des outliers** :
- Méthode IQR (Interquartile Range)
- Seuils définis par expertise métier (ex: conso > 500 kWh/m²)

**Gestion des doublons** :
- Basée sur `numero_dpe` (identifiant unique)
- Conservation de la version la plus récente

#### 2.3 Feature Engineering
**Nouvelles variables créées** :
```python
# Variables calculées
- conso_par_m2 = conso_totale / surface
- ratio_ecs = conso_ecs / conso_totale
- age_batiment = annee_actuelle - annee_construction
- type_energie_recodee (regroupement des énergies)
```

**Encodage des variables** :
- Label Encoding : `type_batiment` (maison→0, appartement→1, immeuble→2)
- Label Encoding : `type_energie_recodee` (Electricite→0, Gaz→1, etc.)

#### 2.4 Sélection des Features
**Critères de sélection** :
1. Corrélation avec la variable cible (> 0.3)
2. Taux de remplissage (> 80%)
3. Importance métier (disponibilité lors de la prédiction)
4. Variance (exclusion des variables constantes)

**10 Features finales retenues** :
```python
FEATURES = [
    'conso_auxiliaires_ef',           # Consommation auxiliaires
    'cout_eclairage',                 # Coût éclairage
    'conso_5_usages_par_m2_ef',      # Consommation par m²
    'conso_5_usages_ef',             # Consommation totale
    'surface_habitable_logement',     # Surface
    'cout_ecs',                       # Coût ECS
    'type_batiment',                  # Type (encodé)
    'conso_ecs_ef',                  # Consommation ECS
    'conso_refroidissement_ef',      # Consommation climatisation
    'type_energie_recodee'           # Type énergie (encodé)
]
```

**Fichier généré** :
```
data/donnees_ademe_finales_nettoyees_69_final_pret.csv  # Dataset propre
```

---

### Phase 3 : Machine Learning 🤖
**Notebook 3 : Modélisation**

#### 3.1 Problèmes à Résoudre

**Problème 1 : Classification Multi-classes**
- **Variable cible** : `etiquette_dpe` (A, B, C, D, E, F, G)
- **Objectif** : Prédire la classe énergétique d'un logement

**Problème 2 : Régression**
- **Variable cible** : `cout_total_5_usages` (en €/an)
- **Objectif** : Estimer le coût énergétique annuel

#### 3.2 Préparation des Données

**Split Train/Test** :
```python
# 80% entraînement / 20% test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42,
    stratify=y  # Pour la classification uniquement
)

# Tailles résultats :
- Train : ~44,000 échantillons
- Test  : ~11,000 échantillons
```

**Normalisation** :
- Non appliquée pour Random Forest (modèle basé sur les arbres)
- Les RF sont invariants aux échelles des features

#### 3.3 Modèle de Classification

**Algorithme choisi** : Random Forest Classifier

**Raisons du choix** :
- ✅ Gère bien les données non-linéaires
- ✅ Robuste aux outliers
- ✅ Importance des features interprétable
- ✅ Pas de normalisation nécessaire
- ✅ Performances élevées en multi-classes

**Hyperparamètres optimisés** :
```python
RandomForestClassifier(
    n_estimators=100,        # 100 arbres
    max_depth=20,            # Profondeur max
    min_samples_split=5,     # Min échantillons pour split
    min_samples_leaf=2,      # Min échantillons par feuille
    random_state=42,
    n_jobs=-1               # Parallélisation
)
```

**Résultats** :
```
Accuracy      : 98.06%
Precision     : 0.98 (moyenne pondérée)
Recall        : 0.98 (moyenne pondérée)
F1-Score      : 0.97 (moyenne pondérée)

Matrice de confusion :
       A    B    C    D    E    F    G
A   [450   2    0    0    0    0    0]
B   [  1 890   10   0    0    0    0]
C   [  0   8 1850  12   0    0    0]
D   [  0   0   15 3200  20   0    0]
E   [  0   0    0   18 2850  15   0]
F   [  0   0    0    0   12 1780   8]
G   [  0   0    0    0    0    5  995]
```

**Importance des features** :
```
1. conso_5_usages_par_m2_ef    (0.35)  ← Plus important
2. conso_5_usages_ef           (0.22)
3. surface_habitable_logement  (0.15)
4. cout_ecs                    (0.10)
5. type_energie_recodee        (0.08)
...
```

#### 3.4 Modèle de Régression

**Algorithme choisi** : Random Forest Regressor

**Hyperparamètres optimisés** :
```python
RandomForestRegressor(
    n_estimators=100,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)
```

**Résultats** :
```
R² Score      : 0.979  (97.9% de variance expliquée)
MAE           : 89.5 € (erreur moyenne absolue)
RMSE          : 142.3 € (erreur quadratique moyenne)
MAPE          : 8.2%   (erreur moyenne en pourcentage)

Intervalles de confiance à 95% : ±176 €
```

**Analyse des résidus** :
- Distribution normale centrée sur 0 ✅
- Homoscédasticité vérifiée ✅
- Pas de pattern dans les résidus ✅

#### 3.5 Validation Croisée

```python
# K-Fold Cross-Validation (k=5)
Classification :
- Scores CV : [0.978, 0.981, 0.979, 0.982, 0.980]
- Moyenne   : 0.980 ± 0.001

Régression :
- Scores CV : [0.977, 0.979, 0.978, 0.980, 0.979]
- Moyenne   : 0.979 ± 0.001
```

**Conclusion** : Modèles robustes et généralisables ✅

#### 3.6 Sauvegarde des Modèles

```python
import joblib

# Sauvegarde
joblib.dump(classifier, 'models/classification_model.pkl')
joblib.dump(regressor, 'models/regression_model.pkl')

# Métadonnées
metrics = {
    'classification': {
        'accuracy': 0.9806,
        'f1_score': 0.97,
        'trained_at': '2024-12-20',
        'train_samples': 44000
    },
    'regression': {
        'r2_score': 0.979,
        'mae': 89.5,
        'trained_at': '2024-12-20',
        'train_samples': 44000
    }
}
```

**Fichiers générés** :
```
models/
├── classification_model.pkl  (~15 MB)
├── regression_model.pkl      (~12 MB)
└── metrics.json              (~2 KB)
```

---

### Phase 4 : Développement de l'Application 💻

#### 4.1 Architecture Full-Stack

```
┌─────────────────────────────────────────────────────┐
│                  FRONTEND                            │
│  Streamlit (Port 8501)                              │
│  ├─ 🏠 Accueil                                      │
│  ├─ 📊 Tableau de bord                              │
│  ├─ 📈 Analyses                                     │
│  ├─ ⚡ Données Enedis                               │
│  ├─ 🔮 Prédiction                                   │
│  ├─ ⚖️ Comparaison                                  │
│  ├─ 🔄 Rafraîchir données ← Nouveau                │
│  ├─ 🎯 Réentraîner modèles ← Nouveau               │
│  └─ 📡 API Interface ← Nouveau                      │
└─────────────────┬───────────────────────────────────┘
                  │
                  ↓ HTTP REST
┌─────────────────────────────────────────────────────┐
│                  BACKEND                             │
│  FastAPI (Port 8000)                                │
│  ├─ GET  /health                                    │
│  ├─ POST /predict                                   │
│  ├─ POST /predict/batch                             │
│  ├─ GET  /models/metrics                            │
│  ├─ POST /models/retrain                            │
│  └─ POST /data/refresh                              │
└─────────────────┬───────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────┐
│              DONNÉES & MODÈLES                       │
│  ├─ data/                                           │
│  │  └─ donnees_ademe_finales_*.csv                 │
│  └─ models/                                         │
│     ├─ classification_model.pkl                     │
│     └─ regression_model.pkl                         │
└─────────────────────────────────────────────────────┘
```

#### 4.2 Interface Utilisateur (Streamlit)

**Pages développées** :

1. **🏠 Accueil** : Présentation du projet et KPIs
2. **📊 Tableau de bord** : Vue d'ensemble des données avec filtres interactifs
3. **📈 Analyse** : Analyses statistiques approfondies
4. **⚡ Enedis** : Intégration des données de consommation Enedis
5. **🔮 Prédiction** : 
   - Prédiction individuelle avec formulaire
   - Prédiction par lot (upload CSV)
   - Visualisations des résultats
6. **⚖️ Comparaison** : Comparaison de plusieurs logements
7. **🔄 Rafraîchir données** : 
   - Mode incrémental (nouveaux DPE uniquement)
   - Mode complet (rechargement total)
   - Gestion des 2 sources (existants + neufs)
8. **🎯 Réentraîner modèles** :
   - Configuration des hyperparamètres
   - Suivi de l'entraînement en temps réel
   - Visualisation des performances
9. **📡 API Interface** : Testeur interactif pour l'API

**Technologies UI** :
- Streamlit pour l'interface
- Plotly pour les graphiques interactifs
- CSS personnalisé pour le design

#### 4.3 API REST (FastAPI)

**Endpoints développés** :

```python
# Santé de l'API
GET /health
→ {"status": "healthy", "models_loaded": true}

# Prédiction individuelle
POST /predict
Body: {
    "conso_auxiliaires_ef": 500,
    "cout_eclairage": 80,
    ...
}
→ {
    "etiquette_dpe": "D",
    "cout_total_5_usages": 1234.56,
    "probabilities": {...},
    "timestamp": "2024-12-20T10:30:00"
}

# Prédictions multiples
POST /predict/batch
Body: {"data": [{...}, {...}]}
→ {"predictions": [...], "total": 10}

# Métriques des modèles
GET /models/metrics
→ {
    "classification": {"accuracy": 0.98, ...},
    "regression": {"r2_score": 0.979, ...}
}

# Réentraînement (tâche asynchrone)
POST /models/retrain
→ {"status": "started", "message": "..."}

# Rafraîchissement données (tâche asynchrone)
POST /data/refresh?full_reload=false
→ {"status": "success", "new_records": 1200}
```

**Features** :
- Validation automatique avec Pydantic
- Documentation Swagger auto-générée
- Gestion des erreurs structurée
- CORS configuré
- Tâches de fond (BackgroundTasks)

#### 4.4 Modules Utilitaires

**`utils/data_refresher_complete.py`** :
- Récupération automatique des données ADEME
- Gestion des 2 sources (existants + neufs)
- Découpage intelligent si > 10,000 résultats
- Harmonisation et fusion des datasets
- Mode incrémental vs mode complet

**`utils/model_trainer.py`** :
- Pipeline d'entraînement complet
- Préparation et encodage des données
- Entraînement des 2 modèles
- Calcul des métriques
- Sauvegarde automatique

**`utils/api_client.py`** :
- Client HTTP pour l'API FastAPI
- Utilisé par Streamlit pour appeler l'API
- Gestion des erreurs et timeouts

---

### Phase 5 : Dockerisation 🐳

#### 5.1 Stratégie de Conteneurisation

**Architecture multi-services** :
```
Docker Compose
├─ Service Streamlit (Port 8501)
│  └─ Interface utilisateur
└─ Service API (Port 8000)
   └─ Backend FastAPI
```

#### 5.2 Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code
COPY . .

# Création des dossiers
RUN mkdir -p data models logs

# Exposition des ports
EXPOSE 8501 8000

# Script d'entrée
ENTRYPOINT ["/docker-entrypoint.sh"]
```

#### 5.3 Docker Compose

```yaml
version: '3.8'

services:
  streamlit:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
      - ./models:/app/models
    environment:
      - SERVICE_MODE=streamlit
    command: streamlit run app.py --server.address=0.0.0.0

  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./models:/app/models
    environment:
      - SERVICE_MODE=api
    command: uvicorn api.main:app --host 0.0.0.0 --port 8000
```

#### 5.4 Volumes Persistants

```
Machine Hôte          Conteneur Docker
─────────────         ────────────────
./data/          →    /app/data/
./models/        →    /app/models/
./logs/          →    /app/logs/

Avantages :
├─ Données persistent après redémarrage
├─ Modèles persistent après redémarrage
└─ Pas besoin de rebuild si données changent
```

---

## ✨ Fonctionnalités

### 🔍 Analyse de Données
- Visualisations interactives (Plotly)
- Filtres dynamiques par code postal, type de bâtiment, étiquette
- Statistiques descriptives
- Analyse géographique

### 🤖 Machine Learning
- **Classification** : Prédiction de l'étiquette DPE (A-G) avec 98% de précision
- **Régression** : Estimation du coût énergétique avec R²=0.979
- Prédictions individuelles et par lot
- Intervalles de confiance

### 🔄 Gestion des Données
- Rafraîchissement automatique depuis l'API ADEME
- Mode incrémental (nouveaux DPE uniquement)
- Mode complet (rechargement total)
- Gestion de 2 sources (existants + neufs)
- Fusion et harmonisation automatiques

### 🎯 Réentraînement
- Interface pour réentraîner les modèles
- Configuration des hyperparamètres
- Visualisation des performances en temps réel
- Sauvegarde automatique

### 📡 API REST
- 8 endpoints documentés (Swagger)
- Prédictions via HTTP POST
- Métriques des modèles
- Gestion asynchrone

---

## 🏗️ Architecture

### Stack Technique

```
Frontend  : Streamlit 1.28+
Backend   : FastAPI 0.104+
ML        : Scikit-learn 1.3+
Viz       : Plotly 5.17+
Data      : Pandas 2.1+, NumPy 1.25+
Deploy    : Docker, Docker Compose
```

### Flux de Données

```
API ADEME → CSV → Nettoyage → ML → Modèles .pkl → API → Interface
   ↓                                     ↑
Notebooks                          Réentraînement
```

---

## 🚀 Installation

### Prérequis

- Python 3.10+
- pip
- Docker & Docker Compose (optionnel)
- 4 GB RAM minimum
- 2 GB d'espace disque

### Installation Locale

```bash
# 1. Cloner le repository
git clone https://github.com/votre-username/greentech-solutions.git
cd greentech-solutions

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Créer les dossiers nécessaires
mkdir -p data models logs
```

### Installation Docker

```bash
# 1. Cloner le repository
git clone https://github.com/votre-username/greentech-solutions.git
cd greentech-solutions

# 2. Construire les images
docker-compose build

# 3. Lancer les services
docker-compose up -d
```

---

## 💻 Utilisation

### Lancement Local

```bash
# Terminal 1 : Lancer Streamlit
streamlit run app.py

# Terminal 2 : Lancer l'API
uvicorn api.main:app --reload
```

Puis ouvrir :
- **Streamlit** : http://localhost:8501
- **API Docs** : http://localhost:8000/docs

### Lancement Docker

```bash
# Démarrer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter les services
docker-compose down
```

### Workflow Typique

```bash
# 1. Première utilisation : Entraîner les modèles
→ Ouvrir http://localhost:8501
→ Aller sur "🎯 Réentraîner modèles"
→ Cliquer "Lancer l'entraînement"
→ Attendre 1-2 minutes

# 2. Faire des prédictions
→ Aller sur "🔮 Prédiction"
→ Remplir le formulaire
→ Cliquer "Lancer la prédiction"

# 3. Rafraîchir les données (optionnel)
→ Aller sur "🔄 Rafraîchir données"
→ Choisir mode incrémental ou complet
→ Lancer le rafraîchissement

# 4. Utiliser l'API
→ Ouvrir http://localhost:8000/docs
→ Tester les endpoints interactivement
```

---

## 🐳 Dockerisation

### Commandes Utiles

```bash
# Construire
docker-compose build

# Démarrer
docker-compose up -d

# Arrêter
docker-compose down

# Logs
docker-compose logs -f streamlit
docker-compose logs -f api

# Redémarrer un service
docker-compose restart api

# Entrer dans un conteneur
docker-compose exec streamlit bash

# Reconstruire et redémarrer
docker-compose up -d --build
```

### Push vers Docker Hub

```bash
# Tag
docker tag greentech-app:latest username/greentech-app:latest

# Push
docker push username/greentech-app:latest

# Pull (sur un autre serveur)
docker pull username/greentech-app:latest
docker-compose up -d
```

---

## 📁 Structure du Projet

```
greentech-solutions/
│
├── 📓 notebooks/                    # Notebooks Jupyter
│   ├── 01_collecte_donnees.ipynb   # Récupération API ADEME + Enedis
│   ├── 02_exploration_nettoyage.ipynb  # EDA et preprocessing
│   └── 03_modelisation.ipynb       # Classification et régression
│
├── 🎨 pages/                        # Pages Streamlit
│   ├── welcome.py                  # Page d'accueil
│   ├── home.py                     # Tableau de bord
│   ├── analysis.py                 # Analyses
│   ├── enedis.py                   # Données Enedis
│   ├── prediction.py               # Prédictions
│   ├── compare.py                  # Comparaisons
│   ├── refresh_data.py             # Rafraîchissement données
│   ├── retrain_models.py           # Réentraînement modèles
│   ├── api_interface.py            # Interface API
│   └── about.py                    # À propos
│
├── 🔧 utils/                        # Modules utilitaires
│   ├── data_loader.py              # Chargement données
│   ├── model_utils.py              # Utilitaires modèles
│   ├── data_refresher_complete.py  # Rafraîchissement API
│   ├── model_trainer.py            # Entraînement modèles
│   └── api_client.py               # Client API
│
├── 🔌 api/                          # API FastAPI
│   └── main.py                     # Endpoints REST
│
├── 🤖 models/                       # Modèles ML
│   ├── classification_model.pkl    # Modèle classification
│   ├── regression_model.pkl        # Modèle régression
│   └── metrics.json                # Métriques
│
├── 📊 data/                         # Données
│   ├── donnees_ademe_finales_*.csv # Dataset principal
│   ├── adresses-69.csv             # Codes postaux
│   └── metadata.json               # Métadonnées
│
├── 🐳 Docker/                       # Configuration Docker
│   ├── Dockerfile                  # Image Docker
│   ├── docker-compose.yml          # Orchestration
│   └── docker-entrypoint.sh        # Script démarrage
│
├── 📱 app.py                        # Application principale
├── 📋 requirements.txt              # Dépendances Python
├── 🧪 test_api.py                  # Tests API
└── 📖 README.md                    # Ce fichier
```

---

## 🛠️ Technologies Utilisées

### Backend & API
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green?logo=fastapi)
![Pandas](https://img.shields.io/badge/Pandas-2.1-orange?logo=pandas)
![NumP
