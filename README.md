# EvaluatorCNDLSTK

### Task list
__TODO__ = To Do
__INPR__ = In progress
_DONE_ = Done

* _DONE_ - 1 - Fonction prenant en entrée la data venant d'influx et en sortie formattée pour talib
* _DONE_ - 2 - Passer les données dans une fonction de détection de pattern de TA-lib.
* _DONE_ - 3 - Fonction qui prend en entrée le tableau de correspondance, les données de candle initiales et un coefficient gain/risque k.
On veut en sortie une liste de valeur de même cardinal que la liste d'entrée qui indique quand le pattern a 'fonctionné'.
Pour cela, la liste contiendra les éléments suivants :
   0 : pas de pattern ici
   1 : réussite d'un pattern
  -1 : echec d'un pattern
* _DONE_ - 4 - Fonction de calcul de l'espérance des gains, du pourcentage de réussite du pattern et du délais moyen de réussite.
* _DONE_ - 5 - Retester les résultats des/du pattern. (ils semblent un peu fort)
    + _DONE_ - 5.1 -  -> Comment est determiné le buy price ? Il ne doit pas être sur le pattern mais juste après celui-ci -> OK
    + _DONE_ - 5.2 -  -> Revoir cette idée de slippage -> Pas mal, il faudra néanmoins être capable par la suite de fixer les sl et tp à des niveaux de supports/résistances ou des pivots.
    + _DONE_ - 5.3 - -> Representer graphiquement ce qu'il se passe, ça aide au debug.
    + _DONE_ - 5.4 -  -> Créer une méthode qui retourne tableau de corrélation aléatoire.
    + _DONE_ - 5.5 -  -> Problème identifié : Effectivement les résultats étaient biaisés par l'ordre d'évaluation des candles suivantes, Il faut maintenant trouver un moyen égalitaire et equilibré pour faire cette détermination -> OK, random 1/2


* _DONE_ - 6 - Ajouter les calculs de max drawndown et de courbe de capital
* __TODO__ - 7 - Créer une méthode de filtrage en fonction du sens de la courbe (.filter apres l'appel à ta-lib)
* __TODO__ - 8 - Automatiser le test de plusieurs patterns. -> Avoir des classements de pattern et résultat de groupe.
* __TODO__ - 9 - Implémenter le critère de Kelly pour le MM.
* __TODO__ - 10 - Télécharger des données du forex pour tester sur de 'vrais' marchés les patterns.


