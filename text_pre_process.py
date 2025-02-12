mp = {}  # Dictionnaire pour stocker les sections

romans = [
    'I', 'V', 'X'
]

with open("/content/file1.txt", "r") as file:
    lines = file.readlines()

str1 = ""  # Clé (titre)
str2 = ""  # Valeur (contenu)
map2 = {}
for line in lines:
    line = line.strip()  # Supprime les espaces et sauts de ligne

    if not line:  # Ignore les lignes vides
        continue

    first_word = line.split()[0]  # Premier mot de la ligne
    tst=0
    for x in first_word :
        if(x.isalpha() and x not in romans) :
          tst+=1
    # Vérifie si la ligne commence par un nombre romain
    if first_word[0] in romans and tst==0 :
        if str1:  # Sauvegarde l'ancienne section avant d'en commencer une nouvelle
            mp[str1] = str2.strip()
            
        map2[first_word] = line
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
