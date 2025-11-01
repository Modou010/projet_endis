# GreenTech Solutions - Dashboard Énergétique Rhône

Application complète d'analyse énergétique basée sur les données DPE (Diagnostic de Performance Énergétique) et Enedis de la région Rhône-Alpes.

## 🚀 Fonctionnalités

### Interface Utilisateur (Streamlit)
- 📊 **Tableau de bord** : Visualisation interactive des données DPE
- 📈 **Analyse** : Analyses statistiques approfondies
- ⚡ **Enedis** : Intégration des données de consommation Enedis
- 🔮 **Prédiction** : Prédiction d'étiquette DPE et de coûts énergétiques
- ⚖️ **Comparaison** : Comparaison entre logements
- 🔄 **Rafraîchissement des données** : Mise à jour automatique depuis l'API ADEME
- 🎯 **Réentraînement des modèles** : Réentraînement des modèles ML avec nouvelles données

### API REST (FastAPI)
- 🔌 **Prédictions individuelles** : Endpoint `/predict`
- 📦 **Prédictions par lot** : Endpoint `/predict/batch`
- 📊 **Métriques des modèles** : Endpoint `/models/metrics`
- 🔄 **Rafraîchissement des données** : Endpoint `/data/refresh`
- 🎯 **Réentraînement** : Endpoint `/models/retrain`

## 📋 Prérequis

- Python 3.10+
- Docker et Docker Compose (optionnel mais recommandé)

## 🛠️ Installation

### Option 1 : Installation locale

```bash
# Cloner le dépôt
git clone <votre-repo>
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

## 🌐 Accès aux services

Une fois lancé :

- **Interface Streamlit** : [http://localhost:8501](http://localhost:8501)
- **API FastAPI** : [http://localhost:8000](http://localhost:8000)
- **Documentation API** : [http://localhost:8000/docs](http://localhost:8000/docs)

## 📁 Structure du projet

```
greentech-solutions/
├── app.py                          # Application Streamlit principale
├── pages/                          # Pages Streamlit
│   ├── welcome.py
│   ├── home.py
│   ├── analysis.py
│   ├── enedis.py
│   ├── prediction.py
│   ├── compare.py
│   ├── about.py
│   ├── refresh_data.py            # Nouvelle page
│   └── retrain_models.py          # Nouvelle page
├── utils/                         # Modules utilitaires
│   ├── data_loader.py
│   ├── model_utils.py
│   ├── data_refresher.py          # Nouveau module
│   └── model_trainer.py           # Nouveau module
├── api/                           # API FastAPI
│   └── main.py                    # Nouveau fichier
├── models/                        # Modèles ML sauvegardés
│   ├── classification_model.pkl
│   ├── regression_model.pkl
│   └── metrics.json
├── data/                          # Données
│   ├── donnees_ademe_finales_nettoyees_69_final_pret.csv
│   ├── adresses-69.csv
│   └── metadata.json
├── Dockerfile                     # Nouveau fichier
├── docker-compose.yml             # Nouveau fichier
├── docker-entrypoint.sh           # Nouveau fichier
├── requirements.txt
├── .dockerignore                  # Nouveau fichier
└── README.md
```

## 🔄 Rafraîchissement des données

### Via l'interface Streamlit
1. Aller dans "🔄 Rafraîchir données"
2. Choisir le mode (nouveaux DPE uniquement ou rechargement complet)
3. Cliquer sur "Lancer le rafraîchissement"

### Via l'API
```bash
# Rafraîchissement incrémental
curl -X POST http://localhost:8000/data/refresh

# Rechargement complet
curl -X POST http://localhost:8000/data/refresh?full_reload=true
```

## 🎯 Réentraînement des modèles

### Via l'interface Streamlit
1. Aller dans "🎯 Réentraîner modèles"
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

### Pousser vers un registry Docker
```bash
# Tag l'image
docker tag greentech-solutions:latest votre-registry/greentech-solutions:latest

# Push vers le registry
docker push votre-registry/greentech-solutions:latest
```

## 📊 Modèles de Machine Learning

### Modèle de Classification
- **Algorithme** : Random Forest Classifier
- **Objectif** : Prédire l'étiquette DPE (A, B, C, D, E, F, G)
- **Performance** : ~98% accuracy

### Modèle de Régression
- **Algorithme** : Random Forest Regressor
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

## 🔒 Sécurité

Pour un déploiement en production :

1. **Changer les CORS** dans `api/main.py`
2. **Ajouter une authentification** (JWT, OAuth2)
3. **Utiliser HTTPS**
4. **Limiter le rate limiting**
5. **Ajouter des logs structurés**

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## 📄 Licence

Ce projet est sous licence MIT.

## 📞 Contact

Pour toute question, contactez l'équipe GreenTech Solutions.

---

**Version** : 1.0.0  
**Dernière mise à jour** : 2024