import os
import face_recognition

def trouver_personne(image_a_comparer):
    # Charger l'image à comparer
    image = face_recognition.load_image_file(image_a_comparer)
    encodage_image = face_recognition.face_encodings(image)[0]

    # Parcourir les images dans le dossier identite_photo
    for fichier in os.listdir('BD_photo'):
        print(fichier)
        if fichier.endswith('.jpg') or fichier.endswith('.png'):
            chemin_image = os.path.join('BD_photo', fichier)
            image_base = face_recognition.load_image_file(chemin_image)
            encodage_base = face_recognition.face_encodings(image_base)[0]

            # Comparer les encodages faciaux
            correspondance = face_recognition.compare_faces([encodage_base], encodage_image)

            if correspondance[0]:
                nom_personne = os.path.splitext(fichier)[0]
                return f"La personne que vous cherchez correspond au profil de {nom_personne}."

    return "Aucune correspondance trouvée."

# Exemple d'utilisation
image_a_comparer = 'fotso.jpg'
resultat = trouver_personne(image_a_comparer)
print(resultat)
