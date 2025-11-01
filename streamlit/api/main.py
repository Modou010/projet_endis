from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import joblib
import pandas as pd
import os
import sys
from datetime import datetime

# Ajouter le chemin parent pour importer les utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.model_trainer import ModelTrainer
from utils.data_refresher import DataRefresher

# Initialiser FastAPI
app = FastAPI(
    title="GreenTech Solutions - API DPE",
    description="API pour prédictions énergétiques et gestion des modèles ML",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === SCHEMAS PYDANTIC ===

class DPEFeatures(BaseModel):
    """Features pour la prédiction DPE"""
    conso_auxiliaires_ef: float = Field(..., description="Consommation auxiliaires (kWh/an)")
    cout_eclairage: float = Field(..., description="Coût éclairage (€/an)")
    conso_5_usages_par_m2_ef: float = Field(..., description="Consommation 5 usages par m² (kWh/m²/an)")
    conso_5_usages_ef: float = Field(..., description="Consommation 5 usages totale (kWh/an)")
    surface_habitable_logement: float = Field(..., description="Surface habitable (m²)")
    cout_ecs: float = Field(..., description="Coût ECS (€/an)")
    type_batiment: str = Field(..., description="Type de bâtiment (maison/appartement/immeuble)")
    conso_ecs_ef: float = Field(..., description="Consommation ECS (kWh/an)")
    conso_refroidissement_ef: float = Field(..., description="Consommation refroidissement (kWh/an)")
    type_energie_recodee: str = Field(..., description="Type d'énergie principale")
    
    class Config:
        schema_extra = {
            "example": {
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
        }

class PredictionResponse(BaseModel):
    """Réponse de prédiction"""
    etiquette_dpe: str
    cout_total_5_usages: float
    probabilities: Optional[Dict[str, float]] = None
    timestamp: str

class BatchPredictionRequest(BaseModel):
    """Requête pour prédictions multiples"""
    data: List[DPEFeatures]

class BatchPredictionResponse(BaseModel):
    """Réponse pour prédictions multiples"""
    predictions: List[PredictionResponse]
    total: int

class ModelMetrics(BaseModel):
    """Métriques des modèles"""
    classification: Dict[str, Any]
    regression: Dict[str, Any]

class RefreshDataResponse(BaseModel):
    """Réponse du rafraîchissement des données"""
    status: str
    message: str
    new_records: Optional[int] = None
    total_records: Optional[int] = None

class RetrainResponse(BaseModel):
    """Réponse du réentraînement"""
    status: str
    message: str
    metrics: Optional[Dict[str, Any]] = None

# === VARIABLES GLOBALES ===

trainer = ModelTrainer()
refresher = DataRefresher()

# Charger les modèles au démarrage
try:
    classifier, regressor = trainer.load_models()
except Exception as e:
    print(f"⚠️ Modèles non chargés au démarrage: {e}")
    classifier, regressor = None, None

# === ENDPOINTS ===

@app.get("/")
def root():
    """Endpoint racine"""
    return {
        "message": "GreenTech Solutions - API DPE",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "predict_batch": "/predict/batch",
            "metrics": "/models/metrics",
            "refresh_data": "/data/refresh",
            "retrain": "/models/retrain"
        }
    }

@app.get("/health")
def health_check():
    """Vérifier l'état de l'API"""
    models_loaded = classifier is not None and regressor is not None
    
    return {
        "status": "healthy" if models_loaded else "degraded",
        "models_loaded": models_loaded,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/predict", response_model=PredictionResponse)
def predict(features: DPEFeatures):
    """
    Prédire l'étiquette DPE et le coût total pour un logement
    """
    global classifier, regressor
    
    if classifier is None or regressor is None:
        raise HTTPException(status_code=503, detail="Modèles non chargés. Veuillez entraîner les modèles d'abord.")
    
    try:
        # Préparer les données
        input_dict = features.dict()
        df_input = pd.DataFrame([input_dict])
        
        # Encoder les variables catégorielles
        type_batiment_map = {'maison': 0, 'appartement': 1, 'immeuble': 2}
        energie_map = {
            'Electricite': 0, 'Gaz_naturel': 1, 'Fioul domestique': 2,
            'Reseau_de_chauffage_urbain': 3, 'Autres': 4
        }
        
        df_input['type_batiment'] = df_input['type_batiment'].map(type_batiment_map).fillna(1)
        df_input['type_energie_recodee'] = df_input['type_energie_recodee'].map(energie_map).fillna(0)
        
        # Prédictions
        etiquette_pred = classifier.predict(df_input)[0]
        cout_pred = float(regressor.predict(df_input)[0])
        
        # Probabilités si disponible
        probabilities = None
        if hasattr(classifier, 'predict_proba'):
            proba = classifier.predict_proba(df_input)[0]
            classes = classifier.classes_
            probabilities = {str(c): float(p) for c, p in zip(classes, proba)}
        
        return PredictionResponse(
            etiquette_dpe=etiquette_pred,
            cout_total_5_usages=cout_pred,
            probabilities=probabilities,
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction: {str(e)}")

@app.post("/predict/batch", response_model=BatchPredictionResponse)
def predict_batch(request: BatchPredictionRequest):
    """
    Prédictions multiples pour plusieurs logements
    """
    global classifier, regressor
    
    if classifier is None or regressor is None:
        raise HTTPException(status_code=503, detail="Modèles non chargés.")
    
    try:
        predictions = []
        
        for features in request.data:
            # Utiliser l'endpoint de prédiction individuelle
            pred = predict(features)
            predictions.append(pred)
        
        return BatchPredictionResponse(
            predictions=predictions,
            total=len(predictions)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors des prédictions: {str(e)}")

@app.get("/models/metrics", response_model=ModelMetrics)
def get_model_metrics():
    """
    Récupérer les métriques de performance des modèles
    """
    try:
        metrics = trainer.load_metrics()
        
        if not metrics:
            raise HTTPException(status_code=404, detail="Aucune métrique disponible. Veuillez entraîner les modèles d'abord.")
        
        return ModelMetrics(**metrics)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des métriques: {str(e)}")

@app.post("/data/refresh", response_model=RefreshDataResponse)
def refresh_data(background_tasks: BackgroundTasks, full_reload: bool = False):
    """
    Rafraîchir les données depuis l'API ADEME
    
    Parameters:
    - full_reload: Si True, recharge toutes les données. Sinon, uniquement les nouveaux DPE.
    """
    try:
        if full_reload:
            # Mode rechargement complet (tâche de fond recommandée)
            background_tasks.add_task(perform_full_reload)
            return RefreshDataResponse(
                status="started",
                message="Rechargement complet lancé en arrière-plan. Cela peut prendre plusieurs minutes."
            )
        else:
            # Mode incrémental
            new_df, new_count = refresher.refresh_new_data()
            
            if new_count == 0:
                return RefreshDataResponse(
                    status="success",
                    message="Aucun nouveau DPE trouvé. Les données sont à jour.",
                    new_records=0
                )
            
            # Fusionner avec les données existantes
            merged_df = refresher.merge_with_existing(new_df)
            refresher.save_refreshed_data(merged_df, backup=True)
            
            return RefreshDataResponse(
                status="success",
                message=f"{new_count} nouveaux DPE récupérés et fusionnés.",
                new_records=new_count,
                total_records=len(merged_df)
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du rafraîchissement: {str(e)}")

def perform_full_reload():
    """Effectuer un rechargement complet (tâche de fond)"""
    all_results = []
    for cp in refresher.codes_postaux:
        results = refresher.fetch_data_smart(cp)
        all_results.extend(results)
    
    if all_results:
        df_complete = pd.DataFrame(all_results)
        refresher.save_refreshed_data(df_complete, backup=True)
        refresher.save_metadata(datetime.now().strftime("%Y-%m-%d"), len(df_complete))

@app.post("/models/retrain", response_model=RetrainResponse)
def retrain_models(background_tasks: BackgroundTasks):
    """
    Réentraîner les modèles de classification et régression
    """
    global classifier, regressor
    
    try:
        # Lancer le réentraînement en arrière-plan
        background_tasks.add_task(perform_retraining)
        
        return RetrainResponse(
            status="started",
            message="Réentraînement lancé en arrière-plan. Consultez /models/metrics pour voir les résultats."
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du réentraînement: {str(e)}")

def perform_retraining():
    """Effectuer le réentraînement (tâche de fond)"""
    global classifier, regressor
    
    try:
        metrics = trainer.train_all_models(save_models=True)
        
        # Recharger les modèles
        classifier, regressor = trainer.load_models()
        
        print(f"✅ Réentraînement terminé: Classification Accuracy={metrics['classification']['accuracy']:.3f}, Regression R²={metrics['regression']['r2_score']:.3f}")
    
    except Exception as e:
        print(f"❌ Erreur lors du réentraînement: {e}")

@app.get("/models/info")
def get_models_info():
    """
    Informations sur les modèles chargés
    """
    global classifier, regressor
    
    if classifier is None or regressor is None:
        return {
            "loaded": False,
            "message": "Aucun modèle chargé"
        }
    
    return {
        "loaded": True,
        "classifier": {
            "type": type(classifier).__name__,
            "n_features": classifier.n_features_in_ if hasattr(classifier, 'n_features_in_') else None,
            "classes": list(classifier.classes_) if hasattr(classifier, 'classes_') else None
        },
        "regressor": {
            "type": type(regressor).__name__,
            "n_features": regressor.n_features_in_ if hasattr(regressor, 'n_features_in_') else None
        },
        "features": trainer.FEATURES
    }

# === LANCEMENT DE L'API ===

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)