import requests

# URL de l'API
# URL pour trouver une photo
# url = 'http://localhost:5000/trouver_personnes'
# url = 'https://valdez-akap-okapi-face-recognition.hf.space/find_person'

# URL pour ajouter une photo
# url = 'http://localhost:5000/ajouter_image'
url = 'https://valdez-akap-okapi-face-recognition.hf.space/add_picture'

# Chemin vers le fichier d'image
# image_path = '/chemin/vers/votre/image.jpg'
image_path = r'fotso.jpg'

# Envoi de la requête POST avec le fichier d'image
files = {'image': open(image_path, 'rb')}
response = requests.post(url, files=files)
print(response)

# Vérification de la réponse
if response.status_code == 200:
    # Traitement de la réponse JSON
    data = response.json()
    print(data)
else:
    print(f'Une erreur est survenue lors de la requête. {response.status_code}')
    
    