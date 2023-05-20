# MERCADONA studi B3
Auteur: Franck Rochette
Date: 10/05/2023

Application Python web asynchrone avec FASTAPI (v 0.95.1) / ORM Tortoise (v 0.19.3)/ 
Jinja2 Templates (v 3.1.2)/ Database: PostgreSQL hébergée sur AlwaysData

Images hébergées sur AWS S3 bucket

Description:
Catalogue publique de produit en retails avec remise ou sans /
Application d'un filtre de tri par categories/
Back Office admin/
    - injection dépendance token
    - création produit et création promotion
    - enregistrement des données en BDD et téléversement des images sur S3 Bucket
    - mise à jour des filtes catégories si création nouvelle catégorie

Point d'entrée application FastApi: app/start.py sur serveur uvicorn

 Lancement --> uvicorn app.start:app

Catalogue: accès publique sans restriction
Endpoints: "/" --> Page d'accueil
           "/articles/" --> Page catalogue

Back Office: accès privés
Endpoints: [...]

déploiement Heroku: https://merca-franck-rochette.herokuapp.com/
