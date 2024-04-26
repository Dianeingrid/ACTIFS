import pandas as pd
from charge_dossier_csv import charger_csv_dossier

dossier = "Actifs_modifie"
dataframes = charger_csv_dossier(dossier)

for nom_fichier, dataframe in dataframes.items():
    nom_entreprise = nom_fichier.split('Actif_')[-1].split('_modifie')[0].capitalize()
    dataframe['Date'] = pd.to_datetime(dataframe['Date'],dayfirst=True)
    dataframe['Année'] = dataframe['Date'].dt.year
    dataframe['Trimestre'] = dataframe['Date'].dt.to_period('Q')
    rendements_trimestriels = dataframe.groupby(['Année', 'Trimestre']) ['Taux de Variation Mensuelle'].apply(
    lambda x: (1 + x).prod() -1).reset_index(name='Rendement Trimestriels')
    rendements_Annuels = dataframe.groupby(['Année']) ['Taux de Variation Mensuelle'].apply(
    lambda x: (1 + x).prod() -1).reset_index(name='Rendement Annuels')
    
print(rendements_trimestriels)

chemin_fichier_trimestriels = f'Taux/{nom_entreprise}/rendements_trimestriels_{nom_entreprise}.csv'
chemin_fichier_annuels = f'Taux/{nom_entreprise}/rendement_annuels_{nom_entreprise}.csv'

rendements_trimestriels.to_csv(chemin_fichier_trimestriels,index=False,sep=';')
rendements_Annuels.to_csv(chemin_fichier_annuels, index=False, sep=';')

