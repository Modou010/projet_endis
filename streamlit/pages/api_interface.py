
import streamlit as st
import requests
import json
import pandas as pd
import plotly.graph_objects as go
import sys
import os
from datetime import datetime

# Ajouter le chemin parent pour importer utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuration de l'API
API_BASE_URL = "http://localhost:8000"

def check_api_status():
    """Vérifier si l'API est accessible"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, None
    except:
        return False, None

def show():
    st.title("Interface API")
    st.markdown("### Accès et test de l'API REST GreenTech Solutions")
    
    # Vérifier le statut de l'API
    api_available, health_data = check_api_status()
    
    st.markdown("---")
    
    # Onglets principaux
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Documentation",
        "Testeur de Prédiction",
        "Métriques des Modèles",
        "Endpoints",
        "Exemples de Code"
    ])
    st.markdown("""
<style>
/* Conteneur global des tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

/* Style général des onglets */
.stTabs [data-baseweb="tab"] {
    background-color: #e8f5e9;
    color: #1b5e20;
    border-radius: 6px 6px 0 0;
    padding: 8px 16px;
    font-weight: 500;
    font-size: 15px;
    border: none !important;
    transition: all 0.3s ease;
    border-bottom: 3px solid transparent !important;
}

/* Onglet actif */
.stTabs [aria-selected="true"] {
    background-color: #1b5e20 !important;
    color: white !important;
    font-weight: 600;
    border: none !important;
    border-bottom: 3px solid #1b5e20 !important;
}

/* Hover */
.stTabs [data-baseweb="tab"]:hover {
    background-color: #2e7d32 !important;
    color: white !important;
    border-bottom: 3px solid #e8f5e9 !important;
}
</style>
""", unsafe_allow_html=True)
    
    # TAB 1 : Documentation
    with tab1:
        st.markdown("#### Documentation de l'API")
        
        st.markdown("""
        L'API GreenTech Solutions est une API REST construite avec **FastAPI** qui permet d'accéder 
        aux modèles de Machine Learning pour prédire les performances énergétiques des logements.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Liens importants")
            st.markdown(f"""
            - **Documentation interactive (Swagger)** : [http://localhost:8000/docs](http://localhost:8000/docs)
            - **Documentation alternative (ReDoc)** : [http://localhost:8000/redoc](http://localhost:8000/redoc)
            - **Schéma OpenAPI** : [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)
            """)
        
        with col2:
            st.markdown("##### Informations techniques")
            st.markdown("""
            - **Framework** : FastAPI 0.104+
            - **Format** : JSON
            - **Authentification** : Non requise (dev)
            - **Rate limiting** : Non configuré (dev)
            """)
        
        st.markdown("---")
        
        st.markdown("##### Endpoints disponibles")
        
        endpoints_data = {
            "Endpoint": [
                "GET /",
                "GET /health",
                "POST /predict",
                "POST /predict/batch",
                "GET /models/metrics",
                "GET /models/info",
                "POST /models/retrain",
                "POST /data/refresh"
            ],
            "Description": [
                "Informations sur l'API",
                "Vérifier l'état de santé",
                "Prédiction individuelle",
                "Prédictions multiples",
                "Métriques des modèles",
                "Informations sur les modèles",
                "Réentraîner les modèles",
                "Rafraîchir les données"
            ],
            "Authentification": ["Non"] * 8
        }
        
        df_endpoints = pd.DataFrame(endpoints_data)
        st.dataframe(df_endpoints, use_container_width=True, hide_index=True)
    
    # TAB 2 : Testeur de Prédiction
    with tab2:
        st.markdown("#### Testeur de Prédiction Interactive")
        st.markdown("Testez l'endpoint `/predict` directement depuis cette interface")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Caractéristiques du bâtiment")
            
            type_batiment = st.selectbox(
                "Type de bâtiment (type_batiment)",
                options=['maison', 'appartement', 'immeuble'],
                help="Sélectionnez le type de construction du logement",
                key="api_type_batiment"
            )
            
            surface_habitable = st.number_input(
                "Surface habitable en m² (surface_habitable_logement)",
                min_value=10.0,
                max_value=500.0,
                value=100.0,
                step=5.0,
                help="Surface totale habitable du logement en mètres carrés",
                key="api_surface"
            )
            
            type_energie = st.selectbox(
                "Source d'énergie principale (type_energie_recodee)",
                options=['Electricite', 'Gaz_naturel', 'Fioul domestique', 
                        'Reseau_de_chauffage_urbain', 'Autres'],
                help="Énergie utilisée pour le chauffage et l'eau chaude",
                key="api_energie"
            )
        
        with col2:
            st.markdown("##### Consommations énergétiques")
            
            conso_5_usages_par_m2 = st.number_input(
                "Consommation annuelle par m² (conso_5_usages_par_m2_ef)",
                min_value=0.0,
                max_value=500.0,
                value=200.0,
                step=10.0,
                help="Consommation énergétique par m² pour chauffage, eau chaude, refroidissement, éclairage et auxiliaires (kWh/m²/an)",
                key="api_conso_m2"
            )
            
            conso_ecs = st.number_input(
                "Eau chaude sanitaire (conso_ecs_ef)",
                min_value=0.0,
                max_value=10000.0,
                value=2000.0,
                step=100.0,
                help="Consommation annuelle pour l'eau chaude (douches, bains, cuisine) en kWh/an",
                key="api_ecs"
            )
            
            conso_auxiliaires = st.number_input(
                "Ventilation et pompes (conso_auxiliaires_ef)",
                min_value=0.0,
                max_value=5000.0,
                value=500.0,
                step=50.0,
                help="Consommation des équipements auxiliaires (VMC, circulateurs, etc.) en kWh/an",
                key="api_aux"
            )
            
            conso_refroidissement = st.number_input(
                "Climatisation (conso_refroidissement_ef)",
                min_value=0.0,
                max_value=5000.0,
                value=0.0,
                step=50.0,
                help="Consommation pour la climatisation/refroidissement en kWh/an (0 si pas de clim)",
                key="api_refroid"
            )
        
        st.markdown("##### Coûts énergétiques")
        col1, col2 = st.columns(2)
        
        with col1:
            cout_ecs = st.number_input(
                "Coût annuel eau chaude (cout_ecs)",
                min_value=0.0,
                max_value=2000.0,
                value=300.0,
                step=10.0,
                help="Coût annuel pour l'eau chaude sanitaire en €/an",
                key="api_cout_ecs"
            )
        
        with col2:
            cout_eclairage = st.number_input(
                "Coût annuel éclairage (cout_eclairage)",
                min_value=0.0,
                max_value=500.0,
                value=80.0,
                step=5.0,
                help="Coût annuel pour l'éclairage en €/an",
                key="api_cout_eclairage"
            )
        
        # Calculer automatiquement
        conso_5_usages_ef = conso_5_usages_par_m2 * surface_habitable
        
        st.info(f" Consommation totale estimée : **{conso_5_usages_ef:,.0f} kWh/an**")
        
        st.markdown("---")
        
        # Afficher la requête JSON
        with st.expander("Voir la requête JSON qui sera envoyée"):
            request_data = {
                "conso_auxiliaires_ef": conso_auxiliaires,
                "cout_eclairage": cout_eclairage,
                "conso_5_usages_par_m2_ef": conso_5_usages_par_m2,
                "conso_5_usages_ef": conso_5_usages_ef,
                "surface_habitable_logement": surface_habitable,
                "cout_ecs": cout_ecs,
                "type_batiment": type_batiment,
                "conso_ecs_ef": conso_ecs,
                "conso_refroidissement_ef": conso_refroidissement,
                "type_energie_recodee": type_energie
            }
            st.json(request_data)
        
        # Bouton pour appeler l'API
        if st.button("Appeler l'API /predict", type="primary", use_container_width=True):
            with st.spinner("Appel de l'API en cours..."):
                try:
                    # Préparer les données
                    payload = {
                        "conso_auxiliaires_ef": float(conso_auxiliaires),
                        "cout_eclairage": float(cout_eclairage),
                        "conso_5_usages_par_m2_ef": float(conso_5_usages_par_m2),
                        "conso_5_usages_ef": float(conso_5_usages_ef),
                        "surface_habitable_logement": float(surface_habitable),
                        "cout_ecs": float(cout_ecs),
                        "type_batiment": type_batiment,
                        "conso_ecs_ef": float(conso_ecs),
                        "conso_refroidissement_ef": float(conso_refroidissement),
                        "type_energie_recodee": type_energie
                    }
                    
                    # Appeler l'API
                    response = requests.post(
                        f"{API_BASE_URL}/predict",
                        json=payload,
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        st.success(" Prédiction réussie !")
                        
                        st.markdown("---")
                        st.markdown("### Résultats")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            etiquette = result.get('etiquette_dpe', 'N/A')
                            colors_dpe = {
                                'A': '#00A550', 'B': '#52B153', 'C': '#C3D545',
                                'D': '#FFF033', 'E': '#F39200', 'F': '#ED2124', 'G': '#CC0033'
                            }
                            color = colors_dpe.get(etiquette, '#666')
                            
                            st.markdown(f"""
                            <div style="background: white; padding: 2rem; border-radius: 15px; 
                                        border-left: 8px solid {color}; text-align: center;
                                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                                <h3 style="color: {color}; margin: 0;">Étiquette DPE</h3>
                                <h1 style="font-size: 72px; margin: 1rem 0; color: {color};">{etiquette}</h1>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            cout = result.get('cout_total_5_usages', 0)
                            st.markdown(f"""
                            <div style="background: white; padding: 2rem; border-radius: 15px; 
                                        border-left: 8px solid #2E7D32; text-align: center;
                                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                                <h3 style="color: #2E7D32; margin: 0;">Coût annuel</h3>
                                <h1 style="font-size: 48px; margin: 1rem 0; color: #2E7D32;">{cout:,.0f} €</h1>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Probabilités
                        if result.get('probabilities'):
                            st.markdown("---")
                            st.markdown("#### Probabilités par classe")
                            
                            probas = result['probabilities']
                            classes = list(probas.keys())
                            values = [probas[c] * 100 for c in classes]
                            
                            fig = go.Figure(data=[
                                go.Bar(
                                    x=classes,
                                    y=values,
                                    marker_color=[colors_dpe.get(c, '#666') for c in classes],
                                    text=[f"{v:.1f}%" for v in values],
                                    textposition='outside'
                                )
                            ])
                            
                            fig.update_layout(
                                xaxis_title="Étiquette DPE",
                                yaxis_title="Probabilité (%)",
                                height=350,
                                showlegend=False
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                        
                        # Réponse JSON complète
                        with st.expander("Voir la réponse JSON complète"):
                            st.json(result)
                    
                    else:
                        st.error(f" Erreur API : {response.status_code}")
                        st.code(response.text)
                
                except requests.exceptions.Timeout:
                    st.error(" Timeout : L'API met trop de temps à répondre")
                except requests.exceptions.ConnectionError:
                    st.error(" Erreur de connexion : Vérifiez que l'API est bien lancée")
                except Exception as e:
                    st.error(f" Erreur : {e}")
    
    # TAB 3 : Métriques des Modèles
    with tab3:
        st.markdown("#### Métriques des Modèles (via API)")
        
        if st.button("Récupérer les métriques", type="primary"):
            with st.spinner("Récupération des métriques..."):
                try:
                    response = requests.get(f"{API_BASE_URL}/models/metrics", timeout=5)
                    
                    if response.status_code == 200:
                        metrics = response.json()
                        
                        st.success(" Métriques récupérées !")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("##### Classification (Étiquette DPE)")
                            
                            if 'classification' in metrics:
                                classif = metrics['classification']
                                
                                metric_col1, metric_col2 = st.columns(2)
                                with metric_col1:
                                    st.metric("Accuracy", f"{classif['accuracy']*100:.2f}%")
                                with metric_col2:
                                    st.metric("F1-Score", f"{classif['f1_score']:.3f}")
                                
                                st.info(f" Entraîné le : {classif.get('trained_at', 'N/A')[:10]}")
                                st.caption(f"Échantillons : {classif.get('train_samples', 'N/A'):,} (train) + {classif.get('test_samples', 'N/A'):,} (test)")
                                
                                # Classes disponibles
                                if 'classes' in classif:
                                    st.write("**Classes :**", ', '.join(classif['classes']))
                        
                        with col2:
                            st.markdown("##### Régression (Coût Total)")
                            
                            if 'regression' in metrics:
                                regress = metrics['regression']
                                
                                metric_col1, metric_col2 = st.columns(2)
                                with metric_col1:
                                    st.metric("R² Score", f"{regress['r2_score']:.3f}")
                                with metric_col2:
                                    st.metric("MAE", f"{regress['mae']:.0f} €")
                                
                                st.info(f" Entraîné le : {regress.get('trained_at', 'N/A')[:10]}")
                                st.caption(f"Échantillons : {regress.get('train_samples', 'N/A'):,} (train) + {regress.get('test_samples', 'N/A'):,} (test)")
                                
                                # RMSE
                                if 'rmse' in regress:
                                    st.write(f"**RMSE :** {regress['rmse']:.2f} €")
                        
                        # JSON complet
                        with st.expander("Voir la réponse JSON complète"):
                            st.json(metrics)
                    
                    elif response.status_code == 404:
                        st.warning(" Aucune métrique disponible. Les modèles n'ont peut-être pas encore été entraînés.")
                        st.info(" Utilisez la page 'Réentraîner modèles' pour créer les modèles.")
                    else:
                        st.error(f" Erreur : {response.status_code}")
                        st.code(response.text)
                
                except Exception as e:
                    st.error(f" Erreur : {e}")
    
    # TAB 4 : Liste des Endpoints
    with tab4:
        st.markdown("#### Tous les Endpoints disponibles")
        
        if st.button("Récupérer les infos de l'API"):
            try:
                response = requests.get(f"{API_BASE_URL}/", timeout=5)
                
                if response.status_code == 200:
                    api_info = response.json()
                    
                    st.json(api_info)
                    
                    if 'endpoints' in api_info:
                        st.markdown("---")
                        st.markdown("##### Endpoints")
                        
                        for name, path in api_info['endpoints'].items():
                            with st.expander(f"**{name}** : `{path}`"):
                                st.code(f"curl {API_BASE_URL}{path}", language="bash")
            except Exception as e:
                st.error(f" Erreur : {e}")
        
        st.markdown("---")
        st.markdown("##### Documentation détaillée")
        
        st.markdown(f"""
        Pour une documentation interactive complète avec possibilité de tester tous les endpoints :
        
         **[Ouvrir la documentation Swagger]({API_BASE_URL}/docs)**
        
         **[Ouvrir la documentation ReDoc]({API_BASE_URL}/redoc)**
        """)
    
    # TAB 5 : Exemples de Code
    with tab5:
        st.markdown("#### Exemples de Code")
        
        st.markdown("##### Python avec requests")
        st.code("""
import requests

# Configuration
API_URL = "http://localhost:8000"

# 1. Health Check
response = requests.get(f"{API_URL}/health")
print(response.json())

# 2. Prédiction individuelle
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

response = requests.post(f"{API_URL}/predict", json=data)
result = response.json()

print(f"Étiquette DPE: {result['etiquette_dpe']}")
print(f"Coût: {result['cout_total_5_usages']:.2f} €")

# 3. Récupérer les métriques
response = requests.get(f"{API_URL}/models/metrics")
metrics = response.json()
print(f"Accuracy: {metrics['classification']['accuracy']}")
""", language="python")
        
        st.markdown("---")
        

if __name__ == "__main__":
    show()