#
# Programme de transformation d'image vers matrice de pixels 8x8
#

# Importation du module PIL pour la manipulation d'images
from PIL import Image
import PIL

# Ouverture du fichier et initialisation des valeurs pour détecter
# le chiffre sur l'image. Pour utiliser le programme avec votre
# propre image, il suffit de changer le nom du fichier en
# paramètre. Si les contour du chiffre sont mal détectés, vous
# pouvez essayer de reprendre une photo mieux cadrée ou de changer
# la valeur du seuil de blanc (par défaut 100)

image = Image.open("Chiffres_Test/0.png") # Chargement de l'image

width, height = image.size # Récupération de la largeur et de la hauteur de l'image

WHITE_THRESHOLD = 100 # Seuil à partir duquel la couleur est considérée blanche
extreme_left = width # initialisation du point extrème gauche 
extreme_right = 0 # initialisation du point extrème droit 
extreme_top = height # initialisation du point extrème haut 
extreme_bot = 0 # initialisation du point extrème bas

# Détection des contours du chiffre et transformation en noir et
# blanc très contrasté

for x in range(width):
    for y in range(height):
        pixel = image.getpixel((x, y)) # Récupération des composantes de couleur aux coordonnées [x,y]
        # On vérifie si le pixel est blanc
        if all(channel > WHITE_THRESHOLD for channel in pixel):
            image.putpixel((x, y), (255,255,255)) # S'il dépasse le seuil alors le pixel est transformé en pixel blanc
        else:
            # On met à jour les extrémités de l'image si les pixels sont foncés
            if extreme_left > x:
                extreme_left = x
            if extreme_right < x:
                extreme_right = x
            if extreme_top > y:
                extreme_top = y
            if extreme_bot < y:
                extreme_bot = y
            # On transforme le pixel en pixel noir
            image.putpixel((x, y), (0,0,0))

# Création d'une nouvelle image aux bonnes dimensions et
# préparation à la mise à l'échelle en matrice 8x8

new_height = extreme_bot - extreme_top # Calcul de la nouvelle hauteur à l'aide des extrémités
new_width = extreme_right - extreme_left # Calcul de la nouvelle largeur à l'aide des extrémités

if new_height > new_width: # Détermination de la plus grande
    # longueur pour la mise à l'échelle (pour éviter de couper une
    # partie de l'image) Et détermination de la différence entre
    # longueur et hauteur (pour ne pas parcourir des pixels
    # inutilement)
    max_dim = new_height
    difference = (max_dim - new_width) // 2
else:
    max_dim = new_width
    difference = (max_dim - new_height) // 2

newDimension = max_dim

# marge = 8 - max_dim % 8    
# Création d'une nouvelle image blanche aux bonnes dimensions
image2 = PIL.Image.new(mode="RGB", size=(newDimension, newDimension), color=(255,255,255))

# Parcours de l'image originale pour recopie sur la nouvelle image
i=0
for x in range(difference,max_dim-difference): 
    j=0
    for y in range(0,max_dim):
        image2.putpixel((x,y),image.getpixel((extreme_left+i,extreme_top+j)))
        j+=1
    i+=1


# Initialisation de la taille d'un pixel pour la création de la matrice
pixelSize = newDimension // 8

# Création d'une liste correspondant à la matrice 8x8
liste = []

# Découpage de l'image en 8x8 et parcours de ces sous parties pour
# calculer la moyenne de l'intensité des pixels

for j in range(8):
    for i in range(8):
        somme = 0
        for x in range(pixelSize):
            for y in range(pixelSize):
                somme += image2.getpixel((i*pixelSize+x, j*pixelSize+y))[0]
        liste.append(16-(somme//(pixelSize*pixelSize)+8)//16)

# Ajout de la classe correspondant au chiffre représenté (chiffre
# entre 0 et 9)
liste.append(0)

# Enregistrement de l'image avant pixelisation au format PNG
image2.save("./Chiffres_Resultat/new0.png", "png")

# Affichage de la liste contenant les informations sur l'image :
print(liste)
