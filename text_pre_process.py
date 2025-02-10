mp = {}  # Dictionnaire pour stocker les sections

romans = [
    'I', 'V', 'X'
]

with open("/content/file.txt", "r") as file:
    lines = file.readlines()

str1 = ""  # Clé (titre)
str2 = ""  # Valeur (contenu)

for line in lines:
    line = line.strip()  # Supprime les espaces et sauts de ligne

    if not line:  # Ignore les lignes vides
        continue

    first_word = line.split()[0]  # Premier mot de la ligne

    # Vérifie si la ligne commence par un nombre romain
    if first_word[0] in romans:
        if str1:  # Sauvegarde l'ancienne section avant d'en commencer une nouvelle
            mp[str1] = str2.strip()
        str1 = line  # Nouveau titre
        str2 = ""  # Réinitialise le contenu
    else:
        str2 += line + "\n"  # Ajoute la ligne au contenu

# Ajouter la dernière section après la boucle
if str1:
    mp[str1] = str2.strip()

# Affichage du dictionnaire
for x, y in mp.items():
    print(f"partie {x} : {y}\n")
