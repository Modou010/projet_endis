def predict_dpe(data: dict):
    """Exemple de fonction de prédiction simplifiée."""
    # Simulation d’un modèle
    score = (
        data["conso_chauffage_ef"]
        + data["conso_ecs_ef"]
        + data["conso_eclairage_ef"]
    ) / data["surface_habitable_logement"]

    if score < 100:
        label = "A"
    elif score < 150:
        label = "B"
    elif score < 200:
        label = "C"
    elif score < 250:
        label = "D"
    elif score < 300:
        label = "E"
    else:
        label = "F"

    confidence = max(0.5, 1.0 - (score / 1000))
    return label, confidence
