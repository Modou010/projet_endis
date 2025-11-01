"""
Client pour interagir avec l'API FastAPI depuis Streamlit
"""

import requests
from typing import Dict, List, Any, Optional
import streamlit as st

class APIClient:
    """Client pour l'API GreenTech Solutions"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialiser le client API
        
        Args:
            base_url: URL de base de l'API
        """
        self.base_url = base_url.rstrip('/')
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Gérer la réponse de l'API"""
        if response.status_code == 200:
            return response.json()
        else:
            error_msg = f"Erreur API ({response.status_code}): {response.text}"
            raise Exception(error_msg)
    
    def health_check(self) -> Dict[str, Any]:
        """Vérifier l'état de l'API"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return self._handle_response(response)
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
    
    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Faire une prédiction individuelle
        
        Args:
            features: Dictionnaire contenant les features du logement
            
        Returns:
            Dict avec etiquette_dpe, cout_total_5_usages, probabilities
        """
        response = requests.post(f"{self.base_url}/predict", json=features)
        return self._handle_response(response)
    
    def predict_batch(self, data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Faire des prédictions multiples
        
        Args:
            data_list: Liste de dictionnaires contenant les features
            
        Returns:
            Dict avec predictions et total
        """
        payload = {"data": data_list}
        response = requests.post(f"{self.base_url}/predict/batch", json=payload)
        return self._handle_response(response)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Récupérer les métriques des modèles"""
        response = requests.get(f"{self.base_url}/models/metrics")
        return self._handle_response(response)
    
    def get_models_info(self) -> Dict[str, Any]:
        """Récupérer les informations sur les modèles"""
        response = requests.get(f"{self.base_url}/models/info")
        return self._handle_response(response)
    
    def refresh_data(self, full_reload: bool = False) -> Dict[str, Any]:
        """
        Rafraîchir les données
        
        Args:
            full_reload: Si True, recharge toutes les données
            
        Returns:
            Dict avec status, message, new_records, total_records
        """
        response = requests.post(
            f"{self.base_url}/data/refresh",
            params={"full_reload": full_reload}
        )
        return self._handle_response(response)
    
    def retrain_models(self) -> Dict[str, Any]:
        """Lancer le réentraînement des modèles"""
        response = requests.post(f"{self.base_url}/models/retrain")
        return self._handle_response(response)

# Fonction utilitaire pour Streamlit
@st.cache_resource
def get_api_client(base_url: str = "http://localhost:8000") -> APIClient:
    """
    Obtenir une instance du client API (cachée)
    
    Args:
        base_url: URL de base de l'API
        
    Returns:
        Instance du client API
    """
    return APIClient(base_url)

# Widget Streamlit pour afficher le statut de l'API
def display_api_status(api_client: APIClient):
    """
    Afficher le statut de l'API dans Streamlit
    
    Args:
        api_client: Instance du client API
    """
    health = api_client.health_check()
    
    if health.get('status') == 'healthy':
        st.success("✅ API opérationnelle")
    elif health.get('status') == 'degraded':
        st.warning("⚠️ API dégradée (modèles non chargés)")
    else:
        st.error(f"❌ API non disponible: {health.get('error', 'Erreur inconnue')}")
    
    return health

# Exemple d'utilisation dans une page Streamlit
def example_usage():
    """Exemple d'utilisation du client API dans Streamlit"""
    
    st.title("Exemple d'utilisation de l'API")
    
    # Obtenir le client API
    api_client = get_api_client()
    
    # Afficher le statut
    st.subheader("Statut de l'API")
    health = display_api_status(api_client)
    
    if health.get('status') != 'healthy':
        st.stop()
    
    # Faire une prédiction
    st.subheader("Prédiction")
    
    if st.button("Faire une prédiction test"):
        features = {
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
        
        try:
            result = api_client.predict(features)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Étiquette DPE", result['etiquette_dpe'])
            with col2:
                st.metric("Coût prédit", f"{result['cout_total_5_usages']:.0f} €")
            
            if result.get('probabilities'):
                st.subheader("Probabilités")
                st.json(result['probabilities'])
        
        except Exception as e:
            st.error(f"Erreur: {e}")
    
    # Récupérer les métriques
    st.subheader("Métriques des modèles")
    
    if st.button("Afficher les métriques"):
        try:
            metrics = api_client.get_metrics()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Classification**")
                st.metric("Accuracy", f"{metrics['classification']['accuracy']*100:.2f}%")
                st.metric("F1-Score", f"{metrics['classification']['f1_score']:.3f}")
            
            with col2:
                st.write("**Régression**")
                st.metric("R² Score", f"{metrics['regression']['r2_score']:.3f}")
                st.metric("MAE", f"{metrics['regression']['mae']:.2f} €")
        
        except Exception as e:
            st.error(f"Erreur: {e}")

if __name__ == "__main__":
    example_usage()