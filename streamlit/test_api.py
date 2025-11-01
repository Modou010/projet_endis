"""
Script de test pour l'API FastAPI
Usage: python test_api.py
"""

import requests
import json
from typing import Dict, Any

# Configuration
API_BASE_URL = "http://localhost:8000"

def print_section(title: str):
    """Afficher une section"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def test_health():
    """Tester le health check"""
    print_section("🏥 Test Health Check")
    
    response = requests.get(f"{API_BASE_URL}/health")
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 200

def test_predict():
    """Tester la prédiction individuelle"""
    print_section("🔮 Test Prédiction Individuelle")
    
    data = {
        "conso_auxiliaires_ef": 500.0,
        "cout_eclairage": 80.0,
        "conso_5_usages_par_m2_ef": 200.0,
        "conso_5_usages_ef": 20000.0,
        "surface_habitable_logement": 100.0,
        "cout_ecs": 300.0,
        "type_batiment": "maison",
        "conso_ecs_ef": 2000.0,
        "conso_refroidissement_ef": 0.0,
        "type_energie_recodee": "Electricite"
    }
    
    print("📤 Données envoyées:")
    print(json.dumps(data, indent=2))
    print()
    
    response = requests.post(f"{API_BASE_URL}/predict", json=data)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ Prédiction réussie!")
        print(f"Étiquette DPE prédite: {result['etiquette_dpe']}")
        print(f"Coût total prédit: {result['cout_total_5_usages']:.2f} €")
        
        if result.get('probabilities'):
            print("\nProbabilités par classe:")
            for classe, proba in result['probabilities'].items():
                print(f"  {classe}: {proba*100:.2f}%")
    else:
        print(f"❌ Erreur: {response.text}")
    
    return response.status_code == 200

def test_batch_predict():
    """Tester les prédictions par lot"""
    print_section("📦 Test Prédictions par Lot")
    
    data = {
        "data": [
            {
                "conso_auxiliaires_ef": 500.0,
                "cout_eclairage": 80.0,
                "conso_5_usages_par_m2_ef": 200.0,
                "conso_5_usages_ef": 20000.0,
                "surface_habitable_logement": 100.0,
                "cout_ecs": 300.0,
                "type_batiment": "maison",
                "conso_ecs_ef": 2000.0,
                "conso_refroidissement_ef": 0.0,
                "type_energie_recodee": "Electricite"
            },
            {
                "conso_auxiliaires_ef": 300.0,
                "cout_eclairage": 60.0,
                "conso_5_usages_par_m2_ef": 150.0,
                "conso_5_usages_ef": 10000.0,
                "surface_habitable_logement": 70.0,
                "cout_ecs": 200.0,
                "type_batiment": "appartement",
                "conso_ecs_ef": 1500.0,
                "conso_refroidissement_ef": 0.0,
                "type_energie_recodee": "Gaz_naturel"
            }
        ]
    }
    
    print(f"📤 Nombre de logements: {len(data['data'])}")
    print()
    
    response = requests.post(f"{API_BASE_URL}/predict/batch", json=data)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ {result['total']} prédictions réussies!")
        
        for i, pred in enumerate(result['predictions']):
            print(f"\nLogement {i+1}:")
            print(f"  Étiquette DPE: {pred['etiquette_dpe']}")
            print(f"  Coût total: {pred['cout_total_5_usages']:.2f} €")
    else:
        print(f"❌ Erreur: {response.text}")
    
    return response.status_code == 200

def test_metrics():
    """Tester la récupération des métriques"""
    print_section("📊 Test Récupération des Métriques")
    
    response = requests.get(f"{API_BASE_URL}/models/metrics")
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        metrics = response.json()
        
        print("\n✅ Métriques récupérées!")
        
        if 'classification' in metrics:
            print("\n🎯 Classification:")
            print(f"  Accuracy: {metrics['classification']['accuracy']*100:.2f}%")
            print(f"  F1-Score: {metrics['classification']['f1_score']:.3f}")
            print(f"  Échantillons d'entraînement: {metrics['classification']['train_samples']:,}")
        
        if 'regression' in metrics:
            print("\n📈 Régression:")
            print(f"  R² Score: {metrics['regression']['r2_score']:.3f}")
            print(f"  MAE: {metrics['regression']['mae']:.2f} €")
            print(f"  RMSE: {metrics['regression']['rmse']:.2f} €")
            print(f"  Échantillons d'entraînement: {metrics['regression']['train_samples']:,}")
    else:
        print(f"❌ Erreur: {response.text}")
    
    return response.status_code == 200

def test_models_info():
    """Tester les informations sur les modèles"""
    print_section("ℹ️ Test Informations Modèles")
    
    response = requests.get(f"{API_BASE_URL}/models/info")
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 200

def main():
    """Exécuter tous les tests"""
    print("\n" + "🚀"*30)
    print("  TEST DE L'API GREENTECH SOLUTIONS")
    print("🚀"*30)
    
    tests = [
        ("Health Check", test_health),
        ("Prédiction Individuelle", test_predict),
        ("Prédictions par Lot", test_batch_predict),
        ("Métriques des Modèles", test_metrics),
        ("Informations Modèles", test_models_info),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ Erreur lors du test '{test_name}': {e}")
            results[test_name] = False
    
    # Résumé
    print_section("📋 RÉSUMÉ DES TESTS")
    
    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {total} tests")
    print(f"Réussis: {passed} ({passed/total*100:.1f}%)")
    print(f"Échoués: {failed} ({failed/total*100:.1f}%)")
    
    if failed == 0:
        print("\n🎉 Tous les tests sont passés avec succès!")
    else:
        print(f"\n⚠️ {failed} test(s) ont échoué. Vérifiez que l'API est bien lancée et que les modèles sont entraînés.")

if __name__ == "__main__":
    main()