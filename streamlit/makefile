.PHONY: help install run-streamlit run-api run-both test-api docker-build docker-up docker-down docker-logs clean

help:
	@echo "🌱 GreenTech Solutions - Commandes disponibles:"
	@echo ""
	@echo "  make install          - Installer les dépendances Python"
	@echo "  make run-streamlit    - Lancer l'application Streamlit"
	@echo "  make run-api          - Lancer l'API FastAPI"
	@echo "  make run-both         - Lancer Streamlit et API en parallèle"
	@echo "  make test-api         - Tester l'API"
	@echo ""
	@echo "  make docker-build     - Construire l'image Docker"
	@echo "  make docker-up        - Démarrer les conteneurs Docker"
	@echo "  make docker-down      - Arrêter les conteneurs Docker"
	@echo "  make docker-logs      - Voir les logs Docker"
	@echo ""
	@echo "  make clean            - Nettoyer les fichiers temporaires"

install:
	@echo "📦 Installation des dépendances..."
	pip install -r requirements.txt
	@echo "✅ Installation terminée!"

run-streamlit:
	@echo "🚀 Lancement de Streamlit..."
	streamlit run app.py

run-api:
	@echo "🔌 Lancement de l'API FastAPI..."
	uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

run-both:
	@echo "🚀 Lancement de Streamlit et de l'API..."
	@echo "⚠️  Utiliser Ctrl+C pour arrêter"
	@make -j2 run-streamlit run-api

test-api:
	@echo "🧪 Test de l'API..."
	python test_api.py

docker-build:
	@echo "🐳 Construction de l'image Docker..."
	docker-compose build
	@echo "✅ Image construite!"

docker-up:
	@echo "🐳 Démarrage des conteneurs..."
	docker-compose up -d
	@echo "✅ Conteneurs démarrés!"
	@echo "📊 Streamlit: http://localhost:8501"
	@echo "🔌 API: http://localhost:8000"
	@echo "📖 Docs API: http://localhost:8000/docs"

docker-down:
	@echo "🛑 Arrêt des conteneurs..."
	docker-compose down
	@echo "✅ Conteneurs arrêtés!"

docker-logs:
	@echo "📋 Logs des conteneurs..."
	docker-compose logs -f

clean:
	@echo "🧹 Nettoyage..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@echo "✅ Nettoyage terminé!"