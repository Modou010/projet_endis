import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_data(path: str = "data/donnees_ademe_finales_nettoyees_69_final_pret.csv") -> pd.DataFrame:
    """Charge le fichier CSV et le met en cache."""
    if not os.path.exists(path):
        st.error(f"❌ Fichier introuvable : {path}")
        return pd.DataFrame()
    try:
        df = pd.read_csv(path)
        st.success(f"✅ Données chargées ({len(df)} lignes, {len(df.columns)} colonnes)")
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier : {e}")
        return pd.DataFrame()
