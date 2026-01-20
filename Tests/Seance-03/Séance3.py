#coding:utf8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Source des données : https://www.data.gouv.fr/datasets/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour/

# Sources des données : production de M. Forriez, 2016-2023

with open ("data/resultats-elections-presidentielles-2022-1er-tour.csv",encoding="utf-8") as fichier:
    contenu = pd.read_csv(fichier)

print(contenu)

#Question 5 et 6 

#Sélectionner uniquement les colonnes quantitatives 

colonnes_quantitatives = contenu.select_dtypes(include=np.number)
#Moyenne
moyennes = round(colonnes_quantitatives.mean(), 2).tolist()
# Médianes
medians = round(colonnes_quantitatives.median(), 2).tolist()
# Modes
modes = round(colonnes_quantitatives.mode().iloc[0], 2).tolist()
#Écart-type
ecarts_type = round(colonnes_quantitatives.std(), 2).tolist()
#Écart absolu à la moyenne
ecart_abs_moyenne = round((np.abs(colonnes_quantitatives - colonnes_quantitatives.mean())).mean(), 2).tolist()
#Étendue de chaque colonne
etendue = round(colonnes_quantitatives.max() - colonnes_quantitatives.min(), 2).tolist()

# Afficher 
print("Moyennes :", moyennes)
print("Médianes :", medians)
print("Modes :", modes)
print("Écart-type :", ecarts_type)
print("Écart absolu à la moyenne :", ecart_abs_moyenne)
print("Étendue :", etendue)

#Question 7: Calculer la distance interquartile et interdécile de chaque colonne quantitative

colonnes_quantitatives = contenu.select_dtypes(include=np.number)

#Distance interquartile
Q1 = colonnes_quantitatives.quantile(0.25)
Q3 = colonnes_quantitatives.quantile(0.75)
distance_interquartile = round((Q3 - Q1), 2).tolist()
# Distance interdécile
D1 = colonnes_quantitatives.quantile(0.1)
D9 = colonnes_quantitatives.quantile(0.9)
distance_interdecile = round((D9 - D1), 2).tolist()
# Affichage des résultats
print("Distance interquartile :", distance_interquartile)
print("Distance interdécile :", distance_interdecile)

#Question 8:  À l’aide de Matplolib et d’une boucle, faire des boîtes à moustache de chaque colonne quantitative. Stocker les résultats dans un dossier img.

colonnes_quantitatives = contenu.select_dtypes(include='number')

# Boucle
for col in colonnes_quantitatives.columns:
    plt.figure(figsize=(6,4))
    plt.boxplot(colonnes_quantitatives[col], vert=True, patch_artist=True)
    plt.title(f"Boîte à moustaches : {col}")
    plt.ylabel(col)
    
    # Enregistrer le graphique
    plt.savefig(f"img/boxplot_{col}.png")
    plt.close()
print("Boîtes à moustaches dans le dossier 'img'.")

#Question 9 importer le fichier data island 
with open ("Data/island-index.csv", encoding="utf-8") as fichier:
    contenu = pd.read_csv(fichier)
print(contenu)

#Question 10  Sélectionner la colonne « Surface (km2) » et écrire un algorithme pour catégoriser et  dénombrer le nombre d’îles ayant une surface comprise
df = pd.read_csv("data/island-index.csv", encoding="utf-8")
#sélectionner surface 
df_surface = df["Surface (km²)"]
# Définir intervalles et labels
bins = [0, 10, 25, 50, 100, 2500, 5000, 10000, float('inf')]
labels = ["0-10", "10-25", "25-50", "50-100", "100-2500", "2500-5000", "5000-10000", "10000+"]
categories = pd.cut(df_surface, bins=bins, labels=labels, right=True, include_lowest=True)
# Compter le nombre d'îles par catégorie
compte = categories.value_counts().sort_index()
print("Nombre d'îles par catégorie de surface :")
print(compte)
#Organigramme 

#lire fichier -> définir les colonnes -> surface (km2) -> définir en valeur numérique -> définir intervalle -> compter nombre d'ile -> résutat