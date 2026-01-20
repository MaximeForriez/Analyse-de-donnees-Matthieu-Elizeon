#coding:utf8
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import scipy.stats
import math
from scipy.stats import spearmanr, kendalltau

#Fonction pour ouvrir les fichiers
def ouvrirUnFichier(nom):
    with open(nom, "r", encoding="latin1") as fichier:

        contenu = pd.read_csv(fichier)
    return contenu
import os

#Convertir les données en données logarithmiques
def conversionLog(liste):
    log = []
    for element in liste:
        log.append(math.log(element))
    return log

#Trier par ordre décroissant les listes (îles et populations)
def ordreDecroissant(liste):
    liste.sort(reverse=True)
    return liste

#Obtenir le classement des listes spécifiques aux populations
def ordrePopulation(pop, etat):
    ordrepop = []
    for element in range(0, len(pop)):
        if not np.isnan(pop[element]):
            ordrepop.append([float(pop[element]), etat[element]])
    ordrepop = ordreDecroissant(ordrepop)
    for element in range(0, len(ordrepop)):
        ordrepop[element] = [element + 1, ordrepop[element][1]]
    return ordrepop

# Obtenir l'ordre défini entre deux classements
def classementPays(ordre1, ordre2):
    classement = []
    if len(ordre1) <= len(ordre2):
        for element1 in range(0, len(ordre2) - 1):
            for element2 in range(0, len(ordre1) - 1):
                if ordre2[element1][1] == ordre1[element2][1]:
                    classement.append([ordre1[element2][0], ordre2[element1][0], ordre1[element2][1]])
    else:
        for element1 in range(0, len(ordre1) - 1):
            for element2 in range(0, len(ordre2) - 1):
                if ordre2[element2][1] == ordre1[element1][1]:
                    classement.append([ordre1[element1][0], ordre2[element2][0], ordre1[element1][1]])
    return classement


# Partie sur les îles

chemin_fichier = os.path.join(os.path.dirname(__file__), "data", "island-index.csv")
print("Répertoire courant :", os.getcwd())

os.chdir(r"./")
print("Répertoire courant :", os.getcwd())

iles = ouvrirUnFichier(chemin_fichier)
print(iles)

iles = iles.rename(columns={"Surface (kmÂ²)": "Surface (km2)"})

# Isoler la colonne "Surface (km2)" et caster en liste Python
surface = list(iles["Surface (km2)"])

# Forcer le typage en float
surface = [float(valeur) for valeur in surface]

# Ajouter les surfaces des continents (sans unité)
surface.append(float(85545323))  # Asie / Afrique / Europe
surface.append(float(37856841))  # Amérique
surface.append(float(7768030))   # Antarctique
surface.append(float(7605049))   # Australie

# 4. Ordonnancement décroissant avec la fonction locale
surface_ord = ordreDecroissant(surface)


# 5 & 6. Loi rang–taille avec conversion logarithmique

# Création des rangs
rangs = list(range(1, len(surface_ord) + 1))

# Conversion en logarithme
log_surface = conversionLog(surface_ord)
log_rangs = conversionLog(rangs)

# Tracé de la loi rang–taille
plt.figure()
plt.scatter(log_rangs, log_surface)
plt.xlabel("log(Rang)")
plt.ylabel("log(Surface)")
plt.title("Loi rang–taille (axes logarithmiques)")
plt.grid(True)

plt.savefig("loi_rang_taille_log.png")
plt.show()

#Partie sur le monde 


chemin_monde = os.path.join(os.path.dirname(__file__), "data", "Le-Monde-HS-Etats-du-monde-2007-2025.csv")
monde = pd.read_csv(chemin_monde, encoding="latin1")  # encoding pour éviter les caractères bizarres

# J'avais un message d'erreur a cause d'accents en trop
monde.columns = [c.strip().replace('Ã©','e').replace('Ã\x89','E').replace('Ã','') for c in monde.columns]

# isoler colonnes
colonnes_a_isoler = ["Etat", "Pop 2007", "Pop 2025", "Densite 2007", "Densite 2025"]

# Création d'un DataFrame avec uniquement ces colonnes
monde_isole = monde[colonnes_a_isoler]

# Extraire les listes
etats = list(monde_isole["Etat"])
pop_2007 = list(monde_isole["Pop 2007"])
pop_2025 = list(monde_isole["Pop 2025"])
densite_2007 = list(monde_isole["Densite 2007"])
densite_2025 = list(monde_isole["Densite 2025"])

# Appliquer la fonction ordrePopulation pour trier en ordre décroissant
ordre_pop_2007 = ordrePopulation(pop_2007, etats)
ordre_pop_2025 = ordrePopulation(pop_2025, etats)
ordre_densite_2007 = ordrePopulation(densite_2007, etats)
ordre_densite_2025 = ordrePopulation(densite_2025, etats)


print("Top 5 pays par population 2007 :", ordre_pop_2007[:5])
print("Top 5 pays par population 2025 :", ordre_pop_2025[:5])
print("Top 5 pays par densité 2007 :", ordre_densite_2007[:5])
print("Top 5 pays par densité 2025 :", ordre_densite_2025[:5])

# Comparer le classement de la population entre 2007 et 2025
classement_population = classementPays(ordre_pop_2007, ordre_pop_2025)
classement_population.sort(key=lambda x: x[0])  # Tri par rang 2007

print("Comparaison des classements population 2007 vs 2025 (top 5) :")
print(classement_population[:5])

# Comparer le classement de la densité entre 2007 et 2025
classement_densite = classementPays(ordre_densite_2007, ordre_densite_2025)
classement_densite.sort(key=lambda x: x[0])  # Tri par rang 2007


print("Comparaison des classements densité 2007 vs 2025 (top 5) :")
print(classement_densite[:5])

# Extraire les rangs pour les colonnes population et densité
rangs_pop = [x[0] for x in classement_population]     
rangs_densite = [x[1] for x in classement_population]

# Calcul du coefficient de Spearman
spearman_corr, spearman_p = spearmanr(rangs_pop, rangs_densite)

# Calcul du coefficient de Kendall
kendall_corr, kendall_p = kendalltau(rangs_pop, rangs_densite)

# Afficher les resultats 
print(f"Corrélation des rangs (Spearman) : {spearman_corr:.4f}, p-value = {spearman_p:.4e}")
print(f"Concordance des rangs (Kendall) : {kendall_corr:.4f}, p-value = {kendall_p:.4e}")



