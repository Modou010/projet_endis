import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
import os
from datetime import datetime

# Ajouter le chemin parent pour importer utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.model_trainer import ModelTrainer

def show():
    st.title("🤖 Réentraînement des Modèles")
    st.markdown("### Entraîner ou réentraîner les modèles de Machine Learning")
    
    # Initialiser le trainer
    trainer = ModelTrainer()
    
    # Vérifier si les données existent
    if not os.path.exists(trainer.DATA_FILE):
        st.error("❌ Fichier de données introuvable. Veuillez d'abord charger ou rafraîchir les données.")
        st.info(f"📁 Fichier attendu : {trainer.DATA_FILE}")
        return
    
    # Charger les métriques existantes si disponibles
    existing_metrics = trainer.load_metrics()
    
    # Afficher les performances actuelles des modèles
    st.markdown("---")
    st.markdown("#### 📊 Performances actuelles des modèles")
    
    if existing_metrics:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 🎯 Modèle de Classification (Étiquette DPE)")
            if 'classification' in existing_metrics:
                classif = existing_metrics['classification']
                
                metric_col1, metric_col2 = st.columns(2)
                with metric_col1:
                    st.metric("Accuracy", f"{classif['accuracy']*100:.2f}%")
                with metric_col2:
                    st.metric("F1-Score", f"{classif['f1_score']:.3f}")
                
                st.info(f"📅 Entraîné le : {classif.get('trained_at', 'N/A')[:10]}")
                st.caption(f"Échantillons d'entraînement : {classif.get('train_samples', 'N/A'):,}")
            else:
                st.warning("Modèle non entraîné")
        
        with col2:
            st.markdown("##### 📈 Modèle de Régression (Coût Total)")
            if 'regression' in existing_metrics:
                regress = existing_metrics['regression']
                
                metric_col1, metric_col2 = st.columns(2)
                with metric_col1:
                    st.metric("R² Score", f"{regress['r2_score']:.3f}")
                with metric_col2:
                    st.metric("MAE", f"{regress['mae']:.2f} €")
                
                st.info(f"📅 Entraîné le : {regress.get('trained_at', 'N/A')[:10]}")
                st.caption(f"Échantillons d'entraînement : {regress.get('train_samples', 'N/A'):,}")
            else:
                st.warning("Modèle non entraîné")
    else:
        st.info("ℹ️ Aucun modèle entraîné détecté. Lancez un premier entraînement ci-dessous.")
    
    st.markdown("---")
    
    # Configuration de l'entraînement
    st.markdown("#### ⚙️ Configuration de l'entraînement")
    
    col1, col2 = st.columns(2)
    
    with col1:
        test_size = st.slider(
            "Taille du jeu de test (%)",
            min_value=10,
            max_value=40,
            value=20,
            step=5,
            help="Pourcentage des données utilisées pour le test"
        )
    
    with col2:
        random_state = st.number_input(
            "Random State",
            min_value=0,
            max_value=100,
            value=42,
            help="Graine aléatoire pour la reproductibilité"
        )
    
    # Paramètres avancés
    with st.expander("🔧 Paramètres avancés des modèles"):
        col1, col2 = st.columns(2)
        
        with col1:
            n_estimators = st.number_input(
                "Nombre d'arbres",
                min_value=50,
                max_value=500,
                value=100,
                step=50,
                help="Nombre d'arbres dans la forêt aléatoire"
            )
            
            max_depth = st.number_input(
                "Profondeur maximale",
                min_value=5,
                max_value=50,
                value=20,
                step=5,
                help="Profondeur maximale des arbres"
            )
        
        with col2:
            min_samples_split = st.number_input(
                "Min échantillons pour split",
                min_value=2,
                max_value=20,
                value=5,
                help="Nombre minimum d'échantillons requis pour diviser un nœud"
            )
            
            min_samples_leaf = st.number_input(
                "Min échantillons par feuille",
                min_value=1,
                max_value=10,
                value=2,
                help="Nombre minimum d'échantillons requis dans une feuille"
            )
    
    st.markdown("---")
    
    # Aperçu des données
    st.markdown("#### 👀 Aperçu des données d'entraînement")
    
    df_preview = pd.read_csv(trainer.DATA_FILE)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📊 Total enregistrements", f"{len(df_preview):,}")
    
    with col2:
        # Compter les valeurs non nulles pour les features
        valid_classif = df_preview[trainer.FEATURES + [trainer.TARGET_CLASSIFICATION]].dropna()
        st.metric("✅ Valides (Classification)", f"{len(valid_classif):,}")
    
    with col3:
        valid_regress = df_preview[trainer.FEATURES + [trainer.TARGET_REGRESSION]].dropna()
        st.metric("✅ Valides (Régression)", f"{len(valid_regress):,}")
    
    # Distribution des étiquettes DPE
    if trainer.TARGET_CLASSIFICATION in df_preview.columns:
        st.markdown("##### Distribution des étiquettes DPE")
        
        etiquette_counts = df_preview[trainer.TARGET_CLASSIFICATION].value_counts().sort_index()
        
        colors_dpe = {
            'A': '#00A550', 'B': '#52B153', 'C': '#C3D545',
            'D': '#FFF033', 'E': '#F39200', 'F': '#ED2124', 'G': '#CC0033'
        }
        
        fig = go.Figure(data=[
            go.Bar(
                x=etiquette_counts.index,
                y=etiquette_counts.values,
                marker_color=[colors_dpe.get(x, '#666') for x in etiquette_counts.index],
                text=etiquette_counts.values,
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            xaxis_title="Étiquette DPE",
            yaxis_title="Nombre",
            height=300,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Bouton d'entraînement
    if st.button("🚀 Lancer l'entraînement", type="primary", use_container_width=True):
        
        # Placeholder pour les messages de progression
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Préparer les paramètres du modèle
            model_params = {
                'n_estimators': n_estimators,
                'max_depth': max_depth,
                'min_samples_split': min_samples_split,
                'min_samples_leaf': min_samples_leaf,
                'random_state': random_state
            }
            
            # Callback de progression
            def update_status(message):
                status_text.info(message)
            
            # Charger les données
            update_status("📁 Chargement des données...")
            progress_bar.progress(0.1)
            
            df = pd.read_csv(trainer.DATA_FILE)
            
            # Préparer les données
            update_status("🔧 Préparation des données...")
            progress_bar.progress(0.2)
            
            df_classif, df_regress = trainer.prepare_data(df)
            
            # Entraîner le modèle de classification
            update_status("🎯 Entraînement du modèle de classification...")
            progress_bar.progress(0.3)
            
            classifier, classif_metrics = trainer.train_classification_model(
                df_classif,
                test_size=test_size/100,
                **model_params
            )
            
            progress_bar.progress(0.6)
            
            # Entraîner le modèle de régression
            update_status("📈 Entraînement du modèle de régression...")

            regress_params = {
                k: v for k, v in model_params.items() if k != 'n_estimators'
                }
            
            regressor, regress_metrics = trainer.train_regression_model(
                df_regress,
                test_size=test_size/100,
                **regress_params
            )
            
            progress_bar.progress(0.9)
            
            # Sauvegarder les modèles
            update_status("💾 Sauvegarde des modèles...")
            
            trainer.save_models(classifier, regressor)
            trainer.save_metrics({
                'classification': classif_metrics,
                'regression': regress_metrics
            })
            
            progress_bar.progress(1.0)
            status_text.success("✅ Entraînement terminé avec succès !")
            
            st.balloons()
            
            # Afficher les résultats détaillés
            st.markdown("---")
            st.markdown("### 🎉 Résultats de l'entraînement")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🎯 Classification (Étiquette DPE)")
                
                metric_col1, metric_col2, metric_col3 = st.columns(3)
                with metric_col1:
                    st.metric("Accuracy", f"{classif_metrics['accuracy']*100:.2f}%")
                with metric_col2:
                    st.metric("F1-Score", f"{classif_metrics['f1_score']:.3f}")
                with metric_col3:
                    st.metric("Classes", len(classif_metrics['classes']))
                
                st.caption(f"✅ Entraîné sur {classif_metrics['train_samples']:,} échantillons")
                st.caption(f"🧪 Testé sur {classif_metrics['test_samples']:,} échantillons")
                
                # Importance des features
                st.markdown("##### 📊 Importance des features")
                feat_imp = pd.DataFrame({
                    'Feature': list(classif_metrics['feature_importance'].keys()),
                    'Importance': list(classif_metrics['feature_importance'].values())
                }).sort_values('Importance', ascending=False)
                
                fig_feat = px.bar(
                    feat_imp,
                    x='Importance',
                    y='Feature',
                    orientation='h',
                    color='Importance',
                    color_continuous_scale='Greens'
                )
                fig_feat.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig_feat, use_container_width=True)
            
            with col2:
                st.markdown("#### 📈 Régression (Coût Total)")
                
                metric_col1, metric_col2, metric_col3 = st.columns(3)
                with metric_col1:
                    st.metric("R² Score", f"{regress_metrics['r2_score']:.3f}")
                with metric_col2:
                    st.metric("MAE", f"{regress_metrics['mae']:.0f} €")
                with metric_col3:
                    st.metric("RMSE", f"{regress_metrics['rmse']:.0f} €")
                
                st.caption(f"✅ Entraîné sur {regress_metrics['train_samples']:,} échantillons")
                st.caption(f"🧪 Testé sur {regress_metrics['test_samples']:,} échantillons")
                
                # Importance des features
                st.markdown("##### 📊 Importance des features")
                feat_imp = pd.DataFrame({
                    'Feature': list(regress_metrics['feature_importance'].keys()),
                    'Importance': list(regress_metrics['feature_importance'].values())
                }).sort_values('Importance', ascending=False)
                
                fig_feat = px.bar(
                    feat_imp,
                    x='Importance',
                    y='Feature',
                    orientation='h',
                    color='Importance',
                    color_continuous_scale='Blues'
                )
                fig_feat.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig_feat, use_container_width=True)
            
            # Rapport de classification détaillé
            if 'classification_report' in classif_metrics:
                with st.expander("📋 Rapport de classification détaillé"):
                    report_df = pd.DataFrame(classif_metrics['classification_report']).transpose()
                    st.dataframe(report_df.style.format("{:.3f}"), use_container_width=True)
        
        except Exception as e:
            status_text.error(f"❌ Erreur lors de l'entraînement : {e}")
            st.exception(e)
    
    # Section d'information
    st.markdown("---")
    st.markdown("#### ℹ️ Informations sur l'entraînement")
    
    with st.expander("📖 À propos des modèles"):
        st.markdown("""
        **Modèle de Classification** :
        - Algorithme : Random Forest Classifier
        - Objectif : Prédire l'étiquette DPE (A, B, C, D, E, F, G)
        - Métrique principale : Accuracy et F1-Score
        
        **Modèle de Régression** :
        - Algorithme : Random Forest Regressor
        - Objectif : Prédire le coût total des 5 usages (€/an)
        - Métriques principales : R², MAE, RMSE
        
        **Features utilisées** :
        """)
        st.code(", ".join(trainer.FEATURES))
        
        st.markdown("""
        **Prétraitement** :
        - Encodage des variables catégorielles (type_batiment, type_energie_recodee)
        - Suppression des valeurs manquantes
        - Séparation train/test avec stratification (classification)
        """)
    
    with st.expander("💡 Conseils pour l'entraînement"):
        st.markdown("""
        **Quand réentraîner les modèles ?**
        - Après avoir rafraîchi les données avec de nouveaux DPE
        - Si les performances des modèles se dégradent
        - Pour expérimenter avec différents hyperparamètres
        
        **Choix des hyperparamètres** :
        - **n_estimators** : Plus d'arbres = meilleure performance mais plus lent
        - **max_depth** : Contrôle la complexité (trop élevé = surapprentissage)
        - **min_samples_split/leaf** : Régularisation pour éviter le surapprentissage
        
        **Interprétation des métriques** :
        - **Accuracy > 95%** : Excellent
        - **R² > 0.90** : Très bon pouvoir prédictif
        - **MAE** : Erreur moyenne en euros (plus c'est bas, mieux c'est)
        """)

if __name__ == "__main__":
    show()