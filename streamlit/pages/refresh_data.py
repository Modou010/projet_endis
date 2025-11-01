import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# Ajouter le chemin parent pour importer utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_refresher import DataRefresher

def show():
    st.title(" Rafraîchissement des Données")
    st.markdown("### Mettre à jour les données DPE depuis l'API ADEME")
    st.info(" **Deux sources** : DPE Existants (logements anciens) + DPE Neufs (constructions neuves)")
    
    # Initialiser le refresher
    refresher = DataRefresher()
    
    # Afficher les informations actuelles
    st.markdown("---")
    
    # Afficher les colonnes communes
    with st.expander(" Informations sur les colonnes communes"):
        st.markdown(f"""
        **Colonnes communes identifiées** : {len(refresher.common_columns)}
        
        Les données proviennent de deux sources :
        - **DPE Existants** : {len(refresher.COLUMNS_EXISTANTS)} colonnes disponibles
        - **DPE Neufs** : {len(refresher.COLUMNS_NEUFS)} colonnes disponibles
        
        Pour fusionner les données, seules les colonnes communes sont conservées.
        """)
        
        if st.checkbox("Voir la liste des colonnes communes"):
            cols_sorted = sorted(list(refresher.common_columns))
            st.write(f"**{len(cols_sorted)} colonnes communes :**")
            
            # Afficher en 3 colonnes
            col1, col2, col3 = st.columns(3)
            third = len(cols_sorted) // 3
            
            with col1:
                for col in cols_sorted[:third]:
                    st.caption(f"• {col}")
            with col2:
                for col in cols_sorted[third:2*third]:
                    st.caption(f"• {col}")
            with col3:
                for col in cols_sorted[2*third:]:
                    st.caption(f"• {col}")
    
    st.markdown("---")
    st.markdown("####  État actuel des données")
    
    col1, col2, col3, col4 = st.columns(4)
    
    last_update = refresher.get_last_update_date()
    
    with col1:
        if os.path.exists(refresher.DATA_FILE):
            df = pd.read_csv(refresher.DATA_FILE)
            st.metric(" Total DPE", f"{len(df):,}")
        else:
            st.metric(" Total DPE", "0")
    
    with col2:
        # Afficher le nombre de DPE existants si la colonne source_dpe existe
        if os.path.exists(refresher.DATA_FILE):
            df = pd.read_csv(refresher.DATA_FILE)
            if 'source_dpe' in df.columns:
                existants = len(df[df['source_dpe'] == 'existant'])
                st.metric(" DPE Existants", f"{existants:,}")
            else:
                st.metric(" DPE Existants", "N/A")
        else:
            st.metric(" DPE Existants", "0")
    
    with col3:
        # Afficher le nombre de DPE neufs si la colonne source_dpe existe
        if os.path.exists(refresher.DATA_FILE):
            df = pd.read_csv(refresher.DATA_FILE)
            if 'source_dpe' in df.columns:
                neufs = len(df[df['source_dpe'] == 'neuf'])
                st.metric(" DPE Neufs", f"{neufs:,}")
            else:
                st.metric(" DPE Neufs", "N/A")
        else:
            st.metric(" DPE Neufs", "0")
    
    with col4:
        if last_update:
            st.metric(" Dernière màj", last_update)
        else:
            st.metric(" Dernière màj", "Jamais")
    
    st.markdown("---")
    
    # Options de rafraîchissement
    st.markdown("####  Options de rafraîchissement")
    
    col1, col2 = st.columns(2)
    
    with col1:
        refresh_mode = st.radio(
            "Mode de rafraîchissement",
            options=["Nouveaux DPE uniquement", "Tout recharger"],
            help="Choisir entre mettre à jour uniquement les nouveaux DPE ou tout recharger"
        )
    
    with col2:
        create_backup = st.checkbox(
            "Créer une sauvegarde",
            value=True,
            help="Créer une sauvegarde des données actuelles avant la mise à jour"
        )
    
    st.markdown("---")
    
    # Bouton de rafraîchissement
    if st.button(" Lancer le rafraîchissement", type="primary", width='stretch'):
        
        # Placeholder pour les messages de progression
        progress_bar = st.progress(0)
        status_text = st.empty()
        detail_text = st.empty()
        
        try:
            if refresh_mode == "Nouveaux DPE uniquement":
                # Mode incrémental
                status_text.info(" Recherche de nouveaux DPE (existants + neufs)...")
                
                current_source = {"value": ""}
                
                def update_progress(current, total, code_postal, source):
                    current_source["value"] = source
                    progress = current / total
                    progress_bar.progress(progress)
                    
                    status_text.info(f" Récupération DPE {source}...")
                    detail_text.caption(f"Code postal : {code_postal} ({current}/{total})")
                
                new_df, stats = refresher.refresh_new_data(progress_callback=update_progress)
                
                if stats['total_count'] == 0:
                    status_text.success(" Aucun nouveau DPE trouvé. Les données sont à jour !")
                    st.balloons()
                else:
                    status_text.info(f" Fusion de {stats['total_count']} nouveaux DPE avec les données existantes...")
                    
                    # Fusionner avec les données existantes
                    merged_df = refresher.merge_with_existing(new_df)
                    
                    # Sauvegarder
                    refresher.save_refreshed_data(merged_df, backup=create_backup)
                    
                    # Mettre à jour les métadonnées
                    refresher.save_metadata(
                        datetime.now().strftime("%Y-%m-%d"),
                        len(merged_df),
                        stats['existants_count'],
                        stats['neufs_count']
                    )
                    
                    progress_bar.progress(1.0)
                    status_text.success(f" Rafraîchissement terminé !")
                    detail_text.empty()
                    
                    # Afficher les statistiques détaillées
                    st.markdown("---")
                    st.markdown("####  Statistiques du rafraîchissement")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric(" Nouveaux DPE", f"{stats['total_count']:,}")
                    
                    with col2:
                        st.metric(" Existants", f"{stats['existants_count']:,}", 
                                delta=f"+{stats['existants_count']}")
                    
                    with col3:
                        st.metric(" Neufs", f"{stats['neufs_count']:,}",
                                delta=f"+{stats['neufs_count']}")
                    
                    with col4:
                        st.metric(" Total après màj", f"{len(merged_df):,}")
                    
                    # Graphique de répartition
                    if 'source_dpe' in new_df.columns:
                        st.markdown("####  Répartition des nouveaux DPE")
                        
                        fig = go.Figure(data=[
                            go.Pie(
                                labels=['Existants', 'Neufs'],
                                values=[stats['existants_count'], stats['neufs_count']],
                                marker=dict(colors=['#4CAF50', '#2196F3']),
                                hole=0.4
                            )
                        ])
                        
                        fig.update_layout(
                            title="Répartition des nouveaux DPE par source",
                            height=350
                        )
                        
                        st.plotly_chart(fig, width='stretch')
                    
                    # Aperçu des nouvelles données
                    st.markdown("####  Aperçu des nouvelles données")
                    
                    # Onglets pour séparer existants et neufs
                    if 'source_dpe' in new_df.columns:
                        tab1, tab2 = st.tabs([" DPE Existants", " DPE Neufs"])
                        
                        with tab1:
                            existants_df = new_df[new_df['source_dpe'] == 'existant']
                            if len(existants_df) > 0:
                                st.dataframe(existants_df.head(10), width='stretch')
                            else:
                                st.info("Aucun nouveau DPE existant")
                        
                        with tab2:
                            neufs_df = new_df[new_df['source_dpe'] == 'neuf']
                            if len(neufs_df) > 0:
                                st.dataframe(neufs_df.head(10), width='stretch')
                            else:
                                st.info("Aucun nouveau DPE neuf")
                    else:
                        st.dataframe(new_df.head(10), width='stretch')
                    
                    st.balloons()
            
            else:
                # Mode complet : recharger toutes les données
                status_text.warning(" Mode rechargement complet activé. Cela peut prendre plusieurs minutes...")
                
                def update_progress(current, total, code_postal):
                    progress = current / total
                    progress_bar.progress(progress)
                    status_text.info(f" Téléchargement complet... {code_postal} ({current}/{total})")
                
                # Utiliser la logique de fetch_data_smart pour tout recharger
                all_results = []
                total_codes = len(refresher.codes_postaux)
                
                for idx, cp in enumerate(refresher.codes_postaux):
                    update_progress(idx + 1, total_codes, cp)
                    results = refresher.fetch_data_smart(cp)
                    all_results.extend(results)
                
                if not all_results:
                    status_text.error(" Aucune donnée récupérée")
                else:
                    status_text.info(" Sauvegarde des données...")
                    
                    df_complete = pd.DataFrame(all_results)
                    refresher.save_refreshed_data(df_complete, backup=create_backup)
                    refresher.save_metadata(datetime.now().strftime("%Y-%m-%d"), len(df_complete))
                    
                    progress_bar.progress(1.0)
                    status_text.success(f" Rechargement complet terminé ! {len(df_complete):,} DPE récupérés.")
                    
                    st.balloons()
        
        except Exception as e:
            status_text.error(f" Erreur lors du rafraîchissement : {e}")
            st.exception(e)
    
    # Section d'information
    st.markdown("---")
    st.markdown("#### ℹ Informations")
    
    with st.expander(" Comment fonctionne le rafraîchissement ?"):
        st.markdown("""
        **Mode "Nouveaux DPE uniquement"** :
        - Récupère uniquement les DPE enregistrés depuis la dernière mise à jour
        - Plus rapide et économe en ressources
        - Recommandé pour les mises à jour régulières
        
        **Mode "Tout recharger"** :
        - Récupère toutes les données depuis l'API ADEME
        - Plus long mais garantit des données complètes
        - Recommandé en cas de problème ou pour une réinitialisation
        
        **Gestion des doublons** :
        - Les doublons sont automatiquement supprimés basés sur le numéro de DPE
        - En cas de doublon, la version la plus récente est conservée
        
        **Sauvegarde** :
        - Une sauvegarde horodatée est créée avant chaque mise à jour si l'option est activée
        - Format : `donnees_ademe_finales_nettoyees_69_final_pret.csv.backup_YYYYMMDD_HHMMSS`
        """)
    
    with st.expander(" Configuration des codes postaux"):
        st.markdown(f"""
        **Fichier de configuration** : `{refresher.codes_postaux_file}`
        
        **Codes postaux configurés** : {len(refresher.codes_postaux)}
        """)
        
        # Afficher quelques codes postaux
        if len(refresher.codes_postaux) > 0:
            st.write("Exemples de codes postaux :")
            st.code(", ".join(refresher.codes_postaux[:10]) + ("..." if len(refresher.codes_postaux) > 10 else ""))

if __name__ == "__main__":
    show()