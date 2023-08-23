from flask import Flask, request, jsonify
import os
import face_recognition

app = Flask(__name__)

@app.route('/trouver_personnes', methods=['POST'])
def trouver_personnes():
    # Vérifier si le fichier d'image est présent dans la requête
    if 'image' not in request.files:
        return jsonify({'message': 'Aucun fichier d\'image trouvé.'}), 400

    image_a_comparer = request.files['image']

    # Charger l'image à comparer
    image = face_recognition.load_image_file(image_a_comparer)
    encodage_image = face_recognition.face_encodings(image)

    if len(encodage_image) == 0:
        return jsonify({'message': 'Aucun visage détecté dans l\'image.'}), 400

    encodage_image = encodage_image[0]

    correspondances = []
    i = 0
    
    # Parcourir les images dans le dossier BD_photo
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
                # taux_fiabilite = face_recognition.face_distance([encodage_base], encodage_image)[0]
                # correspondances.append((nom_personne, taux_fiabilite))
                # correspondances.append(nom_personne)
                i += 1
                if i <= 3: 
                    correspondances.append(nom_personne)

    # Trier les correspondances par ordre décroissant de taux de fiabilité
    correspondances = sorted(correspondances, key=lambda x: x[1], reverse=True)

    if len(correspondances) > 0:
        return jsonify({'resultats': correspondances})
    else:
        return jsonify({'message': 'Aucune correspondance trouvée.'}), 404


@app.route('/ajouter_image', methods=['POST'])
def ajouter_image():
    # Vérifier si le fichier d'image est présent dans la requête
    if 'image' not in request.files:
        return jsonify({'message': 'Aucun fichier d\'image trouvé.'}), 400

    # Charger l'image à ajouter
    image_a_ajouter = request.files['image']

    # # Enregistrer l'image dans le dossier `BD_photo`
    # image_a_ajouter.save('BD_photo/' + image_a_ajouter.filename)
    
    # # Obtenir le chemin absolu du dossier `BD_photo`
    path_to_bd_photo = os.path.abspath("BD_photo")
    print(path_to_bd_photo)

    # # Enregistrer l'image dans le dossier `BD_photo`
    # image_a_ajouter.save(path_to_bd_photo + "/" + image_a_ajouter.filename)
    # Vérifier si le dossier `BD_photo` a les permissions d'écriture
    
    if not os.access(path_to_bd_photo, os.W_OK):
        # Donner les permissions d'écriture au dossier `BD_photo`
        os.chmod(path_to_bd_photo, os.W_OK)

    # Enregistrer l'image dans le dossier `BD_photo`
    image_a_ajouter.save(path_to_bd_photo + "/" + image_a_ajouter.filename)
    
    return jsonify({'message': 'L\'image a été ajoutée avec succès.'}), 200

if __name__ == '__main__':
    app.run()