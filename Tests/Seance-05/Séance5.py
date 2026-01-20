#coding:utf8

import pandas as pd
import math
import scipy
import scipy.stats
import os
print("Répertoire courant :", os.getcwd())
import os
os.chdir(r"./")
print("Répertoire courant :", os.getcwd())

#C'est la partie la plus importante dans l'analyse de données. D'une part, elle n'est pas simple à comprendre tant mathématiquement que pratiquement. D'autre, elle constitue une application des probabilités. L'idée consiste à comparer une distribution de probabilité (théorique) avec des observations concrètes. De fait, il faut bien connaître les distributions vues dans la séance précédente afin de bien pratiquer cette comparaison. Les probabilités permettent de définir une probabilité critique à partir de laquelle les résultats ne sont pas conformes à la théorie probabiliste.
#Il n'est pas facile de proposer des analyses de données uniquement dans un cadre univarié. Vous utiliserez la statistique inférentielle principalement dans le cadre d'analyses multivariées. La statistique univariée est une statistique descriptive. Bien que les tests y soient possibles, comprendre leur intérêt et leur puissance d'analyse dans un tel cadre peut être déroutant.
#Peu importe dans quelle théorie vous êtes, l'idée de la statistique inférentielle est de vérifier si ce que vous avez trouvé par une méthode de calcul est intelligent ou stupide. Est-ce que l'on peut valider le résultat obtenu ou est-ce que l'incertitude qu'il présente ne permet pas de conclure ? Peu importe également l'outil, à chaque mesure statistique, on vous proposera un test pour vous aider à prendre une décision sur vos résultats. Il faut juste être capable de le lire.

#Par convention, on place les fonctions locales au début du code après les bibliothèques.
def ouvrirUnFichier(nom):
    with open(nom, "r") as fichier:
        contenu = pd.read_csv(fichier)
    return contenu

#Théorie de l'échantillonnage (intervalles de fluctuation)

#Ouverture du fichier
fichier = r"./data/Echantillonnage-100-Echantillons.csv"  # chemin relatif vers le fichier
echantillons = ouvrirUnFichier(fichier)

print("Résultat sur le calcul d'un intervalle de fluctuation")

#moyennes par colonne
moyennes_colonnes = echantillons.mean()

#Arrondir les moyennes à 0 décimale
moyennes_arrondies = moyennes_colonnes.round(0)
print("\nMoyennes arrondies des 3 opinions :")
print(moyennes_arrondies)

#Calcul des fréquences issues des moyennes
somme_moyennes = moyennes_arrondies.sum()
frequences_echantillons = (moyennes_arrondies / somme_moyennes).round(2)
print("\nFréquences estimées à partir des moyennes :")
print(frequences_echantillons)

#Taille échantillon 
n = echantillons.iloc[0].sum()

# Intervalle de fluctuation à 95% 
zC = 1.96
intervalle_fluctuation = {}
for opinion, f in frequences_echantillons.items():
    ecart = zC * math.sqrt(f * (1 - f) / n)
    intervalle_fluctuation[opinion] = (round(f - ecart, 2), round(f + ecart, 2))

# Fréquences de la population mère
population_mere = pd.Series([852, 911, 422], index=["Pour", "Contre", "Sans opinion"])
frequences_mere = (population_mere / population_mere.sum()).round(2)
print("\nFréquences de la population mère :")
print(frequences_mere)

#Comparaison échantillons vs population mère
comparaison = pd.DataFrame({
    "Échantillons": frequences_echantillons,
    "Population mère": frequences_mere})
print("\nComparaison (échantillons vs population mère) :")
print(comparaison)

# Affichage des intervalles de fluctuation
print("\nIntervalle de fluctuation à 95% pour chaque opinion :")
for opinion, (inf, sup) in intervalle_fluctuation.items():
    print(f"{opinion} : [{inf} ; {sup}]")



print("Résultat sur le calcul d'un intervalle de confiance")
print("Théorie de la décision")

#Théorie de l'estimation (intervalles de confiance)
#L'estimation se base sur l'effectif.
print("Résultat sur le calcul d'un intervalle de confiance")

# Premier échantillon et intervalle de confiance
premier_echantillon = list(echantillons.iloc[0])
n_premier = sum(premier_echantillon)

frequences_premier = [round(x / n_premier, 2) for x in premier_echantillon]
opinions = echantillons.columns
frequences_premier_dict = dict(zip(opinions, frequences_premier))

print("\nFréquences du premier échantillon :")
for opinion, f in frequences_premier_dict.items():
    print(f"{opinion} : {f}")

zC = 1.96
intervalle_confiance = {}
for opinion, f in frequences_premier_dict.items():
    ecart = zC * math.sqrt(f * (1 - f) / n_premier)
    intervalle_confiance[opinion] = (round(f - ecart, 2), round(f + ecart, 2))

print("\nIntervalle de confiance à 95% pour le premier échantillon :")
for opinion, (inf, sup) in intervalle_confiance.items():
    print(f"{opinion} : [{inf} ; {sup}]")

# Théorie de la décision (tests d'hypothèse)
print("Théorie de la décision")


#Théorie de la décision (tests d'hypothèse)
print("Théorie de la décision")


# Test de normalité avec Shapiro‑Wilk

from scipy.stats import shapiro

fichier1 = "./data/Loi-normale-Test-1.csv"
fichier2 = "./data/Loi-normale-Test-2.csv"

donnees1 = pd.read_csv(fichier1)
donnees2 = pd.read_csv(fichier2)

serie1 = donnees1.iloc[:, 0].tolist()
serie2 = donnees2.iloc[:, 0].tolist()

# Test de Shapiro‑Wilk
stat1, p1 = shapiro(serie1)
stat2, p2 = shapiro(serie2)

print("\nShapiro‑Wilk for Loi‑normale‑Test‑1.csv :")
print(f"Statistic = {stat1:.4f}, p‑value = {p1:.4f}")
if p1 > 0.05:
    print("-> On ne rejette pas H0 : distribution normale possible.")
else:
    print("-> On rejette H0 : distribution non normale.")

#La décision se base sur la notion de risques alpha et bêta.
#Comme à la séance précédente, l'ensemble des tests se trouve au lien : https://docs.scipy.org/doc/scipy/reference/stats.html
print("Théorie de la décision")
