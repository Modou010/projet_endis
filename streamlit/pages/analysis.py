import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
def show():
    st.title("📊 Analyse approfondie des données")
    st.markdown("### Visualisations et insights énergétiques")

    try:
        df = pd.read_csv("data/donnees_ademe_finales_nettoyees_69_final_pret.csv")
        
        # Onglets pour organiser les analyses
        tab1, tab2, tab3, tab4 = st.tabs([
            "💰 Analyse des coûts",
            "⚡ Consommation énergétique",
            "🌍 Émissions GES",
            "🗺️ Analyse géographique"
        ])
        
        # TAB 1: Analyse des coûts
        with tab1:
            st.markdown("#### Comparaison des coûts par type d'énergie")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Coût moyen par type d'énergie
                energie_cout = df.groupby('type_energie_recodee')['cout_total_5_usages'].mean().sort_values(ascending=False).head(10)
                
                fig_cout = go.Figure(data=[
                    go.Bar(
                        x=energie_cout.values,
                        y=energie_cout.index,
                        orientation='h',
                        marker=dict(
                            color=energie_cout.values,
                            colorscale='Reds',
                            showscale=True,
                            colorbar=dict(title="Coût (€)")
                        ),
                        text=energie_cout.values.round(0),
                        textposition='outside'
                    )
                ])
                
                fig_cout.update_layout(
                    title="Coût moyen annuel par type d'énergie",
                    xaxis_title="Coût (€)",
                    yaxis_title="Type d'énergie",
                    height=400
                )
                
                st.plotly_chart(fig_cout, use_container_width=True)
            
            with col2:
                # Distribution des coûts par étiquette
                fig_box = px.box(
                    df,
                    x='etiquette_dpe',
                    y='cout_total_5_usages',
                    color='etiquette_dpe',
                    color_discrete_map={
                        'A': '#00A550', 'B': '#52B153', 'C': '#C3D545',
                        'D': '#FFF033', 'E': '#F39200', 'F': '#ED2124', 'G': '#CC0033'
                    },
                    labels={'cout_total_5_usages': 'Coût annuel (€)', 'etiquette_dpe': 'Étiquette DPE'}
                )
                
                fig_box.update_layout(
                    title="Distribution des coûts par étiquette DPE",
                    showlegend=False,
                    height=400
                )
                
                st.plotly_chart(fig_box, use_container_width=True)
            
            # Tableau récapitulatif
            st.markdown("#### 📋 Statistiques par étiquette DPE")
            stats_etiquette = df.groupby('etiquette_dpe').agg({
                'cout_total_5_usages': ['mean', 'min', 'max'],
                'type_batiment': 'count'
            }).round(0)
            
            stats_etiquette.columns = ['Coût moyen (€)', 'Coût min (€)', 'Coût max (€)', 'Nombre']
            st.dataframe(stats_etiquette, use_container_width=True)
        
        # TAB 2: Consommation énergétique
        with tab2:
            st.markdown("#### Analyse de la consommation énergétique")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Consommation par m² selon le type de bâtiment
                type_conso = df.groupby('type_batiment')['conso_5_usages_par_m2_ef'].mean().sort_values(ascending=False)
                
                fig_type = px.bar(
                    x=type_conso.index,
                    y=type_conso.values,
                    labels={'x': 'Type de bâtiment', 'y': 'Consommation (kWh/m²)'},
                    color=type_conso.values,
                    color_continuous_scale='Greens'
                )
                
                fig_type.update_layout(
                    title="Consommation moyenne par type de bâtiment",
                    showlegend=False,
                    height=400
                )
                
                st.plotly_chart(fig_type, use_container_width=True)
            
            with col2:
                # Scatter plot: Surface vs Consommation
                fig_scatter = px.scatter(
                    df.sample(min(1000, len(df))),  # Limiter à 1000 points pour la performance
                    x='surface_habitable_logement',
                    y='conso_5_usages_ef',
                    color='etiquette_dpe',
                    color_discrete_map={
                        'A': '#00A550', 'B': '#52B153', 'C': '#C3D545',
                        'D': '#FFF033', 'E': '#F39200', 'F': '#ED2124', 'G': '#CC0033'
                    },
                    labels={
                        'surface_habitable_logement': 'Surface habitable (m²)',
                        'conso_5_usages_ef': 'Consommation totale (kWh)',
                        'etiquette_dpe': 'Étiquette'
                    },
                    opacity=0.6
                )
                
                fig_scatter.update_layout(
                    title="Relation Surface / Consommation",
                    height=400
                )
                
                st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Breakdown par usage
            st.markdown("#### Détail des consommations par poste")
            
            # Calculer les moyennes pour chaque usage
            usages = {
                'ECS': df['conso_ecs_ef'].mean(),
                'Auxiliaires': df['conso_auxiliaires_ef'].mean(),
                'Refroidissement': df['conso_refroidissement_ef'].mean()
            }
            
            fig_usages = go.Figure(data=[
                go.Bar(
                    x=list(usages.keys()),
                    y=list(usages.values()),
                    marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1'],
                    text=[f"{v:.0f}" for v in usages.values()],
                    textposition='outside'
                )
            ])
            
            fig_usages.update_layout(
                title="Consommation moyenne par poste (kWh)",
                xaxis_title="Poste de consommation",
                yaxis_title="Consommation (kWh)",
                height=350
            )
            
            st.plotly_chart(fig_usages, use_container_width=True)
        
        # TAB 3: Émissions GES
        with tab3:
            st.markdown("#### Impact environnemental")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # GES par type d'énergie
                ges_energie = df.groupby('type_energie_recodee')['emission_ges_5_usages'].mean().sort_values(ascending=False).head(10)
                
                fig_ges = px.bar(
                    x=ges_energie.index,
                    y=ges_energie.values,
                    labels={'x': "Type d'énergie", 'y': 'Émissions (kg CO₂)'},
                    color=ges_energie.values,
                    color_continuous_scale='Reds'
                )
                
                fig_ges.update_layout(
                    title="Émissions moyennes de GES par type d'énergie",
                    xaxis_tickangle=-45,
                    height=400
                )
                
                st.plotly_chart(fig_ges, use_container_width=True)
            
            with col2:
                # Relation Consommation / GES
                sample_df = df.sample(min(500, len(df)))
                
                fig_scatter_ges = px.scatter(
                    sample_df,
                    x='conso_5_usages_par_m2_ef',
                    y='emission_ges_5_usages',
                    color='type_energie_recodee',
                    labels={
                        'conso_5_usages_par_m2_ef': 'Consommation (kWh/m²)',
                        'emission_ges_5_usages': 'Émissions GES (kg CO₂)',
                        'type_energie_recodee': 'Énergie'
                    },
                    opacity=0.6
                )
                
                fig_scatter_ges.update_layout(
                    title="Relation Consommation / Émissions GES",
                    height=400
                )
                
                st.plotly_chart(fig_scatter_ges, use_container_width=True)
            
            # Comparaison GES par étiquette
            st.markdown("#### Émissions GES par étiquette DPE")
            
            ges_etiquette = df.groupby('etiquette_dpe')['emission_ges_5_usages'].mean().sort_index()
            
            fig_ges_etiq = go.Figure(data=[
                go.Bar(
                    x=ges_etiquette.index,
                    y=ges_etiquette.values,
                    marker=dict(
                        color=['#00A550', '#52B153', '#C3D545', '#FFF033', '#F39200', '#ED2124', '#CC0033']
                    ),
                    text=ges_etiquette.values.round(0),
                    textposition='outside'
                )
            ])
            
            fig_ges_etiq.update_layout(
                xaxis_title="Étiquette DPE",
                yaxis_title="Émissions moyennes (kg CO₂)",
                height=350,
                showlegend=False
            )
            
            st.plotly_chart(fig_ges_etiq, use_container_width=True)
        
        # TAB 4: Analyse géographique
        with tab4:
            st.markdown("#### Distribution géographique des logements")
            
            # Vérifier si les données de localisation existent
            if 'latitude' in df.columns and 'longitude' in df.columns:
                # Filtrer les données avec coordonnées valides
                df_map = df.dropna(subset=['latitude', 'longitude'])
                
                if len(df_map) > 0:
                    # Limiter le nombre de points pour la performance
                    df_map_sample = df_map.sample(min(1000, len(df_map)))
                    
                    fig_map = px.scatter_mapbox(
                        df_map_sample,
                        lat='latitude',
                        lon='longitude',
                        color='etiquette_dpe',
                        color_discrete_map={
                            'A': '#00A550', 'B': '#52B153', 'C': '#C3D545',
                            'D': '#FFF033', 'E': '#F39200', 'F': '#ED2124', 'G': '#CC0033'
                        },
                        size='surface_habitable_logement',
                        hover_data=['type_batiment', 'cout_total_5_usages', 'conso_5_usages_par_m2_ef'],
                        zoom=9,
                        height=500
                    )
                    
                    fig_map.update_layout(
                        mapbox_style="open-street-map",
                        margin={"r":0,"t":0,"l":0,"b":0}
                    )
                    
                    st.plotly_chart(fig_map, use_container_width=True)
                else:
                    st.warning("Aucune donnée de géolocalisation disponible.")
            
            # Analyse par code postal
            st.markdown("#### Analyse par code postal")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Top 10 codes postaux par nombre de logements
                cp_counts = df['code_postal_ban'].value_counts().head(10)
                
                fig_cp = px.bar(
                    x=cp_counts.values,
                    y=cp_counts.index.astype(str),
                    orientation='h',
                    labels={'x': 'Nombre de logements', 'y': 'Code postal'},
                    color=cp_counts.values,
                    color_continuous_scale='Blues'
                )
                
                fig_cp.update_layout(
                    title="Top 10 codes postaux",
                    showlegend=False,
                    height=400
                )
                
                st.plotly_chart(fig_cp, use_container_width=True)
            
            with col2:
                # Consommation moyenne par code postal
                cp_conso = df.groupby('code_postal_ban')['conso_5_usages_par_m2_ef'].mean().sort_values(ascending=False).head(10)
                
                fig_cp_conso = px.bar(
                    x=cp_conso.values,
                    y=cp_conso.index.astype(str),
                    orientation='h',
                    labels={'x': 'Consommation (kWh/m²)', 'y': 'Code postal'},
                    color=cp_conso.values,
                    color_continuous_scale='Oranges'
                )
                
                fig_cp_conso.update_layout(
                    title="Top 10 CP par consommation",
                    showlegend=False,
                    height=400
                )
                
                st.plotly_chart(fig_cp_conso, use_container_width=True)
        
        st.markdown("---")
        
        # Section insights
        st.markdown("### 💡 Insights clés")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            energie_la_plus_chere = df.groupby('type_energie_recodee')['cout_total_5_usages'].mean().idxmax()
            st.info(f"🔥 **Énergie la plus coûteuse** : {energie_la_plus_chere}")
        
        with col2:
            etiquette_la_plus_commune = df['etiquette_dpe'].mode()[0]
            pct = (df['etiquette_dpe'].value_counts()[etiquette_la_plus_commune] / len(df)) * 100
            st.info(f"📊 **Étiquette la plus commune** : {etiquette_la_plus_commune} ({pct:.1f}%)")
        
        with col3:
            surface_moy = df['surface_habitable_logement'].mean()
            st.info(f"📏 **Surface moyenne** : {surface_moy:.1f} m²")
        
    except FileNotFoundError:
        st.error("❌ Le fichier de données est introuvable.")
        st.info("📂 Assurez-vous que `data/donnees_ademe_finales_nettoyees_69_final_pret.csv` existe.")
    except KeyError as e:
        st.error(f"❌ Colonne manquante dans les données : {e}")
        st.info("Certaines colonnes attendues sont absentes du fichier CSV.")
    except Exception as e:
        st.error(f"Une erreur s'est produite : {e}")

