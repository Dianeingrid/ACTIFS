import pandas as pd
import os 
from pandas import DataFrame

def charger_csv_dossier(dossier):
    fichiers_dataframes = {}
    fichiers = os.listdir(dossier)

    for nom_fichier in fichiers: 
        chemin_complet = os.path.join( dossier, nom_fichier)
        if os.path.isfile(chemin_complet) and nom_fichier.endswith('.csv'): 
            data: DataFrame = pd.read_csv(chemin_complet, delimiter=';')
            fichiers_dataframes[nom_fichier] = data
    return fichiers_dataframes        