import matplotlib.pyplot as plt
from charge_dossier_csv import *

dossier = "Actifs_modifie"
dataframes = charger_csv_dossier(dossier)

for nom_fichier, dataframe in dataframes.items():
    dataframe['Date'] = pd.to_datetime(dataframe['Date'], dayfirst=True)

    describes_stats = dataframe[['Ouverture', 'Cloture', 'Plus haut', 'Plus bas']].describe()
    print(describes_stats)

    nom_entreprise = nom_fichier.split('Actif_')[-1].split('_modifie')[0].capitalize()

    plt.figure(figsize=(14,8))
    plt.plot(dataframe['Date'], dataframe['Cloture'],label='Cloture',color='blue')
    plt.plot(dataframe['Date'], dataframe['Ouverture'],label='Ouverture',color='green')
    plt.plot(dataframe['Date'], dataframe['Plus haut'],label='Plus haut',color='red')
    plt.plot(dataframe['Date'], dataframe['Plus bas'],label='Plus bas',color='purple')
    plt.title(f"evolution du prix de l'action {nom_entreprise} au fil du temps")
    plt.xlabel('Date')
    plt.ylabel("prix de l'action")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()