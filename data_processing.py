import os
import pandas as pd 

from charge_dossier_csv import charger_csv_dossier

dossier = "Actifs"
dataframes = charger_csv_dossier(dossier)

for nom_fichier in dataframes:
    chemin_complet = f"{dossier}/{nom_fichier}"

    # Assurer que le fichier est un fichier CSV avant de continuer
    if not nom_fichier.endswith('.csv'):
        continue

    data = pd.read_csv(chemin_complet, delimiter=";", skiprows=3)
    print("Chemin complet du fichier :", chemin_complet)
    # Renommage des colonnes et nettoyage des données
    data.columns = (data.columns.str.replace('Clôture.1', 'Cloture').str.replace('Clôture',
                                                                                 'Cloture_secteur').str.replace('€',
                                                                                                                '').str.strip())

    # Vérifier si la colonne 'Volume' existe
    if 'Volume' in data.columns:
        data['Volume'] = data['Volume'].str.replace(' ', '').replace(',', '').astype(int)
    else:
        print(f"La colonne 'Volume' n'existe pas dans le fichier {nom_fichier}")
        continue  # Passer au fichier suivant si 'Volume' n'existe pas

    data = data.rename(columns={'Cloture_secteur': 'Cloture_secteur', 'Cloture': 'Cloture'})

    # Nettoyage des valeurs numériques et conversion en float
    for col in ['Cloture_secteur', 'Cloture', 'Ouverture', 'Plus haut', 'Plus bas', "Taux de Variation Mensuelle",
                "Taux de variation du marché", "Variance de la rentabilité du marché", "Covarience Actif marché"]:
        if col in data.columns:
            data[col] = data[col].str.replace('€', '').str.replace(',', '.').str.strip()
            data[col] = pd.to_numeric(data[col], errors='coerce')

    # Arrondir les valeurs numériques à quatre décimales
    data = data.round(4)
    # Convertir les données numériques et arrondir
    # data.iloc[:, 7:11] = data.iloc[:, 7:11].apply(pd.to_numeric, errors='coerce').round(4)

    # Conversion de la colonne 'Date' au format datetime
    data["Date"] = pd.to_datetime(data["Date"], format="%d/%m/%Y")

    # Suppression des colonnes non nécessaires
    data = data.drop(columns=[col for col in ["Taux de Variation Trimestrielle", "Taux de Variation Annuelle"] if
                              col in data.columns])
    data.fillna(0.0, inplace=True)
    # Déduire le nom de l'entreprise à partir du nom du fichier
    nom_entreprise = nom_fichier.split("_")[1].split(".")[0].capitalize()
    data["Entreprise"] = nom_entreprise

    # Vérification des modifications
    type_data = data.dtypes
    print(type_data)

    # Sauvegardez le DataFrame modifié dans un nouveau sous-dossier pour éviter l'écrasement
    dossier_sauvegarde = f"{dossier}_modifie"
    os.makedirs(dossier_sauvegarde, exist_ok=True)
    nom_fichier_modifie = nom_fichier.replace(".csv", "_modifie.csv")
    chemin_sauvegarde = f"{dossier_sauvegarde}/{nom_fichier_modifie}"

    if not os.path.exists(chemin_sauvegarde):
        data.to_csv(chemin_sauvegarde, index=False, sep=";", encoding='utf-8', date_format='%d/%m/%Y')
    else:
        print(f"Le fichier {nom_fichier_modifie} existe déjà.")

