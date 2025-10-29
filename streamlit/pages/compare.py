import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def show():
    st.title("⚖️ Comparer les logements")
    st.markdown("### Comparaison détaillée côte à côte")

    try:
        df = pd.read_csv("data/donnees_ademe_finales_nettoyees_69_final_pret.csv")
        
        # Créer un identifiant unique pour chaque logement
        df['id_logement'] = df.apply(
            lambda row: f"{row['type_batiment']} - {row['etiquette_dpe']} - {row['code_postal_ban']} - {row.name}",
            axis=1
        )
        
        st.markdown("---")
        
        # Sélecteurs de logements
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🏠 Logement 1")
            
            # Filtres pour logement 1
            type1 = st.selectbox(
                "Type de bâtiment",
                options=df['type_batiment'].unique().tolist(),
                key="type1"
            )
            
            df_filtered1 = df[df['type_batiment'] == type1]
            
            etiquette1 = st.selectbox(
                "Étiquette DPE",
                options=sorted(df_filtered1['etiquette_dpe'].unique().tolist()),
                key="etiq1"
            )
            
            df_filtered1 = df_filtered1[df_filtered1['etiquette_dpe'] == etiquette1]
            
            logement1_id = st.selectbox(
                "Sélectionner un logement",
                options=df_filtered1['id_logement'].tolist(),
                key="log1"
            )
            
            logement1 = df[df['id_logement'] == logement1_id].iloc[0]
        
        with col2:
            st.markdown("#### 🏠 Logement 2")
            
            # Filtres pour logement 2
            type2 = st.selectbox(
                "Type de bâtiment",
                options=df['type_batiment'].unique().tolist(),
                key="type2"
            )
            
            df_filtered2 = df[df['type_batiment'] == type2]
            
            etiquette2 = st.selectbox(
                "Étiquette DPE",
                options=sorted(df_filtered2['etiquette_dpe'].unique().tolist()),
                key="etiq2"
            )
            
            df_filtered2 = df_filtered2[df_filtered2['etiquette_dpe'] == etiquette2]
            
            logement2_id = st.selectbox(
                "Sélectionner un logement",
                options=df_filtered2['id_logement'].tolist(),
                key="log2"
            )
            
            logement2 = df[df['id_logement'] == logement2_id].iloc[0]
        
        st.markdown("---")
        
        # Bouton de comparaison
        if st.button("🔍 Comparer les logements", type="primary", width='stretch'):
            
            # Cartes de comparaison
            col1, col2 = st.columns(2)
            
            colors_dpe = {
                'A': '#00A550', 'B': '#52B153', 'C': '#C3D545',
                'D': '#FFF033', 'E': '#F39200', 'F': '#ED2124', 'G': '#CC0033'
            }
            
            with col1:
                color1 = colors_dpe.get(logement1['etiquette_dpe'], '#666666')
                st.markdown(
                    f"""
                    <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                                border-left: 6px solid {color1}; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        <h3 style="color: {color1};">🏠 Logement 1</h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                st.markdown("##### 📋 Caractéristiques")
                st.markdown(f"**Type :** {logement1['type_batiment'].capitalize()}")
                st.markdown(f"**Étiquette DPE :** <span style='background-color: {color1}; color: white; padding: 4px 12px; border-radius: 4px; font-weight: bold;'>{logement1['etiquette_dpe']}</span>", unsafe_allow_html=True)
                st.markdown(f"**Surface :** {logement1['surface_habitable_logement']:.1f} m²")
                st.markdown(f"**Code postal :** {int(logement1['code_postal_ban'])}")
                st.markdown(f"**Énergie :** {logement1['type_energie_recodee']}")
                
                st.markdown("##### 💰 Coûts et consommation")
                st.metric("Coût annuel total", f"{logement1['cout_total_5_usages']:,.0f} €")
                st.metric("Consommation par m²", f"{logement1['conso_5_usages_par_m2_ef']:.0f} kWh/m²")
                st.metric("Consommation totale", f"{logement1['conso_5_usages_ef']:,.0f} kWh")
                
                st.markdown("##### 🌍 Impact environnemental")
                st.metric("Émissions GES", f"{logement1['emission_ges_5_usages']:,.0f} kg CO₂")
                st.markdown(f"**Étiquette GES :** {logement1['etiquette_ges']}")
            
            with col2:
                color2 = colors_dpe.get(logement2['etiquette_dpe'], '#666666')
                st.markdown(
                    f"""
                    <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                                border-left: 6px solid {color2}; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        <h3 style="color: {color2};">🏠 Logement 2</h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                st.markdown("##### 📋 Caractéristiques")
                st.markdown(f"**Type :** {logement2['type_batiment'].capitalize()}")
                st.markdown(f"**Étiquette DPE :** <span style='background-color: {color2}; color: white; padding: 4px 12px; border-radius: 4px; font-weight: bold;'>{logement2['etiquette_dpe']}</span>", unsafe_allow_html=True)
                st.markdown(f"**Surface :** {logement2['surface_habitable_logement']:.1f} m²")
                st.markdown(f"**Code postal :** {int(logement2['code_postal_ban'])}")
                st.markdown(f"**Énergie :** {logement2['type_energie_recodee']}")
                
                st.markdown("##### 💰 Coûts et consommation")
                st.metric("Coût annuel total", f"{logement2['cout_total_5_usages']:,.0f} €")
                st.metric("Consommation par m²", f"{logement2['conso_5_usages_par_m2_ef']:.0f} kWh/m²")
                st.metric("Consommation totale", f"{logement2['conso_5_usages_ef']:,.0f} kWh")
                
                st.markdown("##### 🌍 Impact environnemental")
                st.metric("Émissions GES", f"{logement2['emission_ges_5_usages']:,.0f} kg CO₂")
                st.markdown(f"**Étiquette GES :** {logement2['etiquette_ges']}")
            
            st.markdown("---")
            
            # Résultats de la comparaison
            st.markdown("### 📊 Analyse comparative")
            
            diff_cout = logement1['cout_total_5_usages'] - logement2['cout_total_5_usages']
            diff_conso = logement1['conso_5_usages_par_m2_ef'] - logement2['conso_5_usages_par_m2_ef']
            diff_ges = logement1['emission_ges_5_usages'] - logement2['emission_ges_5_usages']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                delta_color = "inverse" if diff_cout > 0 else "normal"
                st.metric(
                    "Différence de coût",
                    f"{abs(diff_cout):,.0f} €",
                    delta=f"{diff_cout:+,.0f} €",
                    delta_color=delta_color
                )
            
            with col2:
                delta_color = "inverse" if diff_conso > 0 else "normal"
                st.metric(
                    "Différence de consommation",
                    f"{abs(diff_conso):.0f} kWh/m²",
                    delta=f"{diff_conso:+.0f} kWh/m²",
                    delta_color=delta_color
                )
            
            with col3:
                delta_color = "inverse" if diff_ges > 0 else "normal"
                st.metric(
                    "Différence d'émissions",
                    f"{abs(diff_ges):,.0f} kg CO₂",
                    delta=f"{diff_ges:+,.0f} kg CO₂",
                    delta_color=delta_color
                )
            
            # Graphique de comparaison
            st.markdown("#### Comparaison visuelle")
            
            categories = ['Coût (€)', 'Conso (kWh/m²)', 'GES (kg CO₂)']
            
            fig = go.Figure(data=[
                go.Bar(
                    name='Logement 1',
                    x=categories,
                    y=[
                        logement1['cout_total_5_usages'],
                        logement1['conso_5_usages_par_m2_ef'],
                        logement1['emission_ges_5_usages']/10  # Divisé par 10 pour l'échelle
                    ],
                    marker_color=color1,
                    text=[
                        f"{logement1['cout_total_5_usages']:,.0f}",
                        f"{logement1['conso_5_usages_par_m2_ef']:.0f}",
                        f"{logement1['emission_ges_5_usages']:,.0f}"
                    ],
                    textposition='outside'
                ),
                go.Bar(
                    name='Logement 2',
                    x=categories,
                    y=[
                        logement2['cout_total_5_usages'],
                        logement2['conso_5_usages_par_m2_ef'],
                        logement2['emission_ges_5_usages']/10  # Divisé par 10 pour l'échelle
                    ],
                    marker_color=color2,
                    text=[
                        f"{logement2['cout_total_5_usages']:,.0f}",
                        f"{logement2['conso_5_usages_par_m2_ef']:.0f}",
                        f"{logement2['emission_ges_5_usages']:,.0f}"
                    ],
                    textposition='outside'
                )
            ])
            
            fig.update_layout(
                barmode='group',
                height=400,
                yaxis_title="Valeur",
                showlegend=True
            )
            
            st.plotly_chart(fig, width='stretch')
            
            # Recommandations
            st.markdown("---")
            st.markdown("### 💡 Recommandations")
            
            meilleur = "Logement 1" if diff_cout < 0 else "Logement 2"
            economie = abs(diff_cout)
            
            if diff_cout != 0:
                st.success(
                    f"✅ **{meilleur}** est plus économique avec une économie de **{economie:,.0f} €/an** "
                    f"soit **{economie*10:,.0f} €** sur 10 ans !"
                )
            else:
                st.info("Les deux logements ont des coûts similaires.")
            
            if diff_ges < 0:
                st.success(
                    f"🌱 **Logement 1** a un impact environnemental plus faible avec "
                    f"**{abs(diff_ges):,.0f} kg CO₂** d'émissions en moins par an."
                )
            elif diff_ges > 0:
                st.success(
                    f"🌱 **Logement 2** a un impact environnemental plus faible avec "
                    f"**{abs(diff_ges):,.0f} kg CO₂** d'émissions en moins par an."
                )
        
    except FileNotFoundError:
        st.error("❌ Le fichier de données est introuvable.")
        st.info("📂 Assurez-vous que `data/donnees_ademe_finales_nettoyees_69_final_pret.csv` existe.")
    except Exception as e:
        st.error(f"Une erreur s'est produite : {e}")
        import traceback
        st.code(traceback.format_exc())