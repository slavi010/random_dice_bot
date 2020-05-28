![Bot run gif](https://cdn.kapwing.com/final_5ecfd27cbecf9800154a81d1_48555.gif)

# Readme Language 
 - French / Français

# French / Français
## Presentation
C'est un bot du jeu Random Dice en python.
Il fonctionne uniquement en mode coop.
Il va automatiquement faire les fusions et le l'amelioration des dés.
Il détecte le type de dé et sont nombre de point.

Il est possible de specifier dans le code des actions tel que :
* "Tu fusionnes toujours les sacrifices si possible"
    ```python
    feature.add_fusion_dice(dice=DiceColorEnum.SACRIFICIAL)
    ```
* "Tu as une probabilité de 5% d'acheter l'amélioration du 5eme dé si il y a au moins 8 dés sur le plateau"
    ```python
    feature.add_buy_shop(proba_buy_shop=0.05, idx_dices=[5], min_dice_board=8)
    ```
* "Tu fusionnes les combos de manière intelligente"
    ```python
    feature.add_fusion_combo(max_dot_fusion=4)
    ```
* "Après une fin de game, tu regardes la pub et lance une nouvelle partie"
    ```python
    feature.add_auto_pub_and_start(ahk)
    ```

## Prérequis
* Python 3 (testé avec 3.7)
* AHK : https://www.autohotkey.com/download/
    * Si après lancement de bot , il ne détecte pas AHK, pensez à l'ajouter dans la varible PATH de votre ordinateur.
* Avec pip :
    * pip install pillow
    * pip install ahk
    * pip install opencv-python
    * pip install pynput

## Utilisation du bot
### Android sur PC
Le bot fonctionne uniquement sur PC.
Donc vous devez utiliser soit :
* Un émulateur de téléphone (android ex: [BluesStacks](https://www.bluestacks.com/))
* Une prise de controlle de votre téléphone sur votre ordinateur 
    (pour android, open source: [scrcpy](https://github.com/Genymobile/scrcpy))
    
### Lancement du programme
1. Innitier une partie sur Random Dice.
2. Lancer le programme du bot. Ne faite AUCUN autre clic !
3. Retourner sur la fenêtre du jeu (vous pouvez utiliser sur Windows alt+tab)
4. Vous devez ensuite faire UN clic en haut a gauche de plateau et UN en bas à droite.
![Image board where click](https://slavi.dev/nextcloud/index.php/s/zjZG52Y83S2awrY/preview)
5. Le bot va ensuite démarrer.

Une nouvelle feunêtre devrais être apparaître.
La grille en rouge devrais normalement être PARFAITEMENT aligné avec les cases du plateau.
Si ce n'est pas le cas, arrêter le bot/programme puis recommencer.

![Image board grid](https://slavi.dev/nextcloud/index.php/s/6GQXDiFcoZq6kCJ/preview)

### Arrêter le bot
Actullement, VOUS NE POUVEZ ARRETER LE BOT.
[#3](https://github.com/slavi010/random_dice_bot/issues/3)

### Skin de la carte
Le skin de carte actuellement compatible pour lancer le bot est celui par défaut.
[#2](https://github.com/slavi010/random_dice_bot/issues/2)

## Decks
L'unique deck qui est disponible où le bot fonctionne par défaut est :

![Deck combo](https://slavi.dev/nextcloud/index.php/s/WxQr4mi96qkGA43/preview)

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
Actuellement il y a uniquement les dés de 1 à 6 points qui sont pris en charge.
Les dés de 7 points (qui ont une étoile) sont détecté comme des dés à 1 point (regardez [#1](https://github.com/slavi010/random_dice_bot/issues/1#issue-626545664)).

## Contribution
Si vous voulez donner un coup de main :

* Pour proposer une nouvelle fonctionnalité ou un déclarer un un bug :
Créez une [nouvelle Issue](https://github.com/slavi010/random_dice_bot/issues/new/choose).
* Si vous voulez le faire vous même :
    Faite vos changement sur une nouvelle branche puis demandez un [nouveau 
    Pull Request](https://github.com/slavi010/random_dice_bot/compare) sur la branche *master*.
    
    Si vos changement sont **significatif** dans un fichier ou que vous en créez un nouveau,
    pensez à mettre votre nom et votre email en haut du fichier.
    
## Clause de non responsabilité
Personne à par vous êtes responssable responsable en cas de ban ou d'autres problèmes. 
Vous l'utilisez en toute connaissance de cause, à vos risques et périls.