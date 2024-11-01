import subprocess


def couper (nomDossier, debut, fin):

    # Noms de tous les fichiers
    sortie = commande ('dir "' + nomDossier + '" /b /s')
    nomElements = list (sortie. split ("\\r\\n"))
    nomFichiers = [
        element. replace ("\\\\", "/")
        for element in nomElements
        if "." in element
    ]
    
    for nomFichier in nomFichiers:
        
        # Durée du fichier
        sortie = commande ('ffprobe "' + nomFichier + '" -show_entries format=duration -of compact=p=0:nk=1 -v 0 -sexagesimal')
        duree = soustraction (sortie. removesuffix ("000"), fin)
        
        # Format du fichier
        format = "." + list (nomFichier. split (".")) [-1]
        
        # Coupe de la vidéo
        nouveauNom = nomFichier. removesuffix (format) + " [Trimmed]" + format
        commande ('ffmpeg -y -i "' + nomFichier + '" -c:v copy -c:a copy -ss ' + debut + ' -to ' + duree + ' "' + nouveauNom + '"')
        print (nouveauNom)


def commande (appel):

    resultat = subprocess. run (appel, capture_output = True, shell = True)
    sortie = str (resultat. stdout). removeprefix ("b'"). removesuffix ("\\r\\n'")
    
    return sortie


def soustraction (baseAffichage, substitutAffichage):

    # Initialisation
    base      = list (map (float, baseAffichage.      split (":")))
    substitut = list (map (float, substitutAffichage. split (":")))
    resultat  = [0] * 3
    
    # Calcul
    for unite in range (3):
        resultat [unite] = base [unite] - substitut [unite]
    
    # Secondes
    if resultat [2] < 0:
        resultat [2] += 60
        resultat [1] -= 1
    
    # Minutes
    if resultat [1] < 0:
        resultat [1] += 60
        resultat [0] -= 1
    
    # Arrondi
    resultat [2] = round (resultat [2], 3)
    resultat [1] = round (resultat [1])
    resultat [0] = round (resultat [0])
    
    # Heures
    if resultat [0] < 0:
        print ("Durée négative : " + baseAffichage + " - " + substitutAffichage)
        exit (0)
    
    # Sortie
    resultatAffichage = ":". join (map (str, resultat))
    return resultatAffichage


couper (
    nomDossier = "F:/Backup/Videos/Cinoche",
    debut = "0:2:14.000",
    fin = "0:0:3.000"
)
