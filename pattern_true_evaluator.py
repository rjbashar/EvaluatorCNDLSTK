import csv
import numpy as np
import talib as ta
import filter
import matplotlib.pyplot as plt


# a
def import_csv(file):
    """ Import d'un fichier csv contenant des candles sous le format date,open,high,low,close

    file -- chemin relatif vers ce fichier. Le fichier doit être contenu dans le dossier csv du projet
    --------
    Retourne 5 arrays, d (dates), o (opens), h (highs), l (lows), c (closes).

    """
    dates = []
    opens = []
    highs = []
    lows = []
    closes = []
    with open('csv/' + file + '.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            dates.append(row[0])
            opens.append(row[1])
            highs.append(row[2])
            lows.append(row[3])
            closes.append(row[4])

    return dates, opens, highs, lows, closes


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
    has_c_been_set = False
    if len(dates) != k or len(opens) != k or len(highs) != k or len(lows) != k or len(closes) != k:
        if len(dates) == len(opens) == len(highs) == len(lows) == len(closes):
            c = closes[len(closes) - 1]
            has_c_been_set = True
        else:
            return "arrays lengths not compatible."

    d = dates[0]
    o = opens[0]
    h = max(highs)
    l = min(lows)
    if not has_c_been_set:
        c = closes[k - 1]
    return d, o, h, l, c


# c
def pattern_matching_and_filtering(filter_name, filter_direction, pattern_name, pattern_direction, opens, highs, lows, closes):
    """ Match les prix avec un pattern

    filter    -- nom du filtre employé
    pattern   -- nom du pattern employé
    direction -- direction du pattern recherché: 'bullish' or 'bearish' (can be range ?)
    opens   -- liste de prix d'open des candles
    highs   -- liste de prix d'high des candles
    lows    -- liste de prix de low des candles
    closes  -- liste de prix de close des candles
    --------
    Retourne un tableau de correlation, de même taille que les tableaux de prix, contenant des valeurs entre [-100 et 100].

    """
    # First we match the prices with ta-lib
    tab_cor = []
    if pattern_name == 'hammer':
        tab_cor = ta.CDLHAMMER(opens, highs, lows, closes)
    elif pattern_name == "belthold":
        tab_cor = ta.CDLBELTHOLD(opens, highs, lows, closes)
    else:  # Default pattern is hammer
        tab_cor = ta.CDLHAMMER(opens, highs, lows, closes)

    if pattern_direction == 'bullish':
        # Then we flat out everything under 0
        for i in range(0, len(tab_cor)):
            if tab_cor[i] < 0:
                tab_cor[i] = 0
    else:
        # Then we flat out everything over 0
        for i in range(0, len(tab_cor)):
            if tab_cor[i] > 0:
                tab_cor[i] = 0

    # Then we filter it
    if filter_name == 'no_filter':
        pass
    elif filter_name == 'ema_filter':
        tab_cor = filter.ema_filter(closes, tab_cor, direction=filter_direction, ma=9)

    return tab_cor


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
    # /!\ Pas de notion de stoploss pour le moment
    k = len(tab_corr)
    if len(dates) != k or len(opens) != k or len(highs) != k or len(lows) != k or len(closes) != k:
        return "array length not equals to k."

    results = []
    for i in range(0, k):
        if tab_corr[i] != 0:
            percentage = (100 * (closes[min(i+period, len(closes)-1)] / closes[i])) - 100
            results.append((dates[i], percentage))

    return results


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
    # /!\ Pas de notion de stoploss pour le moment
    k = len(tab_corr)
    if len(dates) != k or len(opens) != k or len(highs) != k or len(lows) != k or len(closes) != k:
        return "array length not equals to k."

    results = []
    for i in range(0, k):
        if tab_corr[i] != 0:
            highest_price = max(highs[i:i+period])
            percentage = (100 * (highest_price / closes[i])) - 100
            results.append((dates[i], percentage))

    return results


# f
def plot_results(results, pattern_name, filter_name, stoploss=3.5, plot=False):
    """ Plot et écrit les résultats dans la sortie de la fonction

    dates -- tableau de dates
    résults -- tableau de résultat, en pourcentage
    pattern_name -- Nom du pattern utilisé
    filter_name -- Nom du filtre utilisé
    stoploss -- niveau du stoploss en %
    plot -- booléen. Si true alors affiche un graphe résultat
    --------
    Retourne un rapport (string)

    """
    if len(results) == 0:
        print('Erreur: Aucun résultat obtenu depuis le pattern matching')
        return

    bloc1 = 0
    bloc2 = 0
    bloc3 = 0
    bloc4 = 0
    bloc5 = 0
    bloc6 = 0
    for i in range(0, len(results)):
        if results[i][1] < -3:
            bloc1 += 1
        elif -3 <= results[i][1] < -1:
            bloc2 += 1
        elif -1 <= results[i][1] < 0:
            bloc3 += 1
        elif 0 <= results[i][1] < 1:
            bloc4 += 1
        elif 1 <= results[i][1] < 3:
            bloc5 += 1
        elif 3 <= results[i][1]:
            bloc6 += 1

    report = ""
    report += "\nPattern {}, filter {}:".format(pattern_name, filter_name)
    report += "\nAfter n periods, we get the following distribution:".format()
    report += "\n   ]-% ; -3%]: {:.5} %".format(100*bloc1/len(results))
    report += "\n  [-3% ; -1%]: {:.5} %".format(100*bloc2/len(results))
    report += "\n  [-1% ;  0%]: {:.5} %".format(100*bloc3/len(results))
    report += "\n  [ 0% ;  1%]: {:.5} %".format(100*bloc4/len(results))
    report += "\n  [ 1% ;  3%]: {:.5} %".format(100*bloc5/len(results))
    report += "\n  [ 3% ;  +%[: {:.5} %".format(100*bloc6/len(results))
    report += "\nCalculated from {} trades".format(len(results))

    if plot:
        # get all the percents results only
        percents = []
        for i in results:
            percents.append(i[1])
        plt.xlabel("% return")
        plt.ylabel("number of trade")
        bins = [-3.95, -3.9, -3.85, -3.8, -3.75, -3.7, -3.65, -3.6, -3.55, -3.5, -3.45, -3.4, -3.35, -3.3, -3.25, -3.2, -3.15, -3.1, -3.05, -3.0, -2.95, -2.9, -2.85, -2.8, -2.75, -2.7, -2.65, -2.6, -2.55, -2.5, -2.45, -2.4, -2.35, -2.3, -2.25, -2.2, -2.15, -2.1, -2.05, -2.0, -1.95, -1.9, -1.85, -1.8, -1.75, -1.7, -1.65, -1.6, -1.55, -1.5, -1.45, -1.4, -1.35, -1.3, -1.25, -1.2, -1.15, -1.1, -1.05, -1.0, -0.95, -0.9, -0.85, -0.8, -0.75, -0.7, -0.65, -0.6, -0.55, -0.5, -0.45, -0.4, -0.35, -0.3, -0.25, -0.2, -0.15, -0.1, -0.05, 0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5, 1.55, 1.6, 1.65, 1.7, 1.75, 1.8, 1.85, 1.9, 1.95, 2.0, 2.05, 2.1, 2.15, 2.2, 2.25, 2.3, 2.35, 2.4, 2.45, 2.5, 2.55, 2.6, 2.65, 2.7, 2.75, 2.8, 2.85, 2.9, 2.95, 3.0, 3.05, 3.1, 3.15, 3.2, 3.25, 3.3, 3.35, 3.4, 3.45, 3.5]
        n, bins, patches = plt.hist(percents, bins, density=False, facecolor='g', alpha=0.75)
        plt.grid(True)
        plt.axis([-2, 2, 0, max(n)])
        plt.show()

    return report


# g
def routine(dates, opens, highs, lows, closes, filter_name, filter_direction, pattern_name, pattern_direction, max=False, stoploss=3.5, period=10, plot=False):
    """ englobe le processus des fonctions c à f.

    dates        -- liste de date des candles
    opens        -- liste de prix d'open des candles
    highs        -- liste de prix d'high des candles
    lows         -- liste de prix de low des candles
    closes       -- liste de prix de close des candles
    filter_name  -- nom du filtre employé
    pattern_name -- nom du pattern employé
    max          -- booléen. Si vrai alors on utilise analyse_max, sinon analyse.
    stoploss     -- niveau du stoploss en %
    period       -- durée durant laquelle on mesure le résultat maximal. En nombre de candles après le pattern
    plot         -- booléen. Si true alors affiche un graphe résultat
    --------
    Retourne un rapport (string)

    """
    tab_corr = pattern_matching_and_filtering(filter_name, filter_direction, pattern_name, pattern_direction, opens, highs, lows, closes)
    if max:
        results = analyse_max(tab_corr, dates, opens, highs, lows, closes, stoploss=stoploss, period=period)
    else:
        results = analyse(tab_corr, dates, opens, highs, lows, closes, stoploss=stoploss, period=period)
    return plot_results(results, pattern_name, filter_name, stoploss=stoploss, plot=plot)


# h - Fonction qui appelle initialise les données avec a et b et qui appelle g pour plusieurs patterns.
def main():
    """ initialise les données, appelle la fonction de routine pour plusieurs patterns et parametres differents

    --------
    Retourne rien

    """
    starting_year = 2000
    ending_year = 2019
    dates = []
    opens = []
    highs = []
    lows = []
    closes = []
    for i in range(starting_year, ending_year):
        d, o, h, l, c = import_csv("DAT_ASCII_EURUSD_M1_{}".format(i))
        dates += d
        opens += o
        highs += h
        lows += l
        closes += c

    new_dates = []
    new_opens = []
    new_highs = []
    new_lows = []
    new_closes = []
    k = 15
    count = 0
    for i in range(0, len(dates), k):
        d, o, h, l, c = group_candles(dates[count*k:(count+1)*k],
                                      opens[count*k:(count+1)*k],
                                      highs[count*k:(count+1)*k],
                                      lows[count*k:(count+1)*k],
                                      closes[count*k:(count+1)*k],
                                      k)
        count += 1
        new_dates.append(d)
        new_opens.append(o)
        new_highs.append(h)
        new_lows.append(l)
        new_closes.append(c)

    # rewriting new dates into dates, but this time in a numpy array
    dates = np.array(new_dates)
    opens = np.array(new_opens, dtype='double')
    highs = np.array(new_highs, dtype='double')
    lows = np.array(new_lows, dtype='double')
    closes = np.array(new_closes, dtype='double')

    # Appels de la routine pour chaque pattern
    # Chaque pattern embarque ces paramètres sous la forme
    # [pattern_name, pattern_direction, filter_name, filter_direction,
    pattern_list = [{'pn': 'hammer', 'pd': 'bullish', 'fn': 'ema_filter', 'fd':'bearish'},
                    {'pn': 'belthold', 'pd': 'bearish', 'fn': 'ema_filter', 'fd': 'bullish'},
                    {'pn': 'belthold', 'pd': 'bearish', 'fn': 'no_filter', 'fd': 'bullish'}]

    for pattern in pattern_list:
        report = routine(dates, opens, highs, lows, closes,
                         filter_name=pattern['fn'],
                         filter_direction=pattern['fd'],
                         pattern_name=pattern['pn'],
                         pattern_direction=pattern['pd'],
                         max=False,
                         stoploss=1,
                         period=10,
                         plot=True)
        print(report)


if __name__ == "__main__":
    main()

# Pour la sauvegarde
# report = routine(dates, opens, highs, lows, closes,
#                  filter_name='ema_filter',
#                  filter_direction='bearish',
#                  pattern_name='hammer',
#                  pattern_direction='bearish',
#                  max=False,
#                  stoploss=1,
#                  period=10,
#                  plot=True)


# Pour générer les bins
# b = []
# count = -400
# for i in range(0, 150):
#     count += 5
#     b.append(count/100)
