import streamlit as st
import pandas as pd
import plotly.express as px

def show():
    st.title("🏠 Tableau de bord énergétique")
    st.markdown("### Exploration interactive des données DPE")

    try:
        df = pd.read_csv("data/donnees_ademe_finales_nettoyees_69_final_pret.csv")
        
        # Section filtres
        st.markdown("---")
        st.markdown("#### 🔍 Filtres")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            type_batiment = st.multiselect(
                "Type de bâtiment",
                options=df['type_batiment'].unique().tolist(),
                default=df['type_batiment'].unique().tolist()
            )
        
        with col2:
            etiquettes = st.multiselect(
                "Étiquette DPE",
                options=['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                default=['A', 'B', 'C', 'D', 'E', 'F', 'G']
            )
        
        with col3:
            # Filtrer les codes postaux pour n'afficher que ceux avec des données
            codes_postaux = sorted(df['code_postal_ban'].dropna().unique())
            codes_postaux_selected = st.multiselect(
                "Code postal",
                options=codes_postaux,
                default=codes_postaux[:5] if len(codes_postaux) > 5 else codes_postaux
            )
        
        # Appliquer les filtres
        df_filtered = df[
            (df['type_batiment'].isin(type_batiment)) &
            (df['etiquette_dpe'].isin(etiquettes)) &
            (df['code_postal_ban'].isin(codes_postaux_selected))
        ]
        
        st.markdown("---")
        
        # Statistiques filtrées
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📍 Logements", f"{len(df_filtered):,}")
        
        with col2:
            conso_moy = df_filtered['conso_5_usages_par_m2_ef'].mean()
            st.metric("⚡ Conso. moyenne", f"{conso_moy:.0f} kWh/m²")
        
        with col3:
            cout_moy = df_filtered['cout_total_5_usages'].mean()
            st.metric("💰 Coût moyen", f"{cout_moy:,.0f} €")
        
        with col4:
            ges_moy = df_filtered['emission_ges_5_usages'].mean()
            st.metric("🌍 GES moyen", f"{ges_moy:,.0f} kg CO₂")
        
        st.markdown("---")
        
        # Tableau de données avec style
        st.markdown("### 📋 Données détaillées")
        
        # Sélection des colonnes à afficher
        colonnes_affichage = [
            'type_batiment', 'etiquette_dpe', 'conso_5_usages_par_m2_ef',
            'cout_total_5_usages', 'emission_ges_5_usages', 
            'type_energie_recodee', 'code_postal_ban', 'surface_habitable_logement'
        ]
        
        # Renommer les colonnes pour l'affichage
        colonnes_renommees = {
            'type_batiment': 'Type',
            'etiquette_dpe': 'Étiquette',
            'conso_5_usages_par_m2_ef': 'Conso (kWh/m²)',
            'cout_total_5_usages': 'Coût (€)',
            'emission_ges_5_usages': 'GES (kg CO₂)',
            'type_energie_recodee': 'Énergie',
            'code_postal_ban': 'Code Postal',
            'surface_habitable_logement': 'Surface (m²)'
        }
        
        df_display = df_filtered[colonnes_affichage].copy()
        df_display = df_display.rename(columns=colonnes_renommees)
        
        # Arrondir les valeurs numériques
        df_display['Conso (kWh/m²)'] = df_display['Conso (kWh/m²)'].round(0)
        df_display['Coût (€)'] = df_display['Coût (€)'].round(0)
        df_display['GES (kg CO₂)'] = df_display['GES (kg CO₂)'].round(0)
        df_display['Surface (m²)'] = df_display['Surface (m²)'].round(1)
        
        # Limiter le nombre de lignes affichées pour éviter l'erreur
        max_rows = 500
        if len(df_display) > max_rows:
            st.warning(f"⚠️ Affichage limité aux {max_rows} premières lignes sur {len(df_display)} au total. Utilisez les filtres pour affiner votre recherche.")
            df_display = df_display.head(max_rows)
        
        # Fonction pour colorer les étiquettes DPE
        def color_etiquette(val):
            colors_map = {
                'A': 'background-color: #00A550; color: white',
                'B': 'background-color: #52B153; color: white',
                'C': 'background-color: #C3D545; color: black',
                'D': 'background-color: #FFF033; color: black',
                'E': 'background-color: #F39200; color: white',
                'F': 'background-color: #ED2124; color: white',
                'G': 'background-color: #CC0033; color: white'
            }
            return colors_map.get(val, '')
        
        # Afficher le dataframe avec style
        st.dataframe(
            df_display.style.applymap(
                color_etiquette,
                subset=['Étiquette']
            ),
            use_container_width=True,
            height=400
        )
        
        # Options de téléchargement
        col1, col2 = st.columns([3, 1])
        with col2:
            csv = df_filtered.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger CSV",
                data=csv,
                file_name="donnees_filtrees.csv",
                mime="text/csv",
            )
        
        st.markdown("---")
        
        # Graphiques supplémentaires
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Distribution des coûts")
            fig_hist = px.histogram(
                df_filtered,
                x='cout_total_5_usages',
                nbins=30,
                color='etiquette_dpe',
                color_discrete_map={
                    'A': '#00A550', 'B': '#52B153', 'C': '#C3D545',
                    'D': '#FFF033', 'E': '#F39200', 'F': '#ED2124', 'G': '#CC0033'
                },
                labels={'cout_total_5_usages': 'Coût annuel (€)', 'count': 'Nombre de logements'}
            )
            fig_hist.update_layout(height=300)
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            st.markdown("#### Répartition par type de bâtiment")
            type_counts = df_filtered['type_batiment'].value_counts()
            fig_type = px.pie(
                values=type_counts.values,
                names=type_counts.index,
                color_discrete_sequence=px.colors.sequential.Greens
            )
            fig_type.update_layout(height=300)
            st.plotly_chart(fig_type, use_container_width=True)
        
    except FileNotFoundError:
        st.error("❌ Le fichier `data/donnees_ademe_finales_nettoyees_69_final_pret.csv` est introuvable.")
        st.info("📂 Assurez-vous que le fichier existe dans le dossier `data/`")
    except Exception as e:
        st.error(f"Une erreur s'est produite : {e}")