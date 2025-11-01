import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pages.analysis import load_data
from pages.about import footer


def show():
    st.title(" Données Enedis - Consommation électrique")
    st.markdown("### Analyse complémentaire des données de consommation électrique")
    
    try:
        # Charger les données
        df_enedis = load_data("data/donnees_enedis_finales_69.csv")
        
        # Convertir les codes postaux en string et formater correctement
        # Gérer les valeurs manquantes d'abord
        df_enedis['code_postal'] = df_enedis['code_postal'].fillna(0).astype(int).astype(str).str.zfill(5)
        # Remplacer '00000' par 'Inconnu' si nécessaire
        df_enedis.loc[df_enedis['code_postal'] == '00000', 'code_postal'] = 'Inconnu'
        
        # Afficher les années disponibles
        annees_dispo = sorted(df_enedis['Année'].unique())
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(" Années disponibles", f"{min(annees_dispo)} - {max(annees_dispo)}")
        with col2:
            st.metric(" Adresses", f"{df_enedis['adresse_norm'].nunique():,}")
        with col3:
            total_logements = df_enedis['Nombre de logements'].sum()
            st.metric(" Total logements", f"{int(total_logements):,}")
        
        st.markdown("---")
        
        # Filtres
        st.markdown("####  Filtres")
        col1, col2 = st.columns(2)
        
        with col1:
            annee_selectionnee = st.selectbox(
                "Année",
                options=annees_dispo,
                index=len(annees_dispo)-1
            )
        
        with col2:
            codes_postaux = sorted(df_enedis['code_postal'].unique())
            cp_selected = st.multiselect(
                "Codes postaux",
                options=codes_postaux,
                default=codes_postaux[:5] if len(codes_postaux) > 5 else codes_postaux
            )
        
        # Filtrer les données
        df_filtered = df_enedis[
            (df_enedis['Année'] == annee_selectionnee) &
            (df_enedis['code_postal'].isin(cp_selected))
        ]
        
        st.markdown("---")
        
        # Onglets
        tab1, tab2, tab3, tab4 = st.tabs([
            " Vue d'ensemble",
            " Carte interactive",
            " Analyses comparatives",
            " Données détaillées"
        ])
        st.markdown("""
<style>
/* Conteneur global des tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

/* Style général des onglets */
.stTabs [data-baseweb="tab"] {
    background-color: #e8f5e9;   /* vert clair */
    color: #1b5e20;              /* texte vert foncé */
    border-radius: 6px 6px 0 0;
    padding: 8px 16px;
    font-weight: 500;
    font-size: 15px;
    border: none !important;
    transition: all 0.3s ease;
    border-bottom: 3px solid transparent !important; /* 🔥 enlève la barre orange */
}

/*  Onglet actif — même couleur que la navbar */
.stTabs [aria-selected="true"] {
    background-color: #1b5e20 !important;  /* vert foncé */
    color: white !important;
    font-weight: 600;
    border: none !important;
    border-bottom: 3px solid #1b5e20 !important;  /* barre verte discrète */
}

/*  Hover — reste vert, pas d’orange */
.stTabs [data-baseweb="tab"]:hover {
    background-color: #2e7d32 !important;  /* vert moyen */
    color: white !important;
    border-bottom: 3px solid #e8f5e9 !important;
}
</style>
""", unsafe_allow_html=True)

        
        # TAB 1 : Vue d'ensemble
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Distribution de la consommation par logement")
                
                fig_hist = px.histogram(
                    df_filtered,
                    x='Consommation annuelle moyenne par logement de l\'adresse (MWh)',
                    nbins=30,
                    labels={'x': 'Consommation (MWh/logement)'},
                    color_discrete_sequence=['#FF6B6B']
                )
                
                fig_hist.update_layout(
                    showlegend=False,
                    height=350,
                    yaxis_title="Nombre d'adresses"
                )
                
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with col2:
                st.markdown("#### Nombre de logements par adresse")
                
                # Créer des catégories
                df_filtered['categorie_logements'] = pd.cut(
                    df_filtered['Nombre de logements'],
                    bins=[0, 5, 10, 20, 50, 1000],
                    labels=['1-5', '6-10', '11-20', '21-50', '50+']
                )
                
                cat_counts = df_filtered['categorie_logements'].value_counts().sort_index()
                
                fig_cat = px.bar(
                    x=cat_counts.index,
                    y=cat_counts.values,
                    labels={'x': 'Nombre de logements', 'y': 'Nombre d\'adresses'},
                    color=cat_counts.values,
                    color_continuous_scale='Viridis'
                )
                
                fig_cat.update_layout(
                    showlegend=False,
                    height=350
                )
                
                st.plotly_chart(fig_cat, use_container_width=True)
            
            # Statistiques par commune
            st.markdown("####  Top 10 communes par consommation totale")
            
            commune_stats = df_filtered.groupby('code_postal').agg({
                'Consommation annuelle totale de l\'adresse (MWh)': 'sum',
                'Nombre de logements': 'sum',
                'Consommation annuelle moyenne de la commune (MWh)': 'first'
            }).reset_index()
            
            commune_stats.columns = ['Code Postal', 'Conso totale (MWh)', 'Nb logements', 'Conso moy commune']
            commune_stats = commune_stats.nlargest(10, 'Conso totale (MWh)')
            
            # S'assurer que Code Postal est en string
            commune_stats['Code Postal'] = commune_stats['Code Postal'].astype(str)
            
            fig_communes = px.bar(
                commune_stats,
                x='Code Postal',
                y='Conso totale (MWh)',
                color='Nb logements',
                text='Conso totale (MWh)',
                color_continuous_scale='Oranges'
            )
            
            fig_communes.update_traces(texttemplate='%{text:.0f}', textposition='outside')
            fig_communes.update_layout(height=400)
            
            st.plotly_chart(fig_communes, use_container_width=True)
        
        # TAB 2 : Carte interactive
        with tab2:
            st.markdown("####  Répartition géographique des consommations")
            
            if 'latitude' in df_filtered.columns and 'longitude' in df_filtered.columns:
                # Limiter pour performance
                df_map = df_filtered.sample(min(500, len(df_filtered)))
                
                fig_map = px.scatter_mapbox(
                    df_map,
                    lat='latitude',
                    lon='longitude',
                    zoom=10,
                    size='Nombre de logements',
                    color='Consommation annuelle moyenne par logement de l\'adresse (MWh)',
                    hover_name='adresse_norm',
                    hover_data={
                        'Nombre de logements': True,
                        'Consommation annuelle totale de l\'adresse (MWh)': ':.2f',
                        'latitude': False,
                        'longitude': False
                    },
                    color_continuous_scale='Reds',
                    #zoom=5,
                    height=600
                )
                
                fig_map.update_layout(
                    mapbox_style="open-street-map",
                    margin={"r":0,"t":0,"l":0,"b":0}
                )
                
                st.plotly_chart(fig_map, use_container_width=True)
                
                st.info(f" Carte limitée à {len(df_map)} adresses pour la performance. Taille des bulles = nombre de logements, couleur = consommation moyenne.")
            else:
                st.warning("Données de géolocalisation non disponibles.")
        
        # TAB 3 : Analyses comparatives
        with tab3:
            st.markdown("####  Analyses comparatives")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### Relation taille/consommation")
                
                # Scatter plot : nb logements vs conso moyenne
                fig_scatter = px.scatter(
                    df_filtered.sample(min(300, len(df_filtered))),
                    x='Nombre de logements',
                    y='Consommation annuelle moyenne par logement de l\'adresse (MWh)',
                    color='code_postal',
                    opacity=0.6,
                    trendline="lowess",
                    labels={
                        'Nombre de logements': 'Nombre de logements à l\'adresse',
                        'Consommation annuelle moyenne par logement de l\'adresse (MWh)': 'Conso moy (MWh)'
                    }
                )
                
                fig_scatter.update_layout(height=400)
                st.plotly_chart(fig_scatter, use_container_width=True)
            
            with col2:
                st.markdown("##### Boxplot par code postal")
                
                # S'assurer que code_postal est en string pour l'affichage
                df_filtered_plot = df_filtered.copy()
                df_filtered_plot['code_postal_display'] = df_filtered_plot['code_postal'].astype(str)
                
                fig_box = px.box(
                    df_filtered_plot,
                    x='code_postal_display',
                    y='Consommation annuelle moyenne par logement de l\'adresse (MWh)',
                    color='code_postal_display',
                    labels={
                        'code_postal_display': 'Code Postal',
                        'Consommation annuelle moyenne par logement de l\'adresse (MWh)': 'Conso (MWh)'
                    }
                )
                
                fig_box.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig_box, use_container_width=True)
            
            # Evolution temporelle si plusieurs années
            if len(annees_dispo) > 1:
                st.markdown("#####  Évolution temporelle de la consommation")
                
                evolution = df_enedis[
                    df_enedis['code_postal'].isin(cp_selected)
                ].groupby('Année').agg({
                    'Consommation annuelle moyenne par logement de l\'adresse (MWh)': 'mean',
                    'Nombre de logements': 'sum'
                }).reset_index()
                
                fig_evol = make_subplots(specs=[[{"secondary_y": True}]])
                
                fig_evol.add_trace(
                    go.Scatter(
                        x=evolution['Année'],
                        y=evolution['Consommation annuelle moyenne par logement de l\'adresse (MWh)'],
                        name="Conso moyenne (MWh)",
                        line=dict(color='#FF6B6B', width=3)
                    ),
                    secondary_y=False
                )
                
                fig_evol.add_trace(
                    go.Bar(
                        x=evolution['Année'],
                        y=evolution['Nombre de logements'],
                        name="Nb logements",
                        marker_color='#4ECDC4',
                        opacity=0.6
                    ),
                    secondary_y=True
                )
                
                fig_evol.update_xaxes(title_text="Année")
                fig_evol.update_yaxes(title_text="Consommation moyenne (MWh)", secondary_y=False)
                fig_evol.update_yaxes(title_text="Nombre de logements", secondary_y=True)
                fig_evol.update_layout(height=400)
                
                st.plotly_chart(fig_evol, use_container_width=True)
        
        # TAB 4 : Données détaillées
        with tab4:
            st.markdown("####  Tableau des données")
            
            # Renommer les colonnes pour affichage
            df_display = df_filtered[[
                'adresse_norm', 'code_postal', 'Nombre de logements',
                'Consommation annuelle totale de l\'adresse (MWh)',
                'Consommation annuelle moyenne par logement de l\'adresse (MWh)',
                'Consommation annuelle moyenne de la commune (MWh)',
                'score'
            ]].copy()
            
            df_display.columns = [
                'Adresse', 'Code Postal', 'Nb logements',
                'Conso totale (MWh)', 'Conso moy/logement (MWh)',
                'Conso moy commune (MWh)', 'Score géocodage'
            ]
            
            # Arrondir
            for col in df_display.select_dtypes(include=['float64']).columns:
                df_display[col] = df_display[col].round(2)
            
            st.dataframe(df_display, use_container_width=True, height=400)
            
            # Téléchargement
            col1, col2 = st.columns([3, 1])
            with col2:
                csv = df_filtered.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=" Télécharger CSV",
                    data=csv,
                    file_name=f"enedis_{annee_selectionnee}.csv",
                    mime="text/csv"
                )
        
        st.markdown("---")
        
        # Insights
        st.markdown("###  Insights clés")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            conso_max = df_filtered['Consommation annuelle moyenne par logement de l\'adresse (MWh)'].max()
            st.info(f" **Conso max** : {conso_max:.2f} MWh/logement")
        
        with col2:
            nb_max = df_filtered['Nombre de logements'].max()
            st.info(f" **Plus grande adresse** : {int(nb_max)} logements")
        
        with col3:
            conso_totale = df_filtered['Consommation annuelle totale de l\'adresse (MWh)'].sum()
            st.info(f" **Conso totale zone** : {conso_totale:,.0f} MWh")
        
    except FileNotFoundError:
        st.error(" Le fichier des données Enedis est introuvable.")
        st.info("  Placez le fichier dans `data/donnees_enedis.csv`")
    except Exception as e:
        st.error(f"Une erreur s'est produite : {e}")
        import traceback
        st.code(traceback.format_exc())
    
