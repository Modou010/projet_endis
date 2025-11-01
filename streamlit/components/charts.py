import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    """Charge un jeu de données local ou factice."""
    # Simule un DataFrame pour l’exemple
    data = {
        "id_logement": [f"L{i}" for i in range(1, 6)],
        "type_batiment": ["maison", "appartement", "maison", "appartement", "maison"],
        "conso_5_usages_par_m2_ef": [150, 120, 200, 100, 180],
        "cout_total_5_usages": [2000, 1500, 2500, 1300, 2200],
        "emission_ges_5_usages": [80, 60, 90, 50, 85],
    }
    return pd.DataFrame(data)

def plot_conso_distribution(df):
    fig, ax = plt.subplots()
    ax.hist(df["conso_5_usages_par_m2_ef"], bins=10)
    ax.set_xlabel("Consommation (kWh EF/m²)")
    ax.set_ylabel("Nombre de logements")
    ax.set_title("Distribution des consommations")
    return fig

def plot_emission_by_type(df):
    fig, ax = plt.subplots()
    df.groupby("type_batiment")["emission_ges_5_usages"].mean().plot(kind="bar", ax=ax)
    ax.set_ylabel("Émissions moyennes (kgCO₂/m²)")
    ax.set_title("Émissions moyennes par type de bâtiment")
    return fig
