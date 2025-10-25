import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

def clean_data(df, n_neighbors=5, remove_outliers=False):
    print(f" Taille initiale du dataset : {df.shape}\n")

    #  GESTION DES DOUBLONS
    print(" Vérification des doublons...")
    doublons = df.duplicated()
    if doublons.any():
        print(f" {doublons.sum()} doublons trouvés — suppression...")
        df = df.drop_duplicates()
        print(f" Nouvelle taille du dataset : {df.shape}\n")
    else:
        print(" Aucun doublon trouvé.\n")

    #  TRAITEMENT DES VALEURS MANQUANTES
    print(" Imputation des valeurs manquantes...\n")

    # Séparation des colonnes numériques et catégorielles
    df_num = df.select_dtypes(include=np.number)
    df_cat = df.select_dtypes(exclude=np.number)

    # --- Numériques (KNN Imputer) ---
    if df_num.isna().sum().any():
        print(" Colonnes numériques avec NaN (traitement KNN) :")
        print(df_num.isna().sum()[df_num.isna().sum() > 0])
        imputer = KNNImputer(n_neighbors=n_neighbors)
        df_num_imputed = pd.DataFrame(imputer.fit_transform(df_num),
                                      columns=df_num.columns,
                                      index=df.index)
        df[df_num.columns] = df_num_imputed
        print(f" Valeurs numériques imputées avec KNN (k={n_neighbors})\n")
    else:
        print(" Aucune valeur manquante dans les colonnes numériques.\n")

    # --- Catégorielles (mode) ---
    if df_cat.isna().sum().any():
        print(" Colonnes catégorielles avec NaN :")
        print(df_cat.isna().sum()[df_cat.isna().sum() > 0])
        for col in df_cat.columns:
            mode_value = df_cat[col].mode()[0] if not df_cat[col].mode().empty else "Inconnu"
            df[col].fillna(mode_value, inplace=True)
            print(f" {col} : remplacé les NaN par la valeur la plus fréquente ('{mode_value}')")
    else:
        print(" Aucune valeur manquante dans les colonnes catégorielles.\n")

    
    # 3️ SUPPRESSION DES VALEURS ABERRANTES
    print(" Détection et suppression des valeurs aberrantes (outliers)...\n")
    df_num = df.select_dtypes(include=np.number)

    initial_shape = df.shape
    total_removed = 0

    for col in df_num.columns:
        mean = df_num[col].mean()
        std = df_num[col].std()
        cut_off = 3 * std
        lower, upper = mean - cut_off, mean + cut_off

        mask_outliers = (df_num[col] < lower) | (df_num[col] > upper)
        outliers_count = mask_outliers.sum()

        if outliers_count > 0:
            print(f" {outliers_count} outliers supprimés dans '{col}'")
            df = df.loc[~mask_outliers, :]
            total_removed += outliers_count
        else:
            print(f" Aucun outlier dans '{col}'")

    print(f"\n Total {total_removed} lignes supprimées pour valeurs aberrantes.")
    print(f" Nouvelle taille du dataset : {df.shape}")
    print("\n Nettoyage complet terminé.\n")
    return df
