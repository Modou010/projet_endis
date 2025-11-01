import pandas as pd
import numpy as np
import joblib
import json
import os
from datetime import datetime
from typing import Tuple, Dict, Any
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import (
    classification_report, 
    accuracy_score, 
    f1_score, 
    r2_score, 
    mean_squared_error, 
    mean_absolute_error
)

class ModelTrainer:
    """Classe pour entraîner et réentraîner les modèles de ML"""
    
    # Features utilisées pour les modèles
    FEATURES = [
        'conso_auxiliaires_ef',
        'cout_eclairage',
        'conso_5_usages_par_m2_ef',
        'conso_5_usages_ef',
        'surface_habitable_logement',
        'cout_ecs',
        'type_batiment',
        'conso_ecs_ef',
        'conso_refroidissement_ef',
        'type_energie_recodee'
    ]
    
    # Targets
    TARGET_CLASSIFICATION = 'etiquette_dpe'
    TARGET_REGRESSION = 'cout_total_5_usages'
    
    # Chemins des fichiers
    DATA_FILE = 'data/donnees_ademe_finales_nettoyees_69_final_pret.csv'
    CLASSIFIER_PATH = 'models/classification_model.pkl'
    REGRESSOR_PATH = 'models/regression_model.pkl'
    METRICS_PATH = 'models/metrics.json'
    
    def __init__(self):
        """Initialiser le trainer"""
        os.makedirs('models', exist_ok=True)
    
    def prepare_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Préparer les données pour l'entraînement
        
        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: (données pour classification, données pour régression)
        """
        # Copier pour ne pas modifier l'original
        df_clean = df.copy()
        
        # Supprimer les valeurs manquantes sur les features et targets
        required_cols_classif = self.FEATURES + [self.TARGET_CLASSIFICATION]
        required_cols_regress = self.FEATURES + [self.TARGET_REGRESSION]
        
        df_classif = df_clean[required_cols_classif].dropna()
        df_regress = df_clean[required_cols_regress].dropna()
        
        # Encoder les variables catégorielles
        df_classif = self._encode_features(df_classif)
        df_regress = self._encode_features(df_regress)
        
        return df_classif, df_regress
    
    def _encode_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Encoder les variables catégorielles"""
        df = df.copy()
        
        # Mapping type_batiment
        type_batiment_map = {
            'maison': 0,
            'appartement': 1,
            'immeuble': 2
        }
        
        # Mapping type_energie
        energie_map = {
            'Electricite': 0,
            'Gaz_naturel': 1,
            'Fioul domestique': 2,
            'Reseau_de_chauffage_urbain': 3,
            'Autres': 4
        }
        
        # Appliquer les mappings si les colonnes existent
        if 'type_batiment' in df.columns:
            # Gérer les valeurs non mappées
            df['type_batiment'] = df['type_batiment'].apply(
                lambda x: type_batiment_map.get(x, 1) if pd.notna(x) else 1
            )
        
        if 'type_energie_recodee' in df.columns:
            df['type_energie_recodee'] = df['type_energie_recodee'].apply(
                lambda x: energie_map.get(x, 0) if pd.notna(x) else 0
            )
        
        return df
    
    def train_classification_model(
        self, 
        df: pd.DataFrame,
        test_size: float = 0.3,
        random_state: int = 42,
        **model_params
    ) -> Tuple[RandomForestClassifier, Dict[str, Any]]:
        """
        Entraîner le modèle de classification pour prédire l'étiquette DPE
        
        Returns:
            Tuple[model, metrics]: Modèle entraîné et métriques de performance
        """
        # Séparer features et target
        X = df[self.FEATURES]
        y = df[self.TARGET_CLASSIFICATION]
        
        # Split train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Paramètres par défaut du modèle
        default_params = {
            'n_estimators': 300,
            'max_depth': None,
            'random_state': random_state,
            'n_jobs': -1
        }
        default_params.update(model_params)
        
        # Entraîner le modèle
        model = RandomForestClassifier(**default_params)
        model.fit(X_train, y_train)
        
        # Prédictions
        y_pred = model.predict(X_test)
        
        # Calculer les métriques
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        metrics = {
            'model_type': 'classification',
            'accuracy': float(accuracy),
            'f1_score': float(f1),
            'train_samples': len(X_train),
            'test_samples': len(X_test),
            'classes': list(model.classes_),
            'classification_report': classification_report(y_test, y_pred, output_dict=True),
            'feature_importance': dict(zip(self.FEATURES, model.feature_importances_.tolist())),
            'trained_at': datetime.now().isoformat()
        }
        
        return model, metrics
    
    def train_regression_model(
        self,
        df: pd.DataFrame,
        test_size: float = 0.3,
        random_state: int = 42,
        **model_params
    ) -> Tuple[DecisionTreeRegressor, Dict[str, Any]]:
        """
        Entraîner le modèle de régression pour prédire le coût total
        
        Returns:
            Tuple[model, metrics]: Modèle entraîné et métriques de performance
        """
        # Séparer features et target
        X = df[self.FEATURES]
        y = df[self.TARGET_REGRESSION]
        
        # Split train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        # Paramètres par défaut du modèle
        default_params = {
            'max_depth': 30,
            'min_samples_split': 20,
            'min_samples_leaf': 4,
            'random_state': random_state
        }
        default_params.update(model_params)
        
        # Entraîner le modèle
        model = DecisionTreeRegressor(**default_params)
        model.fit(X_train, y_train)
        
        # Prédictions
        y_pred = model.predict(X_test)
        
        # Calculer les métriques
        r2 = r2_score(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        
        metrics = {
            'model_type': 'regression',
            'r2_score': float(r2),
            'mse': float(mse),
            'rmse': float(rmse),
            'mae': float(mae),
            'train_samples': len(X_train),
            'test_samples': len(X_test),
            'feature_importance': dict(zip(self.FEATURES, model.feature_importances_.tolist())),
            'trained_at': datetime.now().isoformat()
        }
        
        return model, metrics
    
    def train_all_models(
        self,
        data_path: str = "data/donnees_ademe_finales_nettoyees_69_final_pret.csv",
        save_models: bool = True,
        progress_callback=None
    ) -> Dict[str, Any]:
        """
        Entraîner tous les modèles (classification et régression)
        
        Returns:
            Dict contenant les métriques des deux modèles
        """
        # Charger les données
        if progress_callback:
            progress_callback("Chargement des données...")
        
        df = pd.read_csv(data_path)
        
        # Préparer les données
        if progress_callback:
            progress_callback("Préparation des données...")
        
        df_classif, df_regress = self.prepare_data(df)
        
        # Entraîner le modèle de classification
        if progress_callback:
            progress_callback("Entraînement du modèle de classification...")
        
        classifier, classif_metrics = self.train_classification_model(df_classif)
        
        # Entraîner le modèle de régression
        if progress_callback:
            progress_callback("Entraînement du modèle de régression...")
        
        regressor, regress_metrics = self.train_regression_model(df_regress)
        
        # Sauvegarder les modèles
        if save_models:
            if progress_callback:
                progress_callback("Sauvegarde des modèles...")
            
            self.save_models(classifier, regressor)
            self.save_metrics({
                'classification': classif_metrics,
                'regression': regress_metrics
            })
        
        if progress_callback:
            progress_callback("Entraînement terminé !")
        
        return {
            'classification': classif_metrics,
            'regression': regress_metrics
        }
    
    def save_models(self, classifier, regressor):
        """Sauvegarder les modèles entraînés"""
        joblib.dump(classifier, self.CLASSIFIER_PATH)
        joblib.dump(regressor, self.REGRESSOR_PATH)
    
    def save_metrics(self, metrics: Dict[str, Any]):
        """Sauvegarder les métriques d'entraînement"""
        with open(self.METRICS_PATH, 'w') as f:
            json.dump(metrics, f, indent=2)
    
    def load_models(self) -> Tuple[RandomForestClassifier, DecisionTreeRegressor]:
        """Charger les modèles sauvegardés"""
        if not os.path.exists(self.CLASSIFIER_PATH) or not os.path.exists(self.REGRESSOR_PATH):
            raise FileNotFoundError("Les modèles n'existent pas. Veuillez les entraîner d'abord.")
        
        classifier = joblib.load(self.CLASSIFIER_PATH)
        regressor = joblib.load(self.REGRESSOR_PATH)
        
        return classifier, regressor
    
    def load_metrics(self) -> Dict[str, Any]:
        """Charger les métriques sauvegardées"""
        if not os.path.exists(self.METRICS_PATH):
            return {}
        
        with open(self.METRICS_PATH, 'r') as f:
            return json.load(f)