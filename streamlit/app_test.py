import streamlit as st
from pages import welcome, home, analysis, compare, about, enedis, prediction, refresh_data, retrain_models

# Configuration de la page
st.set_page_config(
    page_title="GreenTech Solutions Rhône - Dashboard Énergétique",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour un design moderne
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8f5e9 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8f5e9 100%);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2d5016 0%, #1b5e20 100%);
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: bold;
    }
    .st-emotion-cache-16idsys p {
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# Barre latérale avec style
with st.sidebar:
    st.markdown("# 🌱 GreenTech Solutions")
    st.markdown("### Rhône-Alpes")
    st.markdown("---")
    
    # Section principale
    st.markdown("### 📊 Navigation")
    page = st.radio(
        "Pages",
        [
            "🏠 Accueil",
            "📊 Tableau de bord",
            "📈 Analyse",
            "⚡ Enedis",
            "🔮 Prédiction",
            "⚖️ Comparer"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Section Administration/ML
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
    
    st.markdown("---")
    
    # Section À propos
    st.markdown("### ℹ️ Informations")
    if st.button("À propos", use_container_width=True):
        page = "ℹ️ À propos"
    
    st.markdown("---")
    st.markdown("### 📡 API")
    st.markdown("L'API REST est accessible sur le port **8000**")
    st.caption("Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)")
    
    st.markdown("---")
    st.caption("Application d'analyse énergétique basée sur les données DPE et Enedis de la région Rhône.")
    st.caption("Version 1.0.0")

# Affichage des pages principales
if ml_page != "Aucune":
    # Priorité aux pages ML si sélectionnées
    if ml_page == "🔄 Rafraîchir données":
        refresh_data.show()
    elif ml_page == "🎯 Réentraîner modèles":
        retrain_models.show()
else:
    # Pages normales
    if page == "🏠 Accueil":
        welcome.show()
    elif page == "📊 Tableau de bord":
        home.show()
    elif page == "📈 Analyse":
        analysis.show()
    elif page == "⚡ Enedis":
        enedis.show()
    elif page == "🔮 Prédiction":
        prediction.show()
    elif page == "⚖️ Comparer":
        compare.show()
    elif page == "ℹ️ À propos":
        about.show()

#-------------------------------------------------------------------------
import streamlit as st
from pages import welcome, home, analysis, compare, about, enedis, prediction

# Configuration de la page
st.set_page_config(
    page_title="GreenTech Solutions Rhône - Dashboard Énergétique",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour un design moderne
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8f5e9 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8f5e9 100%);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2d5016 0%, #1b5e20 100%);
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: bold;
    }
    .st-emotion-cache-16idsys p {
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# Barre latérale avec style
with st.sidebar:
    st.markdown("# 🌱 GreenTech Solutions")
    st.markdown("### Rhône-Alpes")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["🏠 Accueil", "📊 Tableau de bord", "📈 Analyse", "⚡ Enedis", "🔮 Prédiction", "⚖️ Comparer", "ℹ️ À propos"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### À propos")
    st.markdown("Application d'analyse énergétique basée sur les données DPE et Enedis de la région Rhône.")

# Affichage des pages
if page == "🏠 Accueil":
    welcome.show()
elif page == "📊 Tableau de bord":
    home.show()
elif page == "📈 Analyse":
    analysis.show()
elif page == "⚡ Enedis":
    enedis.show()
elif page == "🔮 Prédiction":
    prediction.show()
elif page == "⚖️ Comparer":
    compare.show()
elif page == "ℹ️ À propos":
    about.show()