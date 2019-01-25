# a
def import_csv(file):
    """ Import d'un fichier csv contenant des candles sous le format date,open,high,low,close

    file -- chemin relatif vers ce fichier. Le fichier doit être contenu dans le dossier csv du projet
    --------
    Retourne 5 numpy arrays, d (dates), o (opens), h (highs), l (lows), c (closes).

    """
    pass


# b
def group_candles(dates, opens, highs, lows, closes, k):
    """ Regroupe k candles en une seule

    dates -- liste de date des candles, doit être de la même taille que k
    opens -- liste de prix d'open des candles, doit être de la même taille que k
    highs -- liste de prix d'high des candles, doit être de la même taille que k
    lows  -- liste de prix de low des candles, doit être de la même taille que k
    closes-- liste de prix de close des candles, doit être de la même taille que k
    k     -- Nombre de candles devant être regroupées. Entier
    --------
    Retourne 5 nombres à virgule, d (date), o (open), h (high), l (low), c (close).

    """
    pass


# c
def pattern_matching(filter, pattern, dates, opens, highs, lows, closes):
    """ Match les prix avec un pattern

    filter  -- nom du filtre employé
    pattern -- nom du pattern employé
    dates   -- liste de date des candles
    opens   -- liste de prix d'open des candles
    highs   -- liste de prix d'high des candles
    lows    -- liste de prix de low des candles
    closes  -- liste de prix de close des candles
    --------
    Retourne un tableau de correlation, de même taille que les tableaux de prix, contenant des valeurs entre [-100 et 100].

    """
    pass


# d
def analyse(tab_corr, dates, opens, highs, lows, closes, stoploss=3.5, period=10):
    """ Fonction analysant le résultat après une certaine durée après un pattern. Retourne la performance après la période.

    tab_corr-- tableau de corrélation du pattern sur les prix
    dates   -- liste de date des candles
    opens   -- liste de prix d'open des candles
    highs   -- liste de prix d'high des candles
    lows    -- liste de prix de low des candles
    closes  -- liste de prix de close des candles
    stoploss-- niveau du stoploss en %
    period  -- durée attendue pour mesurer les résultats en nombre de candles après le pattern
    --------
    Retourne un tableau de couples (date, résultat).

    """
    pass


# e
def analyse_max(tab_corr, dates, opens, highs, lows, closes, stoploss=3.5, period=10):
    """ Fonction analysant le résultat maximal durant une certaine durée après un pattern. Retourne la performance après la période.

    tab_corr-- tableau de corrélation du pattern sur les prix
    dates   -- liste de date des candles
    opens   -- liste de prix d'open des candles
    highs   -- liste de prix d'high des candles
    lows    -- liste de prix de low des candles
    closes  -- liste de prix de close des candles
    stoploss-- niveau du stoploss en %
    period  -- durée durant laquelle on mesure le résultat maximal. En nombre de candles après le pattern
    --------
    Retourne un tableau de couples (date, résultat). Les résultats sont en pourcent

    """
    pass


# f
def plot_results(dates, results, plot=False):
    """ Plot et écrit les résultats dans la sortie de la fonction

    dates -- tableau de dates
    résultats -- tableau de résultat, en pourcentage
    plot -- booléen. Si true alors affiche un graphe résultat
    --------
    Retourne un rapport (string)

    """
    pass


# g
def routine(dates, opens, highs, lows, closes, filter, pattern, stoploss=3.5, period=10, plot=False):
    """ englobe le processus des fonctions c à f.

    dates   -- liste de date des candles
    opens   -- liste de prix d'open des candles
    highs   -- liste de prix d'high des candles
    lows    -- liste de prix de low des candles
    closes  -- liste de prix de close des candles
    filter  -- nom du filtre employé
    pattern -- nom du pattern employé
    stoploss-- niveau du stoploss en %
    period  -- durée durant laquelle on mesure le résultat maximal. En nombre de candles après le pattern
   plot -- booléen. Si true alors affiche un graphe résultat
    --------
    Retourne un rapport (string)

    """
    pass


# h - Fonction qui appelle initialise les données avec a et b et qui appelle g pour plusieurs patterns.
def main():
    """ initialise les données, appelle la fonction de routine pour plusieurs patterns et parametres differents

    --------
    Retourne rien

    """
    pass
