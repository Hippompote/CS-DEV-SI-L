--------------------------------------------------------------
<p align="center">Space Invaders</p>
--------------------------------------------------------------

Ce programme est une version python du jeux d'arcade Space Invaders,
L'interface graphique est rélisée à l'aide de TKinter.

## Dépendances :

Ce programme utilise le package `pillow` non présent par défaut,
Python 3.10 est également nécessaire à cause de l'utilisation de type
pour la documentation.

## Touches :
- Aller à gauche : flèche de gauche / Q
- Aller à droite : flèche de droite / D
- Tirer un laser : espace
- Pause : échap

## Règles :
- Le **joueur** possède 3 points de vie à l'issue desquels il perd la partie.
- Les **barricades** possèdent 5 points de vie et se détruisent au contact de
    l'ennemi ou d'un laser.
- Les **aliens** accélèrent à chaque palier de 100 points et tirent des
    lasers aléatoirement.
- Les **lasers** provenant de source différentes (alien ou joueur)
    s'entredétruisent.
- Ce jeu est composé d'un seul niveau où le joueur doit détruire tous les
    aliens pour gagner. Ce niveau comporte 23 aliens et 2 barricades.

## Copyrights :
L'image servant de fond au niveau est une image du domaine public issue de
https://wallpaperflare.com.<br>
Nous avons créé tous les autres éléments graphiques de ce projet.

## Auteurs :
- Charles ARBAUD (Aioniostheos)
- Louis ROBERT (fierperle)

## Dépôt :
Une copie de ce fichier, ainsi que du code source est disponible à
l'adresse :<br>
https://github.com/cpe-lyon/tp-5---groupe-a-groupe-a-arbaud-robert

--------------------------------------------------------------

## Structure du projet :
 - L'intégralité des ressources graphiques utilisées par le programme se
    trouvent dans le dossier `assets`.
 - Le sous-paquet `entities` contient les 6 fichiers python définissant les
    classes d'entités du jeu.
 - Le sous-paquet `util` contient les 2 fichiers python définissant les
    implémentations de pile et de file utilisées dans la classe `World`.
 - Le sous-paquet `world` contient les 2 fichiers python définissant les
    classes `World` et `Client`. Ces classes permettent le découpage du jeu
    en deux parties : une partie fonctionnelle et un partie graphique.
 - Le fichier `game.py` définit la classe `Game`. Il s'agit de la classe
    principale du programme. Elle permet de gérer les événements clavier et
    de lancer le jeu. 
 - Le fichier `main.py` est le point d'entrée du programme. Il lance une
    fenêtre de menu de jeu permettant de lancer le jeu ou de quitter.
 - Le fichier `test.py` est un fichier de test utilisé pour vérifier des
    fonctionnalités du programme sans impacter le code principal.

Le code de ce projet a été intégralement documenté au format `pydoc`. Les
IDE compatibles permettent de visualiser cette documentation.

--------------------------------------------------------------
## Spécificités techniques :
Il est possible de lancer le jeu en pleine écran en modifiant la variable
globale `FULLSCREEN` dans le fichier `main.py`.

Le programme exécute indépendamment un rafraîchissement de l'écran et une
actualisation du jeu. Il est possible de définir la fréquence de
rafraîchissement de l'écran en modifiant la variable globale
`MAX_FRAMERATE` dans le fichier `main.py`.

Une implémentation de pile a été réalisée dans le fichier `util/stack.py`.
Cette pile est utilisée pour stocker les aliens présents dans le monde afin
de vérifier la fin de la partie (tous les aliens sont morts) et de leur
permettre de tirer. Pour toute information complémentaire, se référer à la
documentation.

Une implémentation de file a été réalisée dans le fichier `util/queue.py`.
Cette file est utilisée pour stocker les entités en attente de destruction.
En effet, il est possible qu'une entité soit retirée du monde physiquement
alors que son affichage n'est pas encore terminé. Pour toute information
complémentaire, se référer à la documentation.