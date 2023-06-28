# Compte rendu TP MCTS
> Auteurs : **Nathan Peyronnet** et **Émilie Vey**
> Date : 20/06/2023

## Paramétrage du jeu

Le jeu possède 3 modes : 
- **Humain vs Humain** : permet de jouer à deux joueurs humains
- **Humain vs IA** : permet de jouer contre une IA
- **IA vs IA** : permet de faire jouer deux IA l'une contre l'autre

Il est possible de séléctionner le mode de jeu dans le fichier [`main.py`](main.py#L18) en laissant décommentée la ligne correspondant au mode de jeu souhaité (lignes 18 à 20, `IA vs IA` par défaut).

Si le mode de jeu choisi comprend une IA, il est possible de choisir l'algorithme utilisé par celle(s)-ci. Sont implémentés les 3 algorithmes suivants :
- **MiniMax** : l'algorithme MiniMax
- **AlphaBeta** : l'algorithme AlphaBeta
- **UCT** : l'algorithme UCT

Pour choisir l'algorithme, il suffit de modifier le fichier [`ai.py`](ai.py#L12), et laisser décommentée la ligne correspondant à l'algorithme souhaité (lignes 12 à 14, `UCT` par défaut).