#!/usr/bin/env python3
"""
Script de vérification de l'installation GreenTech Solutions
Vérifie que tous les fichiers sont en place et correctement configurés
"""

import os
import sys
from pathlib import Path
import importlib.util

# Couleurs pour l'affichage
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}  {text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓{Colors.END} {text}")

def print_error(text):
    print(f"{Colors.RED}✗{Colors.END} {text}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠{Colors.END} {text}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ{Colors.END} {text}")

# Structure attendue du projet
REQUIRED_STRUCTURE = {
    'files': [
        'app.py',
        'requirements.txt',
        'README.md',
        'test_api.py',
        'Dockerfile',
        'docker-compose.yml',
        'docker-entrypoint.sh',
        '.dockerignore',
    ],
    'directories': {
        'pages': [
            '__init__.py',
            'welcome.py',
            'home.py',
            'analysis.py',
            'compare.py',
            'about.py',
            'enedis.py',
            'prediction.py',
            'refresh_data.py',
            'retrain_models.py'
        ],
        'utils': [
            '__init__.py',
            'data_loader.py',
            'model_utils.py',
            'data_refresher.py',
            'model_trainer.py',
            'api_client.py'
        ],
        'api': [
            'main.py'
        ],
        'data': [],  # Vide mais doit exister
        'models': []  # Vide mais doit exister
    }
}

# Dépendances requises
REQUIRED_PACKAGES = [
    'streamlit',
    'pandas',
    'numpy',
    'scikit-learn',
    'plotly',
    'fastapi',
    'uvicorn',
    'pydantic',
    'requests',
    'joblib'
]

def check_file_exists(filepath):
    """Vérifier si un fichier existe"""
    return os.path.isfile(filepath)

def check_directory_exists(dirpath):
    """Vérifier si un dossier existe"""
    return os.path.isdir(dirpath)

def check_package_installed(package_name):
    """Vérifier si un package Python est installé"""
    spec = importlib.util.find_spec(package_name)
    return spec is not None

def check_file_structure():
    """Vérifier la structure des fichiers"""
    print_header("Vérification de la structure des fichiers")
    
    all_good = True
    
    # Vérifier les fichiers racine
    print_info("Fichiers racine:")
    for file in REQUIRED_STRUCTURE['files']:
        if check_file_exists(file):
            print_success(f"  {file}")
        else:
            print_error(f"  {file} - MANQUANT")
            all_good = False
    
    # Vérifier les dossiers et leurs fichiers
    for directory, files in REQUIRED_STRUCTURE['directories'].items():
        print_info(f"\nDossier {directory}/:")
        
        if not check_directory_exists(directory):
            print_error(f"  Le dossier {directory}/ n'existe pas")
            all_good = False
            continue
        
        print_success(f"  Dossier existe")
        
        for file in files:
            filepath = os.path.join(directory, file)
            if check_file_exists(filepath):
                print_success(f"    {file}")
            else:
                print_error(f"    {file} - MANQUANT")
                all_good = False
    
    return all_good

def check_dependencies():
    """Vérifier les dépendances Python"""
    print_header("Vérification des dépendances Python")
    
    all_good = True
    
    for package in REQUIRED_PACKAGES:
        if check_package_installed(package):
            print_success(f"  {package}")
        else:
            print_error(f"  {package} - NON INSTALLÉ")
            all_good = False
    
    return all_good

def check_data_files():
    """Vérifier les fichiers de données"""
    print_header("Vérification des fichiers de données")
    
    data_file = "data/donnees_ademe_finales_nettoyees_69_final_pret.csv"
    codes_postaux_file = "data/adresses-69.csv"
    
    if check_file_exists(data_file):
        print_success(f"  Données DPE trouvées: {data_file}")
        # Vérifier la taille
        size_mb = os.path.getsize(data_file) / (1024 * 1024)
        print_info(f"    Taille: {size_mb:.2f} MB")
    else:
        print_warning(f"  Données DPE non trouvées: {data_file}")
        print_info("    Ce fichier sera nécessaire pour utiliser l'application")
    
    if check_file_exists(codes_postaux_file):
        print_success(f"  Codes postaux trouvés: {codes_postaux_file}")
    else:
        print_warning(f"  Codes postaux non trouvés: {codes_postaux_file}")
        print_info("    Ce fichier est nécessaire pour le rafraîchissement des données")
    
    return True

def check_models():
    """Vérifier les modèles ML"""
    print_header("Vérification des modèles ML")
    
    classifier_file = "models/classification_model.pkl"
    regressor_file = "models/regression_model.pkl"
    
    classifier_exists = check_file_exists(classifier_file)
    regressor_exists = check_file_exists(regressor_file)
    
    if classifier_exists:
        print_success(f"  Modèle de classification trouvé: {classifier_file}")
        size_mb = os.path.getsize(classifier_file) / (1024 * 1024)
        print_info(f"    Taille: {size_mb:.2f} MB")
    else:
        print_warning(f"  Modèle de classification non trouvé: {classifier_file}")
        print_info("    Utilisez la page 'Réentraîner modèles' pour créer ce modèle")
    
    if regressor_exists:
        print_success(f"  Modèle de régression trouvé: {regressor_file}")
        size_mb = os.path.getsize(regressor_file) / (1024 * 1024)
        print_info(f"    Taille: {size_mb:.2f} MB")
    else:
        print_warning(f"  Modèle de régression non trouvé: {regressor_file}")
        print_info("    Utilisez la page 'Réentraîner modèles' pour créer ce modèle")
    
    return True

def check_imports():
    """Vérifier que les imports fonctionnent"""
    print_header("Vérification des imports")
    
    all_good = True
    
    # Test imports utils
    try:
        from utils import data_loader, model_utils
        print_success("  utils.data_loader")
        print_success("  utils.model_utils")
    except ImportError as e:
        print_error(f"  Erreur import utils existants: {e}")
        all_good = False
    
    # Test nouveaux imports utils
    try:
        from utils import data_refresher, model_trainer, api_client
        print_success("  utils.data_refresher")
        print_success("  utils.model_trainer")
        print_success("  utils.api_client")
    except ImportError as e:
        print_error(f"  Erreur import nouveaux utils: {e}")
        all_good = False
    
    # Test imports pages
    try:
        from pages import welcome, home, analysis, compare, about, enedis, prediction
        print_success("  pages existantes")
    except ImportError as e:
        print_error(f"  Erreur import pages existantes: {e}")
        all_good = False
    
    # Test nouvelles pages
    try:
        from pages import refresh_data, retrain_models
        print_success("  pages.refresh_data")
        print_success("  pages.retrain_models")
    except ImportError as e:
        print_error(f"  Erreur import nouvelles pages: {e}")
        all_good = False
    
    # Test API
    try:
        from api import main
        print_success("  api.main")
    except ImportError as e:
        print_error(f"  Erreur import API: {e}")
        all_good = False
    
    return all_good

def check_docker():
    """Vérifier la configuration Docker"""
    print_header("Vérification de Docker")
    
    # Vérifier si Docker est installé
    docker_installed = os.system("docker --version > /dev/null 2>&1") == 0
    
    if docker_installed:
        print_success("  Docker est installé")
        
        # Vérifier docker-compose
        compose_installed = os.system("docker-compose --version > /dev/null 2>&1") == 0
        if compose_installed:
            print_success("  Docker Compose est installé")
        else:
            print_warning("  Docker Compose n'est pas installé")
            print_info("    Docker Compose est recommandé pour lancer l'application")
    else:
        print_warning("  Docker n'est pas installé")
        print_info("    Docker est optionnel mais recommandé pour le déploiement")
    
    return True

def create_missing_init_files():
    """Créer les fichiers __init__.py manquants"""
    print_header("Création des fichiers __init__.py manquants")
    
    init_files = [
        'utils/__init__.py',
        'pages/__init__.py',
        'api/__init__.py'
    ]
    
    for init_file in init_files:
        if not check_file_exists(init_file):
            try:
                os.makedirs(os.path.dirname(init_file), exist_ok=True)
                with open(init_file, 'w') as f:
                    f.write('"""Module initialization"""\n')
                print_success(f"  Créé: {init_file}")
            except Exception as e:
                print_error(f"  Erreur création {init_file}: {e}")
        else:
            print_info(f"  Déjà présent: {init_file}")

def create_missing_directories():
    """Créer les dossiers manquants"""
    print_header("Création des dossiers manquants")
    
    directories = ['data', 'models', 'logs', 'utils', 'pages', 'api']
    
    for directory in directories:
        if not check_directory_exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
                print_success(f"  Créé: {directory}/")
            except Exception as e:
                print_error(f"  Erreur création {directory}/: {e}")
        else:
            print_info(f"  Déjà présent: {directory}/")

def run_quick_tests():
    """Exécuter des tests rapides"""
    print_header("Tests rapides")
    
    # Test 1: Importer l'application principale
    try:
        import app
        print_success("  app.py peut être importé")
    except Exception as e:
        print_error(f"  Erreur import app.py: {e}")
    
    # Test 2: Vérifier que les modèles peuvent être chargés (si présents)
    if check_file_exists("models/classification_model.pkl"):
        try:
            import joblib
            model = joblib.load("models/classification_model.pkl")
            print_success(f"  Modèle de classification chargé (type: {type(model).__name__})")
        except Exception as e:
            print_error(f"  Erreur chargement modèle classification: {e}")
    
    # Test 3: Vérifier l'API
    try:
        from api.main import app as fastapi_app
        print_success(f"  API FastAPI peut être importée")
    except Exception as e:
        print_error(f"  Erreur import API: {e}")

def print_summary(results):
    """Afficher le résumé final"""
    print_header("Résumé de la vérification")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\nRésultats: {passed}/{total} vérifications réussies")
    print(f"Taux de réussite: {(passed/total)*100:.1f}%\n")
    
    if passed == total:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ Tout est prêt ! Vous pouvez lancer l'application.{Colors.END}\n")
        print("Commandes pour démarrer:")
        print(f"  {Colors.BLUE}streamlit run app.py{Colors.END}                    # Lancer Streamlit")
        print(f"  {Colors.BLUE}uvicorn api.main:app --reload{Colors.END}          # Lancer l'API")
        print(f"  {Colors.BLUE}make run-both{Colors.END}                          # Lancer les deux (avec Makefile)")
        print(f"  {Colors.BLUE}docker-compose up -d{Colors.END}                   # Lancer avec Docker")
    else:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠ Des problèmes ont été détectés.{Colors.END}\n")
        print("Actions recommandées:")
        
        if not results.get('dependencies', True):
            print(f"  1. Installer les dépendances: {Colors.BLUE}pip install -r requirements.txt{Colors.END}")
        
        if not results.get('structure', True):
            print(f"  2. Vérifier que tous les fichiers fournis sont bien copiés")
        
        if not results.get('imports', True):
            print(f"  3. Créer les fichiers __init__.py manquants")

def main():
    """Fonction principale"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║        GreenTech Solutions - Setup Checker                ║")
    print("║           Vérification de l'installation                  ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    results = {}
    
    # Créer les dossiers et fichiers manquants d'abord
    create_missing_directories()
    create_missing_init_files()
    
    # Exécuter les vérifications
    results['structure'] = check_file_structure()
    results['dependencies'] = check_dependencies()
    results['data'] = check_data_files()
    results['models'] = check_models()
    results['imports'] = check_imports()
    results['docker'] = check_docker()
    
    # Tests rapides
    run_quick_tests()
    
    # Résumé
    print_summary(results)

if __name__ == "__main__":
    main()