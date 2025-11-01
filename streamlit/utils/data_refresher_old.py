import requests
import pandas as pd
import os
import json
from datetime import datetime, timedelta
import time
from typing import Optional, List, Tuple

class DataRefresher:
    """Classe pour rafraîchir les données DPE depuis l'API ADEME"""
    
    BASE_URL = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe03existant/lines"
    METADATA_FILE = "data/metadata.json"
    DATA_FILE = "data/donnees_ademe_finales_nettoyees_69_final_pret.csv"
    
    # Colonnes à extraire (identiques à ton script initial)
    COLUMNS = [
        "configuration_installation_chauffage_n1", "conso_chauffage_installation_chauffage_n1",
        "type_generateur_n1_ecs_n1", "numero_voie_ban", "score_ban", "surface_habitable_immeuble",
        "conso_auxiliaires_ep", "deperditions_murs", "cout_eclairage", "conso_auxiliaires_ef",
        "statut_geocodage", "ventilation_posterieure_2012", "cout_chauffage", "conso_5_usages_par_m2_ep",
        "date_etablissement_dpe", "conso_ecs_ef_energie_n1", "conso_ecs_ef_energie_n2",
        "emission_ges_chauffage", "description_installation_chauffage_n1", "conso_5_usages_par_m2_ef",
        "cout_ecs_energie_n2", "conso_chauffage_ef_energie_n1", "conso_chauffage_ef_energie_n2",
        "qualite_isolation_menuiseries", "cout_total_5_usages_energie_n2", "date_reception_dpe",
        "cout_total_5_usages_energie_n1", "cout_ecs_energie_n1", "qualite_isolation_plancher_bas",
        "modele_dpe", "qualite_isolation_enveloppe", "conso_chauffage_generateur_n1_installation_n1",
        "type_energie_n1", "emission_ges_eclairage", "type_energie_n2", "code_postal_ban",
        "emission_ges_ecs", "conso_5_usages_ef_energie_n2", "conso_5_usages_ef",
        "conso_5_usages_ef_energie_n1", "code_insee_ban", "deperditions_planchers_bas",
        "conso_5_usages_ep", "date_fin_validite_dpe", "deperditions_enveloppe", "code_region_ban",
        "volume_stockage_generateur_n1_ecs_n1", "surface_chauffee_installation_chauffage_n1",
        "version_dpe", "besoin_ecs", "coordonnee_cartographique_x_ban",
        "type_generateur_chauffage_principal", "type_energie_principale_ecs",
        "apport_solaire_saison_chauffe", "adresse_ban", "nombre_appartement",
        "deperditions_renouvellement_air", "_rand", "surface_habitable_desservie_par_installation_ecs_n1",
        "production_electricite_pv_kwhep_par_an", "type_installation_chauffage",
        "nombre_niveau_logement", "surface_habitable_logement", "cout_ecs", "type_installation_ecs_n1",
        "emission_ges_5_usages_energie_n1", "emission_ges_5_usages_energie_n2",
        "apport_interne_saison_froide", "emission_ges_5_usages_par_m2",
        "description_generateur_chauffage_n1_installation_n1",
        "qualite_isolation_plancher_haut_comble_perdu", "apport_interne_saison_chauffe",
        "apport_solaire_saison_froide", "type_generateur_n1_installation_n1",
        "nombre_logements_desservis_par_installation_ecs_n1", "complement_adresse_logement",
        "cout_auxiliaires", "type_emetteur_installation_chauffage_n1", "besoin_chauffage",
        "configuration_installation_ecs_n1", "description_installation_ecs_n1",
        "classe_inertie_batiment", "deperditions_ponts_thermiques",
        "type_generateur_chauffage_principal_ecs", "emission_ges_refroidissement",
        "hauteur_sous_plafond", "conso_chauffage_ef", "nom_commune_ban", "annee_construction",
        "_geopoint", "date_visite_diagnostiqueur", "type_batiment", "periode_construction",
        "type_installation_ecs", "conso_ecs_ep", "conso_ecs_ef", "emission_ges_5_usages",
        "date_derniere_modification_dpe", "etiquette_ges", "identifiant_ban",
        "deperditions_baies_vitrees", "type_energie_generateur_n1_ecs_n1", "ubat_w_par_m2_k",
        "numero_etage_appartement", "nom_commune_brut", "conso_ef_installation_ecs_n1",
        "etiquette_dpe", "description_generateur_n1_ecs_n1", "code_departement_ban",
        "type_installation_chauffage_n1", "methode_application_dpe", "adresse_brut",
        "cout_total_5_usages", "categorie_enr", "conso_refroidissement_ef", "conso_eclairage_ef",
        "deperditions_planchers_hauts", "zone_climatique", "conso_ef_generateur_n1_ecs_n1",
        "emission_ges_ecs_energie_n1", "emission_ges_ecs_energie_n2", "cout_refroidissement",
        "conso_chauffage_ep", "conso_eclairage_ep", "usage_generateur_n1_installation_n1",
        "nom_rue_ban", "qualite_isolation_murs", "type_installation_solaire_n1", "classe_altitude",
        "conso_refroidissement_ep", "type_energie_principale_chauffage", "numero_dpe", "_i",
        "besoin_refroidissement", "emission_ges_chauffage_energie_n2",
        "emission_ges_chauffage_energie_n1", "cout_chauffage_energie_n2", "deperditions_portes",
        "cout_chauffage_energie_n1", "coordonnee_cartographique_y_ban",
        "type_energie_generateur_n1_installation_n1", "code_postal_brut", "emission_ges_auxiliaires",
        "usage_generateur_n1_ecs_n1"
    ]
    
    def __init__(self, codes_postaux_file: str = "data/adresses-69.csv"):
        """Initialiser le refresher avec le fichier des codes postaux"""
        self.codes_postaux_file = codes_postaux_file
        self.codes_postaux = self._load_codes_postaux()
        
    def _load_codes_postaux(self) -> List[str]:
        """Charger les codes postaux du département 69"""
        if not os.path.exists(self.codes_postaux_file):
            # Si le fichier n'existe pas, utiliser les codes postaux du Rhône par défaut
            return [f"69{i:03d}" for i in range(1, 300)]
        
        df = pd.read_csv(self.codes_postaux_file, dtype=str, sep=';')
        return df['code_postal'].unique().tolist()
    
    def get_last_update_date(self) -> Optional[str]:
        """Récupérer la date de dernière mise à jour depuis les métadonnées"""
        if not os.path.exists(self.METADATA_FILE):
            return None
        
        try:
            with open(self.METADATA_FILE, 'r') as f:
                metadata = json.load(f)
                return metadata.get('last_update_date')
        except Exception as e:
            print(f"Erreur lecture metadata: {e}")
            return None
    
    def save_metadata(self, last_date: str, total_records: int):
        """Sauvegarder les métadonnées de mise à jour"""
        os.makedirs(os.path.dirname(self.METADATA_FILE), exist_ok=True)
        
        metadata = {
            'last_update_date': last_date,
            'last_refresh': datetime.now().isoformat(),
            'total_records': total_records,
            'codes_postaux': self.codes_postaux
        }
        
        with open(self.METADATA_FILE, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def fetch_data_smart(self, code_postal: str, etiquette: Optional[str] = None,
                        start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[dict]:
        """
        Récupérer les données de manière intelligente avec découpage si nécessaire
        (Reprise de ta logique existante)
        """
        results = []
        size = 1000
        page = 1
        
        # Construction du filtre
        q_parts = [f"code_postal_ban:{code_postal}"]
        if etiquette:
            q_parts.append(f"etiquette_dpe:{etiquette}")
        if start_date and end_date:
            q_parts.append(f"date_reception_dpe:[{start_date} TO {end_date}]")
        q_filter = " AND ".join(q_parts)
        
        # Première requête pour connaître le total
        params = {
            "page": 1,
            "size": size,
            "qs": q_filter,
            "select": ",".join(self.COLUMNS),
            "q_fields": "code_postal_ban,etiquette_dpe,date_reception_dpe"
        }
        
        response = requests.get(self.BASE_URL, params=params)
        if response.status_code != 200:
            return results
        
        data = response.json()
        total = data.get("total", 0)
        
        # Si total > 10000 et pas filtré par étiquette
        if total > 10000 and etiquette is None:
            etiquettes = ["A", "B", "C", "D", "E", "F", "G"]
            for etiq in etiquettes:
                results.extend(self.fetch_data_smart(code_postal, etiquette=etiq))
            return results
        
        # Si total > 10000 et filtré par étiquette mais pas par date
        if total > 10000 and etiquette is not None and start_date is None:
            current_year = datetime.now().year
            for year in range(2021, current_year + 1):
                year_start = f"{year}-01-01"
                year_end = f"{year}-12-31"
                results.extend(self.fetch_data_smart(code_postal, etiquette, year_start, year_end))
            return results
        
        # Récupération normale par page
        while True:
            params["page"] = page
            response = requests.get(self.BASE_URL, params=params)
            if response.status_code != 200:
                break
            
            page_results = response.json().get("results", [])
            if not page_results:
                break
            
            results.extend(page_results)
            
            if len(page_results) < size:
                break
            
            page += 1
            time.sleep(0.5)  # Respecter l'API
        
        return results
    
    def refresh_new_data(self, progress_callback=None) -> Tuple[pd.DataFrame, int]:
        """
        Rafraîchir uniquement les nouvelles données depuis la dernière mise à jour
        
        Returns:
            Tuple[pd.DataFrame, int]: (nouvelles données, nombre de nouveaux enregistrements)
        """
        last_update = self.get_last_update_date()
        
        if last_update:
            # Récupérer uniquement depuis la dernière date
            start_date = (datetime.fromisoformat(last_update) + timedelta(days=1)).strftime("%Y-%m-%d")
        else:
            # Si première fois, récupérer les 3 derniers mois
            start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
        
        end_date = datetime.now().strftime("%Y-%m-%d")
        
        all_results = []
        total_codes = len(self.codes_postaux)
        
        for idx, cp in enumerate(self.codes_postaux):
            if progress_callback:
                progress_callback(idx + 1, total_codes, cp)
            
            # Ajouter le filtre de date dans la requête
            results = self.fetch_new_records(cp, start_date, end_date)
            all_results.extend(results)
        
        if not all_results:
            return pd.DataFrame(), 0
        
        new_df = pd.DataFrame(all_results)
        
        # Sauvegarder la nouvelle date de mise à jour
        if len(new_df) > 0:
            self.save_metadata(end_date, len(new_df))
        
        return new_df, len(new_df)
    
    def fetch_new_records(self, code_postal: str, start_date: str, end_date: str) -> List[dict]:
        """Récupérer uniquement les nouveaux enregistrements pour un code postal"""
        results = []
        size = 1000
        page = 1
        
        q_filter = f"code_postal_ban:{code_postal} AND date_reception_dpe:[{start_date} TO {end_date}]"
        
        while True:
            params = {
                "page": page,
                "size": size,
                "qs": q_filter,
                "select": ",".join(self.COLUMNS),
                "q_fields": "code_postal_ban,date_reception_dpe"
            }
            
            response = requests.get(self.BASE_URL, params=params)
            if response.status_code != 200:
                break
            
            page_results = response.json().get("results", [])
            if not page_results:
                break
            
            results.extend(page_results)
            
            if len(page_results) < size:
                break
            
            page += 1
            time.sleep(0.5)
        
        return results
    
    def merge_with_existing(self, new_df: pd.DataFrame) -> pd.DataFrame:
        """Fusionner les nouvelles données avec les données existantes"""
        if not os.path.exists(self.DATA_FILE):
            return new_df
        
        existing_df = pd.read_csv(self.DATA_FILE)
        
        # Concaténer et supprimer les doublons basés sur numero_dpe
        if 'numero_dpe' in new_df.columns and 'numero_dpe' in existing_df.columns:
            merged_df = pd.concat([existing_df, new_df], ignore_index=True)
            merged_df = merged_df.drop_duplicates(subset=['numero_dpe'], keep='last')
        else:
            merged_df = pd.concat([existing_df, new_df], ignore_index=True)
        
        return merged_df
    
    def save_refreshed_data(self, df: pd.DataFrame, backup: bool = True):
        """Sauvegarder les données rafraîchies"""
        os.makedirs(os.path.dirname(self.DATA_FILE), exist_ok=True)
        
        # Créer une sauvegarde si demandé
        if backup and os.path.exists(self.DATA_FILE):
            backup_file = f"{self.DATA_FILE}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.rename(self.DATA_FILE, backup_file)
        
        df.to_csv(self.DATA_FILE, index=False, encoding='utf-8')