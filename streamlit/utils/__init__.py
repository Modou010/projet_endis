"""
Module utilitaires pour GreenTech Solutions
"""

# Import des modules existants
try:
    from . import data_loader
    from . import model_utils
except ImportError as e:
    print(f"Avertissement : Impossible d'importer certains modules existants : {e}")
    data_loader = None
    model_utils = None

# Import des nouveaux modules
try:
    from . import data_refresher
    from . import model_trainer
    from . import api_client
except ImportError as e:
    print(f"Avertissement : Impossible d'importer les nouveaux modules : {e}")
    data_refresher = None
    model_trainer = None
    api_client = None

__all__ = [
    'data_loader',
    'model_utils',
    'data_refresher',
    'model_trainer',
    'api_client'
]