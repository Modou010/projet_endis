from pages.about import footer
import streamlit as st
from pages import welcome, home, analysis, about, enedis, prediction, api_interface, refresh_data, retrain_models

# --- Configuration de la page ---
st.set_page_config(
    page_title="GreenTech Solutions Rhône - Dashboard Énergétique",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Pages disponibles ---
PAGES = ["Accueil", "Contexte", "Analyse", "Enedis", "Prédiction", "API", "Refresh", "Train", "À propos"]
PAGE_TO_FUNC = {
    "Accueil": welcome.show,
    "Contexte": home.show,
    "Analyse": analysis.show,
    "Enedis": enedis.show,
    "Prédiction": prediction.show,
    "API": api_interface.show,
    "Refresh": refresh_data.show,
    "Train": retrain_models.show,
    "À propos": about.show,
}

# --- Lecture de la page depuis l'URL ---
qp = dict(st.query_params)
page = qp.get("page", "Accueil")
if page not in PAGES:
    page = "Accueil"

# --- CSS global ---
st.markdown("""
<style>
/* --- Conteneur principal --- */
.block-container {
  max-width: 1200px;
  margin: 0 auto;
  background-color: #F7FCF7;
}

/* --- Barre de navigation --- */
.navbar {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  background-color: #1b5e20;
  padding: 10px 12px;
  border-radius: 10px;
  margin: 20px 0 28px 0;
  gap: 8px;
}

/* --- Lien de navigation --- */
.nav-item {
  color: #ffffff !important;
  text-decoration: none !important;
  padding: 10px 22px;
  font-size: 17px;
  font-weight: 500;
  border-radius: 8px;
  transition: background 0.25s ease;
  line-height: 1.5;
  display: inline-block;
  vertical-align: middle;
}

.nav-item:hover {
  background-color: #388e3c;
  color: #ffffff !important;
}

/* --- Page active --- */
.nav-item.active {
  background-color: #66bb6a;
  font-weight: 600;
}

/* --- Sous-menu déroulant --- */
.dropdown {
  position: relative;
  display: inline-block;
  vertical-align: middle;
}

/* Augmenter la zone cliquable */
.dropdown::after {
  content: "";
  position: absolute;
  bottom: -8px;
  left: 0;
  right: 0;
  height: 8px;
}

.dropdown .dropbtn {
  display: inline-block;
  vertical-align: middle;
}

.dropbtn::after {
  content: " ▼";
  font-size: 0.7em;
  margin-left: 4px;
  vertical-align: middle;
}

/* --- Contenu du sous-menu --- */
.dropdown-content {
  display: none;
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  background-color: #e8f5e9;
  min-width: 180px;
  box-shadow: 0px 8px 16px rgba(0,0,0,0.2);
  border-radius: 8px;
  z-index: 10;
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 0.3s ease, transform 0.3s ease;
  padding: 8px 0;
}

/* Zone de transition invisible pour faciliter le passage */
.dropdown-content::before {
  content: "";
  position: absolute;
  top: -8px;
  left: 0;
  right: 0;
  height: 8px;
}

.dropdown-content a {
  color: #1b5e20;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
  font-size: 15px;
  border-radius: 6px;
  white-space: nowrap;
  margin: 2px 8px;
}

.dropdown-content a:hover {
  background-color: #c8e6c9;
}

/* --- Afficher le menu au survol --- */
.dropdown:hover .dropdown-content {
  display: block;
  opacity: 1;
  transform: translateY(0);
}

/* --- Survol du bouton parent --- */
.dropdown:hover .dropbtn {
  background-color: #388e3c;
  color: #fff !important;
}

/* --- Version mobile --- */
@media (max-width: 768px) {
  .nav-item, .dropbtn {
    width: 100%;
    text-align: center;
    font-size: 16px;
    padding: 10px 18px;
  }
  .dropdown-content {
    position: static;
    box-shadow: none;
    background-color: #2e7d32;
  }
  .dropdown-content a {
    color: white;
  }
  .dropdown-content a:hover {
    background-color: #66bb6a;
  }
}
</style>
""", unsafe_allow_html=True)

# --- Navbar avec sous-menu ---
nav_html = f"""
<nav class="navbar">
  <a class="nav-item {'active' if page == 'Accueil' else ''}" href="?page=Accueil" target="_self">Accueil</a>
  <a class="nav-item {'active' if page == 'Contexte' else ''}" href="?page=Contexte" target="_self">Contexte</a>
  <div class="dropdown">
    <a class="nav-item dropbtn {'active' if page in ['Analyse', 'Enedis'] else ''}" href="?page=Analyse" target="_self">Analyse</a>
    <div class="dropdown-content">
      <a href="?page=Analyse" target="_self">Vue générale</a>
      <a href="?page=Enedis" target="_self">Données Enedis</a>
    </div>
  </div>
  <a class="nav-item {'active' if page == 'Prédiction' else ''}" href="?page=Prédiction" target="_self">Prédiction</a>
  <div class="dropdown">
    <a class="nav-item dropbtn {'active' if page in ['Refresh', 'Train'] else ''}" href="?page=Refresh" target="_self">Update</a>
    <div class="dropdown-content">
      <a href="?page=Refresh" target="_self">Actualiser données</a>
      <a href="?page=Train" target="_self">Réentraîner modèle</a>
    </div>
  </div>
  <a class="nav-item {'active' if page == 'API' else ''}" href="?page=API" target="_self">API</a>
  <a class="nav-item {'active' if page == 'À propos' else ''}" href="?page=À propos" target="_self">À propos</a>
</nav>
"""

st.markdown(nav_html, unsafe_allow_html=True)

# --- Synchroniser l'URL ---
st.query_params["page"] = page

# --- Afficher la page sélectionnée ---
PAGE_TO_FUNC[page]()

# --- Pied de page ---
footer()