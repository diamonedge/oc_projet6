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

# Authentifiaction et utilisateurs
- 2 utilisateurs sont paramétrés par défaut. Un administrateur ayant tous les droits ainsi qu'un utilisateur lecteur pour la consultation
- Par défaut le fichier `compose.yml` contient les identifiants administrateurs. Il est possible de les changer avant ou après la création.
- le mot de passe de l'utilisateur `reader_user` est généré aléatoirement à la création du container. Les identifiants peuvent être modifiés avant ou après
- Pour se connecter il est possible d'utiliser un client mongo comme mongosh (https://www.mongodb.com/try/download/shell)  ou encore d'ajouter un container mongo-express comme vu ici https://hub.docker.com/_/mongo, cette dernière possibilité met à disposition une IHM web selon la configuration souhaitée

# Relance docker compose et construction image
docker compose down && docker compose build && docker compose up -d && docker logs -f oc_projet6-app_server-1
