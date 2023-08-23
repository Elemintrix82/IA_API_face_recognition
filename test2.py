import os
import face_recognition

def trouver_personnes(image_a_comparer):
    # Charger l'image à comparer
    image = face_recognition.load_image_file(image_a_comparer)
    encodage_image = face_recognition.face_encodings(image)

    if len(encodage_image) == 0:
        print("Aucun visage détecté dans l'image.")
        return []

    encodage_image = encodage_image[0]

    correspondances = []

    # Parcourir les images dans le dossier identite_photo
    for fichier in os.listdir('BD_photo'):
        print(fichier)
        if fichier.endswith('.jpg') or fichier.endswith('.png'):
            chemin_image = os.path.join('BD_photo', fichier)
            image_base = face_recognition.load_image_file(chemin_image)
            encodage_base = face_recognition.face_encodings(image_base)

            if len(encodage_base) == 0:
                continue

            encodage_base = encodage_base[0]

            # Comparer les encodages faciaux
            correspondance = face_recognition.compare_faces([encodage_base], encodage_image)

            if correspondance[0]:
                nom_personne = os.path.splitext(fichier)[0]
                taux_fiabilite = face_recognition.face_distance([encodage_base], encodage_image)[0]
                # correspondances.append((nom_personne, taux_fiabilite))
                correspondances.append(nom_personne)

    # Trier les correspondances par ordre décroissant de taux de fiabilité
    correspondances = sorted(correspondances, key=lambda x: x[1], reverse=True)

    return correspondances

# Exemple d'utilisation
image_a_comparer = 'team2.jpg'
resultats = trouver_personnes(image_a_comparer)

if len(resultats) > 0:
    for resultat in resultats:
        # nom_personne, taux_fiabilite = resultat
        nom_personne = resultat
        # print(f"La personne que vous cherchez correspond au profil de {nom_personne} avec un taux de fiabilité de {taux_fiabilite}.")
        print(f"La personne que vous cherchez correspond au profil de {nom_personne}.")
else:
    print("Aucune correspondance trouvée.")