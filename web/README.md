# Application de labellisation

## Utilisation

Variables d'environnement nécéssaires (à mettre dans un fichier .env):
* PATH_TWEETS           : le chemin vers la base de données de tweets originale (.pkl)
* PATH_LABELED_TWEETS   : le fichier (.csv) où seront ennregistré les tweets labelisés
* PATH_UNLABELED_TWEETS : le fichier (.csv) où seront enregistrés les tweets non labelisés

```bash
#/chemin/vers/ce/projet/
pip install -r requirements.txt
flet run -p 8000 -n -w app2.py # remplacer 8000 par le port souhaité.
```

L'application sera disponible à l'adresse `localhost:8000`
