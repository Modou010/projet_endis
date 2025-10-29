import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

def show():
    # Bandeau principal avec image de fond
    image_path = "assets/eco_vision.jpg"
    
    if os.path.exists(image_path):
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(rgba(46, 125, 50, 0.85), rgba(27, 94, 32, 0.85)),
                            url('{image_path}');
                background-size: cover;
                background-position: center;
                padding: 4rem 2rem;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                margin-bottom: 2rem;
            ">
                <h1 style="color:white; font-size:52px; margin-bottom: 1rem;">
                    🌱 Bienvenue sur GreenTech Solutions Rhône
                </h1>
                <p style="color:white; font-size:22px; opacity: 0.95;">
                    Analyse et comparaison énergétique simplifiée pour vos logements
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style="
                background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%);
                padding: 4rem 2rem;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                margin-bottom: 2rem;
            ">
                <h1 style="color:white; font-size:52px; margin-bottom: 1rem;">
                    🌱 Bienvenue sur GreenTech Solutions Rhône
                </h1>
                <p style="color:white; font-size:22px; opacity: 0.95;">
                    Analyse et comparaison énergétique simplifiée pour vos logements
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # KPIs principaux
    try:
        df = pd.read_csv("data/donnees_ademe_finales_nettoyees_69_final_pret.csv")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="🏠 Logements analysés",
                value=f"{len(df):,}",
                delta="Base de données complète"
            )
        
        with col2:
            conso_moy = df['conso_5_usages_par_m2_ef'].mean()
            st.metric(
                label="⚡ Consommation moyenne",
                value=f"{conso_moy:.0f} kWh/m²",
                delta=f"{conso_moy - 180:.0f} vs. objectif"
            )
        
        with col3:
            cout_moy = df['cout_total_5_usages'].mean()
            st.metric(
                label="💰 Coût moyen annuel",
                value=f"{cout_moy:,.0f} €",
                delta="Par logement"
            )
        
        with col4:
            ges_moy = df['emission_ges_5_usages'].mean()
            st.metric(
                label="🌍 Émissions GES moy.",
                value=f"{ges_moy:,.0f} kg CO₂",
                delta="Par an"
            )
        
        st.markdown("---")
        
        # Graphiques en colonnes
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Répartition des étiquettes DPE")
            etiquette_counts = df['etiquette_dpe'].value_counts().sort_index()
            
            colors_dpe = {
                'A': '#00A550', 'B': '#52B153', 'C': '#C3D545',
                'D': '#FFF033', 'E': '#F39200', 'F': '#ED2124', 'G': '#CC0033'
            }
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=etiquette_counts.index,
                values=etiquette_counts.values,
                marker=dict(colors=[colors_dpe.get(x, '#666') for x in etiquette_counts.index]),
                textinfo='label+percent',
                textfont_size=14,
                hole=0.3
            )])
            
            fig_pie.update_layout(
                showlegend=True,
                height=350,
                margin=dict(t=0, b=0, l=0, r=0)
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.markdown("### ⚡ Consommation par type d'énergie")
            
            energie_stats = df.groupby('type_energie_recodee').agg({
                'conso_5_usages_par_m2_ef': 'mean',
                'cout_total_5_usages': 'mean'
            }).reset_index()
            
            energie_stats = energie_stats.nlargest(5, 'conso_5_usages_par_m2_ef')
            
            fig_bar = go.Figure(data=[
                go.Bar(
                    x=energie_stats['type_energie_recodee'],
                    y=energie_stats['conso_5_usages_par_m2_ef'],
                    marker_color='#6B8E23',
                    text=energie_stats['conso_5_usages_par_m2_ef'].round(0),
                    textposition='outside'
                )
            ])
            
            fig_bar.update_layout(
                yaxis_title="Consommation moyenne (kWh/m²)",
                xaxis_title="Type d'énergie",
                height=350,
                showlegend=False,
                margin=dict(t=20, b=0, l=0, r=0)
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
        
    except FileNotFoundError:
        st.warning("⚠️ Fichier de données introuvable. Utilisation des données de démonstration.")
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")

    st.markdown("---")

    # Fonctionnalités
    st.markdown("### 🎯 Fonctionnalités de l'application")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #6B8E23; margin-bottom: 1rem;">
            <h4>📈 Tableau de bord interactif</h4>
            <p>Visualisez et filtrez les données en temps réel par type de bâtiment, code postal et étiquette DPE</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #2E8B57;">
            <h4>🔍 Analyse approfondie</h4>
            <p>Graphiques détaillés des consommations par zone géographique et type d'énergie</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #FF9800; margin-bottom: 1rem;">
            <h4>⚖️ Comparaison</h4>
            <p>Comparez deux logements côte à côte pour identifier les économies potentielles</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #9C27B0;">
            <h4>🔮 Prédiction IA (à venir)</h4>
            <p>Estimez l'étiquette DPE et les coûts énergétiques d'un logement grâce au machine learning</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    st.info("💡 **Astuce** : Utilisez le menu de navigation à gauche pour explorer les différentes sections de l'application !")