#coding:utf8

import pandas as pd
import matplotlib.pyplot as plt
import os
import pandas as pd


chemin_csv = os.path.join(
    os.path.dirname(__file__),  
    "data",                      
    "resultats-elections-presidentielles-2022-1er-tour.csv")

# Charger le CSV
contenu = pd.read_csv(chemin_csv, encoding="utf-8")
 
#Question 5: tableau 
print (contenu)
pd.DataFrame (contenu)

# Question 6: Nombre de lignes

nb_lignes= len(contenu)
#affichage 

#Nombre de colonnes 
nb_colonnes= len(contenu.columns)

print("nombre de lignes :",nb_lignes)
print("nombres de colonnes :",nb_colonnes)
types_colonnes = []

#Question 7: liste nature statistique des variables

for col in contenu.columns:
    dtype = contenu[col].dtype
    if pd.api.types.is_integer_dtype(dtype):
        types_colonnes.append('int')
    elif pd.api.types.is_float_dtype(dtype):
        types_colonnes.append('float')
    elif pd.api.types.is_bool_dtype(dtype):
        types_colonnes.append('bool')
    else:
        types_colonnes.append('str')

#Question 8:afficher sur le terminal le nom des colonne

print(contenu.dtypes)
print(contenu.columns)
print(contenu.head())

colonne_inscrits = contenu["Inscrits"]
print(colonne_inscrits)

#Question 9 : nombres d'inscrits 

print("\n=== Somme des colonnes quantitaives")
somme_colonnes = {} 

#Question 10 : calculer la somme des inscrits 

print("\n=== Somme des colonnes quantitatives ===")
somme_colonnes=[] 
for col in contenu.columns:
    if contenu[col].dtype in ["int64", "float64"]:
        somme_colonnes.append(contenu[col].sum())
print(somme_colonnes)

#Question 11 :

for i in range(len(contenu)): 
    dept= contenu.loc[i,"Libellé du département"]
    inscrits =contenu.loc[i, "Inscrits"]
    votants = contenu.loc[i, "Votants"]
    plt.figure(figsize=(6,4))
    plt.bar(["Inscrits","Votants"], [inscrits,votants],color= ["blue","red"])
    plt.title(f"{dept}")
    plt.ylabel("nombre de personnes")
    plt.ticklabel_format(style="plain",axis="y")
    plt.savefig(f"{dept}.png")
    plt.close()

# Question 12 : Diagrammes circulaires par département

import os 
os.makedirs("images_circulaires", exist_ok= True)

for i in range(len(contenu)):
    dept= contenu.loc [i, "Libellé du département"]
    blancs= contenu.loc[i, "Blancs"]
    nuls = contenu.loc[i, "Nuls"]
    votants = contenu.loc[i,"Votants"]
    abstention = contenu.loc [i, "Abstentions"]
    exprimés = votants - blancs - nuls
    valeurs = [blancs, nuls, exprimés, abstention]
    labels = ["blancs", "Nuls", "Exprimés", "Abstention"]
    couleurs = ["lightgrey", "red", "green", "orange"]
    plt.figure(figsize=(6,6))
    plt.pie(valeurs, labels = labels, colors =couleurs, autopct='%1.1f%%', startangle=90)
    plt.title(f"{dept}")
    #Sauvegarder
    plt.savefig(f"images_circulaires/{dept}.png")
    plt.close()


#Question 13 Histogramme

plt.figure(figsize=(8,5))
plt.hist(contenu["Inscrits"], bins=20, density=True, edgecolor = 'black', color= 'skyblue')
plt.title("Histogramme du nombre d'inscrits")
plt.xlabel("nombre d'inscrits")
plt.ylabel("densité")
plt.grid(alpha=0.3)
plt.show()