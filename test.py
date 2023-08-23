import os
import cv2
import numpy as np

# # Fonction pour charger les images et les étiquettes à partir de la base de données
# def charger_base_donnees():
#     images = []
#     etiquettes = []
    
#     # Chemin vers le dossier contenant les images
#     dossier_images = "BD_photo"
    
#     # Parcourir tous les fichiers dans le dossier des images
#     for fichier in os.listdir(dossier_images):
#         chemin_image = os.path.join(dossier_images, fichier)
        
#         # Charger l'image en niveaux de gris
#         image = cv2.imread(chemin_image, cv2.IMREAD_GRAYSCALE)
        
#         # Ajouter l'image à la liste des images
#         images.append(image)
        
#         # Extraire l'étiquette à partir du nom du fichier
#         etiquette = int(os.path.splitext(fichier)[0])
        
#         # Ajouter l'étiquette à la liste des étiquettes
#         etiquettes.append(etiquette)
    
#     return images, etiquettes

def charger_base_donnees():
    chemin_dossier = "BD_photo"
    images = []
    etiquettes = []
    etiquettes_dict = {}

    for fichier in os.listdir(chemin_dossier):
        if fichier.endswith(".jpg"):
            chemin_image = os.path.join(chemin_dossier, fichier)
            image = charger_image(chemin_image)
            images.append(image)

            etiquette = etiquettes_dict.get(fichier)
            if etiquette is None:
                etiquette = len(etiquettes_dict) + 1
                etiquettes_dict[fichier] = etiquette
            etiquettes.append(etiquette)

    return images, etiquettes


def charger_image(chemin_image):
    # Charger l'image à partir du chemin donné
    image = cv2.imread(chemin_image)
    
    return image

# Fonction pour entraîner le modèle de reconnaissance faciale
def entrainer_modele(images, etiquettes):
    # Créer un objet de reconnaissance faciale
    modele = cv2.face.EigenFaceRecognizer_create()
    
    # Entraîner le modèle avec les images et les étiquettes
    modele.train(images, np.array(etiquettes))
    
    return modele

# Fonction pour détecter et reconnaître le visage dans une image donnée
def reconnaitre_visage(modele, image):
    # Convertir l'image en niveaux de gris
    image_gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Détecter les visages dans l'image
    detecteur_visage = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    visages = detecteur_visage.detectMultiScale(image_gris, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Parcourir tous les visages détectés
    for (x, y, w, h) in visages:
        # Extraire la région du visage de l'image en niveaux de gris
        visage_roi = image_gris[y:y+h, x:x+w]
        
        # Redimensionner la région du visage à une taille fixe
        visage_roi_redim = cv2.resize(visage_roi, (100, 100))
        
        # Effectuer la reconnaissance faciale sur la région du visage
        etiquette, confiance = modele.predict(visage_roi_redim)
        
        # Dessiner un rectangle autour du visage détecté
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Afficher le nom de la personne reconnue et la confiance
        if confiance < 500:
            nom_personne = "Personne " + str(etiquette)
        else:
            nom_personne = "Inconnu"
        
        cv2.putText(image, nom_personne, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    return image

# Charger les images et les étiquettes à partir de la base de données
images, etiquettes = charger_base_donnees()

# Entraîner le modèle de reconnaissance faciale
modele = entrainer_modele(images, etiquettes)

# Charger l'image à partir de l'application web
image_utilisateur = cv2.imread("img1.jpg")

# Reconnaître le visage dans l'image utilisateur
resultat = reconnaitre_visage(modele, image_utilisateur)

# Afficher l'image avec le visage reconnu
cv2.imshow("Résultat", resultat)
cv2.waitKey(0)
cv2.destroyAllWindows()