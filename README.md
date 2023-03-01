# SAE3.05_grp_NathanBourdere_2A

## Liens
Vous trouverez ci-dessous tous les liens utiles en rapport avec le projet.

### [Manuel utilisateur](https://github.com/NathanBourdere/SAE3.05_grp_NathanBourdere_2A/wiki)
Le manuel utilisateur donne la description et le guidage nécessaires pour prendre en main le site Vacat'O quel que soit le type de personne l'utilisant (administrateur ou vacataire).

### [Dossier partagé Google Drive](https://drive.google.com/drive/folders/1n3ntdANdTEU4EXUBkdOFUPeqhCDqvSGY?usp=sharing)
Le dossier partagé Google Drive regroupe toutes les ressources du projet. Il contient les rapports, les exports et les sauvegardes du diagramme de Gantt, les diagrammes conçus lors de l'analyse comme le diagramme des cas d'utilisation ou le modèle conceptuel des données, le cahier des charges, le sujet de ce projet ou encore les rapports écris demandé par le corps professeur. Pour avoir accès au dossier partagé il n'y a pas forcément besoin de se connecter à Google. N'importe qui peut le consulter mais ne peut en rien modifier quoi que ce soit.

### [Maquettes sur Figma](https://www.figma.com/file/6Ac3W80ETHOQVFtlyHYx3N/Vacataire?node-id=0%3A1)
Figma est un site que nous avons utilisé pour faire les maquettes du site Vacat'O et nous donner une idée de l'orientation front-end lors de l'implémentation des templates HTML.

### [Planning Trello](https://trello.com/invite/saes305/ATTI4c2f89044ce7c7d1f58ca0dca85d3adaB77ECDE7)
Trello est un site qui nous a permis de nous organiser pour la répartition et l'attribution des tâches. Il nous permettait sur les parties analyse et rendus de voir les tâches effectuées, les tâches en cours et les tâches à venir tout en sachant qui était responsable de l'exécution de quelle tâche. Pour la partie plus programmation du projet nous nous sommes basés sur les "Issues" Github pour nous organiser de manière similaire.

## Installations, configuration et lancement côté serveur

1. Pour faire tourner le site web il est conseillé d'utiliser un environnement virtuel. Pour le créer il suffi de se positionner dans le dossier contenant le projet et exécuter la commande qui suit. Si vous ne souhaitez pas utiliser d'environnement virtuel, rendez-vous à l'étape 3.
```sh
virtualenv -p python3 venv
```

2. Pour utiliser l'environnement virtuel nouvellement créé, toujours dans le même terminal, faites la commande ci-dessous :
```sh
source venv/bin/activate
```

3. Le site Vacat'O a besoin de plusieurs librairies pour fonctionner. La commande qui suit permet de toutes les installer grâce à un fichier texte qui concerve leurs noms.
```sh
pip install -r requirement.txt
```

4. Pour lancer l'application veillez à vous trouver dans le répertoire "app" se trouvant à la racine du projet auquel cas une erreur sera retournée. Une fois dans le bon répertoire, utilisez la commande suivante :
```sh
flask run
```

5. Au cours du développement nous avons ajouté des commandes en rapport avec la base de données. Elles sont utiles dans la mesure où l'on veut utiliser les jeux de données contenus dans les fichiers CSV, remettre la base de données à 0 (c'est à dire avoir une base de données uniquement avec toutes les tables étant vides) ou juste supprimer la base de données. Pour voir ces commandes, faites la commande qui suit.
```sh
flask
```
