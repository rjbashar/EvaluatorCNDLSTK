import talib as ta


def zigzag_filter(tab_cor, direction='up', since='15'):
    return tab_cor


def ema_filter(prices, tab_cor, direction='bullish', ma=15):
    """ Filter patterns results according to a trend direction

    prices -- liste de prix
    tab_cor -- tableau de correlation prix / pattern
    direction -- direction du pattern recherché: 'bullish' or 'bearish' or 'range'
    ma -- longueur de la moving average pour le filtrage
    --------
    Retourne un tableau de correlation, de même taille que les tableaux de prix, contenant des valeurs entre [-100 et 100].

    """
    ema = ta.EMA(prices, timeperiod=ma)
    long_ema = ta.EMA(prices, timeperiod=2 * ma - 1)
    pdirection = 'range'
    for i in range(0, len(tab_cor)):
        if tab_cor[i] != 0:
            if ema[i] is not None:
                if prices[i] > ema[i] > long_ema[i]:
                    pdirection = 'bullish'
                elif prices[i] < ema[i] < long_ema[i]:
                    pdirection = 'bearish'
                else:
                    pdirection = 'range'
            if pdirection != direction:
                tab_cor[i] = 0
    return tab_cor


def amplitude_filter(c, l, tab_cor, min_amplitude=0.01):
    for i in range(0, len(tab_cor)):
        if tab_cor[i] != 0:
            if (c[i] - l[i]) / c[i] < min_amplitude:
                tab_cor[i] = 0
    return tab_cor
