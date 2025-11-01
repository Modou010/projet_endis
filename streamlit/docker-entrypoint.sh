#!/bin/bash

# Script de démarrage pour Docker
# Permet de lancer soit Streamlit soit FastAPI selon la variable d'environnement

set -e

echo "🚀 Démarrage de GreenTech Solutions..."

# Vérifier que les dossiers existent
mkdir -p data models logs

# Lancer le service approprié
if [ "$SERVICE_MODE" = "streamlit" ]; then
    echo "📊 Démarrage de l'interface Streamlit..."
    exec streamlit run app.py --server.address=0.0.0.0 --server.port=8501
elif [ "$SERVICE_MODE" = "api" ]; then
    echo "🔌 Démarrage de l'API FastAPI..."
    exec uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
else
    echo "⚠️ SERVICE_MODE non défini. Démarrage de Streamlit par défaut..."
    exec streamlit run app.py --server.address=0.0.0.0 --server.port=8501
fi