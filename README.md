# Open Classrooms Projet 6
Maintenez et documentez un système de stockage des données sécurisé et performant

# Logique de Migration
- les données sont téléchargés par le script python dans le volume /temp (alternativement il est possible de sourcer le fichier manuellement et fournir le dossier).
- une fois intégrées les données du container MongoDB sont dans le volume correspondant.
- Dès lors que le CSV est disponible, le script vérifies/crée une base de donnes et une collection
- Ensuite pour chaque ligne on injecte un document dans la collection
- le nombre de ligne est découpé en iterrable pour former des batchs de quantité paramétrable
- une fois insérées on compare le nombre de lignes du fichier et le nombre de documents

# Modèle de données
Chaque document dispose des colonnes suivantes :
- Admission Type
- Age
- Billing Amount
- Blood Type
- Date of Admission
- Discharge Date
- Doctor
- Gender
- Hospital
- Insurance Provider
- Medical Condition
- Medication
- Name
- Room Number
- Test Results

# Relance docker compose et construction image
docker compose down && docker compose build && docker compose up -d && docker logs -f oc_projet6-app_server-1
