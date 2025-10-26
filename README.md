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
3. **Déploiement** d'une application web interactive sous **Dash**  
4. **Documentation** technique et fonctionnelle, accompagnée d'une **vidéo de démonstration**

---

## Architecture du dépôt

```
m2_enedis/
├── app/                     # Application Dash
│   ├── app.py               # Serveur principal (Dash + API)
│   ├── assets/              # Fichiers CSS, images
│   ├── model/               # Modèles entraînés (.pkl)
│   └── utils/               # Fonctions auxiliaires
│
├── data/
│   ├── raw/                 # Données brutes ADEME
│   └── processed/           # Données nettoyées
│
├── notebooks/               # Analyse et modélisation
│   ├── exploration.ipynb
│   ├── classification.ipynb
│   └── regression.ipynb
│
├── docker/                  # Conteneurisation
│   └── Dockerfile
│
├── docs/                    # Documentation et livrables
│   ├── doc_technique.md
│   ├── doc_fonctionnelle.md
│   ├── rapport_ml.md
│   └── assets/              # Schémas & captures d’écran
│
├── requirements.txt
├── Procfile                 # Déploiement Render
├── runtime.txt              # Version Python
└── README.md
```

---

## Stack technique

| Domaine | Outils |
|----------|--------|
| Langage principal | Python 3.10+ |
| Data & ML | pandas, numpy, scikit-learn |
| Visualisation | Plotly Express, Dash |
| API & déploiement | Flask, gunicorn, Render |
| Conteneurisation | Docker |
| Collaboration | GitHub, Taiga (Scrum) |

---

## Équipe & rôles

| Membre | Rôle principal | Rôles secondaires |
|---------|----------------|-------------------|
| **Nico Dena** | Responsable data & intégration | Modélisation, documentation |
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
| Dataset final | `data/processed/dpe_full.parquet` |
| Modèles | `app/model/classification_model.pkl`, `app/model/regression_model.pkl` |
| Application Dash | `app/app.py` |
| Documentation technique | `docs/doc_technique.md` |
| Documentation fonctionnelle | `docs/doc_fonctionnelle.md` |
| Rapport ML | `docs/rapport_ml.md` |
| Vidéo démo | 🔗 _[Lien à venir]_ |

---

## Installation locale

```bash
# 1. Cloner le dépôt
git clone https://github.com/<votre_repo>.git
cd <votre_repo>

# 2. Créer l’environnement virtuel
python -m venv venv
source venv\Scripts\activate  # ou venv/bin/activate sous MacOS

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'application Dash
python app/app.py
```

---

## Déploiement

L'application est hébergée sur **Render** :  
🔗 [Lien vers l'application déployée](https://...)  

Endpoints disponibles :
- `/predict` → prédiction DPE + consommation  
- `/health` → vérification du service  
- `/retrain` → réentraînement du modèle

---

### 📊 Statut du projet

| Sprint | État | Avancement |
|---------|------|-------------|
| Sprint 1 - Data Foundation | ✅ Terminé | 100 % |
| Sprint 2 - Model Building | 🔄 En cours | 20 % |
| Sprint 3 - Deployment & API | 🔄 En cours | 20 % |
| Sprint 4 - Final Delivery | 🔜 À venir | - |
