# 💡 GreenTech Solutions

> _Modélisation et visualisation des performances énergétiques des logements en France_
>
> Projet réalisé dans le cadre du Master 2 **SISE – Statistique et Informatique pour la Science des donnéEs (Lyon 2)**  
> Année universitaire 2025-2026

---

## Objectif du projet

L'objectif de **GreenTech Solutions** est de construire une chaîne complète d'analyse et de prédiction à partir des données publiques des **Diagnostics de Performance Énergétique (DPE)**.

Le projet couvre toutes les étapes du cycle de la donnée :

1. **Extraction et nettoyage** des données ADEME (DPE existants & neufs)  
2. **Analyse exploratoire et modélisation** (classification & régression)  
3. **Déploiement** d'une application web interactive sous **Streamlit**  
4. **Documentation** technique et fonctionnelle

---


## 🚀 Fonctionnalités

### Interface Utilisateur (Streamlit)
-  **Tableau de bord** : Visualisation interactive des données DPE
-  **Analyse** : Analyses statistiques approfondies
-  **Enedis** : Intégration des données de consommation Enedis
-  **Prédiction** : Prédiction d'étiquette DPE et de coûts énergétiques
-  API : mise à disposition de données et de modèles à travers une API
-  **Rafraîchissement des données** : Mise à jour automatique depuis l'API ADEME
-  **Réentraînement des modèles** : Réentraînement des modèles ML avec nouvelles données

### API REST (FastAPI)
-  **Prédictions individuelles** : Endpoint `/predict`
-  **Prédictions par lot** : Endpoint `/predict/batch`
-  **Métriques des modèles** : Endpoint `/models/metrics`
-  **Rafraîchissement des données** : Endpoint `/data/refresh`
-  **Réentraînement** : Endpoint `/models/retrain`

##  Prérequis

- Python 3.10+
- Docker et Docker Compose (optionnel mais recommandé)

---

##  Structure du projet

```
greentech-solutions/
├── Data/                                               # Données provenant des Apis
├   ├──data_ademe_existants_69.csv
│   ├──data_ademe_existants_69.csv
│   ├──donnees_enedis_69_.csv                           # Application Streamlit principale
├── Notebooks/
├   ├──1_extraction_preparation_donnees.ipynb
│   ├──2_exploration_donnees.ipynb
│   ├──3_classification_regression.ipynb
├── streamlit/
|   ├── app.py                          # Application Streamlit principale
|   ├── pages/                          # Pages Streamlit
|   │   ├── welcome.py
|   │   ├── home.py
|   │   ├── analysis.py
|   │   ├── enedis.py
|   │   ├── prediction.py
|   │   ├── compare.py
|   │   ├── about.py
|   │   ├── refresh_data.py            
|   │   └── retrain_models.py          
|   ├── utils/                         # Modules utilitaires
|   │   ├── data_loader.py
|   │   ├── model_utils.py
|   │   ├── data_refresher.py          
|   │   └── model_trainer.py           
|   ├── api/                           # API FastAPI
|   │   └── main.py                    
|   ├── models/                        # Modèles ML sauvegardés
|   │   ├── classification_model.pkl
|   │   ├── regression_model.pkl
|   │   └── metrics.json
|   ├── data/                          # Données
|   │   ├── donnees_ademe_finales_nettoyees_69_final_pret.csv
|   │   ├──donnees_enedis_69_finales.csv
|   │   ├── adresses-69.csv
|   │   └── metadata.json
|   ├── app.py                          # Application Streamlit principale
|   ├── pages/                          # Pages Streamlit
|   │   ├── welcome.py
|   │   ├── home.py
|   │   ├── analysis.py
|   │   ├── enedis.py
|   │   ├── prediction.py
|   │   ├── compare.py
|   │   ├── about.py
|   │   ├── refresh_data.py            
|   │   └── retrain_models.py          
|   ├── utils/                         # Modules utilitaires
|   │   ├── data_loader.py
|   │   ├── model_utils.py
|   │   ├── data_refresher.py          
|   │   └── model_trainer.py           
|   ├── api/                           # API FastAPI
|   │   └── main.py                    
|   ├── models/                        # Modèles ML sauvegardés
|   │   ├── classification_model.pkl
|   │   ├── regression_model.pkl
|   │   └── metrics.json
|   ├── data/                          # Données application
|   │   ├── donnees_ademe_finales_nettoyees_69_final_pret.csv
|   │   ├──donnees_enedis_69_finales.csv
|   │   ├── adresses-69.csv
|   │   └── metadata.json
├── Dockerfile                     
├── docker-compose.yml             
├── docker-entrypoint.sh           
├── requirements.txt
├── .dockerignore                  
└── README.md
```
<p align="center"><img src="schema_archicture_projet.jpg" alt="Schéma d’architecture du projet" width="80%"></p>
```


## Stack technique

| Domaine | Outils |
|----------|--------|
| Langage principal | Python 3.10+ |
| Data & ML | pandas, numpy, scikit-learn |
| Visualisation | Plotly Express, Streamlit |
| API & déploiement | FastAPI, unicorn, Render |
| Conteneurisation | Docker |
| Collaboration | GitHub, Taiga (Scrum) |

---

## Équipe & rôles

| Membre | Rôle principal | Rôles secondaires |
|---------|----------------|-------------------|
| **Nico Dena** | Responsable data & intégration |Ingestion, Modélisation et documentation |
| **Modou Mboup** | Responsable ML & qualité | Interface, déploiement |
| **Rina Razafimahefa** | Responsable interface & design | Data, documentation |

> Chaque membre a contribué à plusieurs volets du projet : la répartition est indicative mais la production a été collective et itérative selon les sprints.

---

## Organisation agile

- Outil de gestion : [Taiga.io](https://tree.taiga.io/) – Méthode **Scrum**  
- Backlog structuré en 6 Épics : Data / ML / Interface / Déploiement / Documentation / Gestion  
- Sprints hebdomadaires (burndown suivi automatiquement)  
- Revue et rétrospective à chaque fin de sprint  

---

## Livrables clés

| Type | Fichier / dossier |
|-------|-------------------|
| Dataset final | `Data/donnees_ademe_finales_nettoyees_69_final_pret.csv`, `Data/donnees_enedis_69_finales.csv` |
| Modèles | `streamlit/models/classification_model.pkl`, `streamlit/models/regression_model.pkl` |
| Application Streamlit | `streamlit/app.py` |
| Documentation technique | `docs/doc_technique.md` |
| Documentation fonctionnelle | `docs/doc_fonctionnelle.md` |
| Rapport ML | `docs/rapport_ml.md` |
| Vidéo démo | 🔗 _[Lien à venir]_ |

---


## 🛠️ Installation

### Option 1 : Installation locale

```bash
# Cloner le dépôt
git clone https://github.com/Modou010/m2_enedis.git
cd greentech-solutions

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application Streamlit
streamlit run app.py

# Dans un autre terminal, lancer l'API FastAPI
uvicorn api.main:app --reload
```

### Option 2 : Avec Docker (Recommandé)

```bash
# Construire et lancer les services
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter les services
docker-compose down
```

##  Accès aux services

Une fois lancé :

- **Interface Streamlit** : [http://localhost:8501](http://localhost:8501)
- **API FastAPI** : [http://localhost:8000](http://localhost:8000)
- **Documentation API** : [http://localhost:8000/docs](http://localhost:8000/docs)

## Rafraîchissement des données

### Via l'interface Streamlit
1. Aller dans " Rafraîchir données"
2. Choisir le mode (nouveaux DPE uniquement ou rechargement complet)
3. Cliquer sur "Lancer le rafraîchissement"

### Via l'API
```bash
# Rafraîchissement incrémental
curl -X POST http://localhost:8000/data/refresh

# Rechargement complet
curl -X POST http://localhost:8000/data/refresh?full_reload=true
```

## Réentraînement des modèles

### Via l'interface Streamlit
1. Aller dans " Réentraîner modèles"
2. Configurer les hyperparamètres (optionnel)
3. Cliquer sur "Lancer l'entraînement"

### Via l'API
```bash
curl -X POST http://localhost:8000/models/retrain
```

## 🔌 Exemples d'utilisation de l'API

### Prédiction individuelle
```python
import requests

url = "http://localhost:8000/predict"
data = {
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
}

response = requests.post(url, json=data)
print(response.json())
```

### Récupérer les métriques des modèles
```python
import requests

response = requests.get("http://localhost:8000/models/metrics")
metrics = response.json()

print(f"Accuracy: {metrics['classification']['accuracy']}")
print(f"R² Score: {metrics['regression']['r2_score']}")
```

## 🐳 Gestion Docker

### Construire l'image
```bash
docker build -t greentech-solutions .
```

### Lancer uniquement Streamlit
```bash
docker run -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  -e SERVICE_MODE=streamlit \
  greentech-solutions
```

### Lancer uniquement l'API
```bash
docker run -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  -e SERVICE_MODE=api \
  greentech-solutions
```

## 📊 Modèles de Machine Learning

### Modèle de Classification
- **Algorithme** : Random Forest Classifier
- **Objectif** : Prédire l'étiquette DPE (A, B, C, D, E, F, G)
- **Performance** : ~96% accuracy

### Modèle de Régression
- **Algorithme** : DecisionTree Regressor
- **Objectif** : Prédire le coût total des 5 usages (€/an)
- **Performance** : R² > 0.97

### Features utilisées
- `conso_auxiliaires_ef`
- `cout_eclairage`
- `conso_5_usages_par_m2_ef`
- `conso_5_usages_ef`
- `surface_habitable_logement`
- `cout_ecs`
- `type_batiment`
- `conso_ecs_ef`
- `conso_refroidissement_ef`
- `type_energie_recodee`

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request, ou à nous laisser un message

## 📄 Licence

Ce projet est sous licence MIT.

## Contact

Pour toute question, contactez l'équipe GreenTech Solutions : franckdena@gmail.com, mboupmodou05@gmail.com, n.razafimahefa@univ-lyon2.fr

---

**Version** : 1.0.0  
**Dernière mise à jour** : 2025
