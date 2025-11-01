"""
Module des pages Streamlit
"""

# Import des pages existantes
try:
    from . import welcome
    from . import home
    from . import analysis
    from . import compare
    from . import about
    from . import enedis
    from . import prediction
except ImportError as e:
    print(f"Avertissement : Impossible d'importer certaines pages existantes : {e}")
    # Créer des modules vides pour éviter les erreurs
    class DummyModule:
        @staticmethod
        def show():
            import streamlit as st
            st.warning("Cette page n'est pas encore implémentée.")
    
    welcome = DummyModule()
    home = DummyModule()
    analysis = DummyModule()
    compare = DummyModule()
    about = DummyModule()
    enedis = DummyModule()
    prediction = DummyModule()

# Import des nouvelles pages
try:
    from . import refresh_data
    from . import retrain_models
    from . import api_interface
except ImportError:
    # Si les nouvelles pages ne sont pas encore créées, créer des modules vides
    class DummyModule:
        @staticmethod
        def show():
            import streamlit as st
            st.info("Cette page sera bientôt disponible.")
    
    refresh_data = DummyModule()
    retrain_models = DummyModule()
    api_interface = DummyModule()

__all__ = [
    'welcome',
    'home',
    'analysis',
    'compare',
    'about',
    'enedis',
    'prediction',
    'refresh_data',
    'retrain_models',
    'api_interface'
]