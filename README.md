[comment]: <> (#################################################################################)
[comment]: <> (# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR    #)
[comment]: <> (# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,      #)
[comment]: <> (# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE   #)
[comment]: <> (# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER        #)
[comment]: <> (# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, #)
[comment]: <> (# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE #)
[comment]: <> (# SOFTWARE.                                                                     #)
[comment]: <> (#################################################################################)
[comment]: <> (# Contributors :)
[comment]: <> (# Copyright \(c\) 2020 slavi010 pro@slavi.dev)

# Random Dice Bot

# WARNING
**Due to updates, the bot is not working properly !! (more information :[#7](https://github.com/slavi010/random_dice_bot/issues/7))**

# Readme Language 
 - French / Français

# French / Français
## Presentation
C'est un bot du jeu Random Dice en python.
Il fonctionne uniquement en mode coop.
Il va automatiquement faire les fusions et le l'amelioration des dés.
Il détecte le type de dé et sont nombre de point.

Une nouvelle interface graphique est disponible !

## Prérequis
* Python 3 (testé avec 3.7 et 3.8)
* Dépendances python
    * /!\ Cette application utilise Tkinter
    * Instalation des dépendances avec le fichier requirements.txt
        * ```pip install -r requirements.txt```

*(Ou ```pip3``` en fonction de votre installation de python)

## Utilisation du bot
### Android sur PC
Le bot fonctionne uniquement sur PC (testé sous Ubuntu 20.10).
Donc vous devez utiliser soit :
* Un émulateur de téléphone (android ex: [BluesStacks](https://www.bluestacks.com/))
* Une prise de contrôle de votre téléphone sur votre ordinateur 
    (pour android, open source : [scrcpy](https://github.com/Genymobile/scrcpy))
    
### Lancement du programme
1. Lancez le programme du bot. Une interface graphique devrait afficher, si ce n'est pas le cas, avez-vous des problèmes de dépendances ? (Lancez le fichier src/main.py dans la racine du projet)

![Image interface graphique](https://slavi.dev/nc/index.php/s/JSmJ3jRbLibCdDt/preview)

2. Le bot est déjà pré configuré pour un deck spécifique. Vous pouvez vous amuser a changer le comportement du bot via l'interface graphique, mais aucune modification ne sera sauvegardées. Vous pouvez aussi directement modifier le fichier src/main.py.
3. Initier une partie coop sur Random Dice.
4. Démarrer le bot
5. Ne faite AUCUN autre clic !
6. Retourner sur la fenêtre du jeu (vous pouvez utiliser sur Windows, alt+tab)
7. Vous devez ensuite faire UN clic en haut a gauche de plateau et UN en bas à droite.

![Image board where click](https://slavi.dev/nc/index.php/s/N8NGeNmrFsMSQBG/preview)

8. Le bot va ensuite démarrer.

Une nouvelle fenêtre devrait apparaître.
La grille en rouge devrait normalement être PARFAITEMENT aligné avec les cases du plateau.
Si ce n'est pas le cas, arrêter le bot/programme puis recommencer.

![Image board grid](https://slavi.dev/nextcloud/index.php/s/6GQXDiFcoZq6kCJ/preview)

### Arrêter le bot
Pour arrêter le programme, appuyer longuement sur la touche Echap.
[#3](https://github.com/slavi010/random_dice_bot/issues/3)

### Skin de la carte
Le skin de carte actuellement compatible pour lancer le bot est celui par défaut (version claire).
[#2](https://github.com/slavi010/random_dice_bot/issues/2)

## Decks
L'unique deck qui est disponible où le bot fonctionne par défaut est :

![Deck combo](https://slavi.dev/nc/index.php/s/5AmWSQqx9LWAssd/preview)

Les dés doivent être dans le même ordre !

Si vous voulez customizer votre bot pour votre deck, 
modifier le dossier [main](https://github.com/slavi010/random_dice_bot/blob/master/src/main.py)
la partie feature. 

## Dés pris en charge
### Type de dé
* FIRE
* ELECTRIC
* WIND
* POISON
* ICE
* IRON
* BROKEN
* GAMBLE
* LOCK
* MINE
* THORN
* CRACK
* ENERGY
* SACRIFICIAL
* BOW
* GROWTH
* COMBO
* METASTASIS
* JOKER
* MIMIC

### Les points des dés
Actuellement, il y a uniquement les dés de 1 à 6 points qui sont pris en charge.
Les dés de 7 points (qui ont une étoile) sont détectés comme des dés à 1 point.
[#1](https://github.com/slavi010/random_dice_bot/issues/1#issue-626545664))

## Contribution
Si vous voulez donner un coup de main :

* Pour proposer une nouvelle fonctionnalité ou un déclarer un bug :
  Créez une [nouvelle Issue](https://github.com/slavi010/random_dice_bot/issues/new/choose).
* Si vous voulez le faire vous-même :
  Faite vos changements en faisant un fork du projet sur votre compte puis demandez un [nouveau 
  Pull Request](https://github.com/slavi010/random_dice_bot/compare) sur la branche *master* de ce projet.

  Si vos changements sont *significatif* dans un fichier ou que vous en créez un nouveau,
  pensez à mettre votre nom/speudo et votre e-mail en haut du fichier.

## Clause de non responsabilité
Ce projet a pour but une utilisation ludique des capacités de python.
En **AUCUN** cas, il n'a pour but de farm des coffres ou toutes autres choses en désaccord
avec les règles du jeu Random Dice.

Personne a par vous êtes responsable responsable en cas de ban ou d'autres problèmes. 
Vous l'utilisez en toute connaissance de cause, à vos risques et périls.
