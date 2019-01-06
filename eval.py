from mpl_finance import candlestick2_ohlc
import matplotlib.pyplot as plt
import random


def simple_continuation(o, h, l, c, tab_cor, k=1, n=1):
    ret = []
    for i in range(0, len(tab_cor)):
        if tab_cor[i] == 100:
            if c[i + n] > c[i]:
                ret.append(1)
            else:
                ret.append(-1)
        elif tab_cor[i] == -100:
            if c[i + n] < c[i]:
                ret.append(1)
            else:
                ret.append(-1)
        else:
            ret.append(0)
    return ret


def continuation_higher_than_risk_after_n(o, h, l, c, tab_cor, k=1, n=5):
    ret = []
    coef_adjust = 1.04
    for i in range(0, len(tab_cor) - n - 1):
        if tab_cor[i] == 100:
            risk = (c[i] - l[i]) * coef_adjust
            if c[i + n] > c[i] + k * risk:
                ret.append(1)
            else:
                ret.append(-1)
        elif tab_cor[i] == -100:
            risk = (h[i] - c[i]) * coef_adjust
            if c[i + n] < c[i] - k * risk:
                ret.append(1)
            else:
                ret.append(-1)
        else:
            ret.append(0)
    return ret


def continuation_higher_than_risk_n_timeframe(o, h, l, c, tab_cor, k=1, n=5):
    ret = []
    coef_adjust = 1.04
    for i in range(0, len(tab_cor) - n - 1):
        if tab_cor[i] == 100:  # If bullish signal

            risk = (c[i] - l[i]) * coef_adjust
            tp = c[i] + k * risk
            has_triggered_tp = False

            for j in range(i, i + n + 1):
                if c[j] > tp or h[j] > tp or o[j] > tp or l[j] > tp:
                    has_triggered_tp = True
                    break

            if has_triggered_tp:
                ret.append(1)
            else:
                ret.append(-1)

        elif tab_cor[i] == -100:  # else is bearish signal

            risk = (h[i] - c[i]) * coef_adjust
            tp = c[i] - k * risk
            has_triggered_tp = False

            for j in range(i, i + n + 1):
                if c[j] < tp or h[j] < tp or o[j] < tp or l[j] < tp:
                    has_triggered_tp = True
                    break

            if has_triggered_tp:
                ret.append(1)
            else:
                ret.append(-1)
        else:
            ret.append(0)
    return ret


def continuation_higher_than_risk_n_timeframe_with_stoploss(o, h, l, c, tab_cor, k=1, n=5, plot=False):
    ret = []
    coef_adjust = 1.02
    for i in range(0, len(tab_cor) - n - 1):
        if tab_cor[i] == 100:

            # Initializing SL and TP levels, according to the candle of the pattern, adjusted with a constant
            risk = (c[i] - l[i]) * coef_adjust
            tp = c[i] + k * risk
            sl = c[i] - risk
            has_triggered_tp = False
            has_triggered_sl = False

            # Some logs
            print(' ')
            print("################################")
            print("buy price : {:.7}".format(c[i]))
            print("tp price : {:.7}".format(tp))
            print("sl price : {:.7}".format(sl))

            # There we evaluate if the sl or tp is triggered in the next candle. Note that SL and TP can be both
            # triggered in the same candle. For this, we use random to determine which one was triggered first.
            for j in range(i + 1, i + n + 1):
                print("O : {:.7}    H : {:.7}    L : {:.7}    C : {:.7}".format(o[j], h[j], l[j], c[j]))
                if c[j] < sl or h[j] < sl or o[j] < sl or l[j] < sl:
                    has_triggered_sl = True
                    print("-- SL triggered --")

                if c[j] > tp or h[j] > tp or o[j] > tp or l[j] > tp:
                    has_triggered_tp = True
                    print("-- TP triggered --")

                if has_triggered_sl and has_triggered_tp:
                    print("-- SL AND TP BOTH TRIGGERED --")
                    if random.randint(0, 1) == 1:
                        print("-- RANDOM SAYS SL--")
                        has_triggered_tp = False
                    else:
                        print("-- RANDOM SAYS TP--")
                        has_triggered_sl = False
                    break

                if has_triggered_tp or has_triggered_sl:
                    break

            # Let's plot stuff
            if plot:
                fig, ax = plt.subplots()
                candlestick2_ohlc(ax, o[i-2:i+n+1], h[i-2:i+n+1], l[i-2:i+n+1], c[i-2:i+n+1], width=1)
                plt.axhline(sl, color='r')
                plt.axhline(tp, color='g')

            if has_triggered_tp:
                ret.append(1)
            elif has_triggered_sl:
                ret.append(-1)
            else:
                ret.append(-1)

        elif tab_cor[i] == -100:

            # Initializing SL and TP levels, according to the candle of the pattern, adjusted with a constant
            risk = (h[i] - c[i]) * coef_adjust
            tp = c[i] - k * risk
            sl = c[i] + risk
            has_triggered_tp = False
            has_triggered_sl = False

            # Some logs
            print(' ')
            print("################################")
            print("buy price : {:.7}".format(c[i]))
            print("tp price : {:.7}".format(tp))
            print("sl price : {:.7}".format(sl))

            # There we evaluate if the sl or tp is triggered in the next candle. Note that SL and TP can be both
            # triggered in the same candle. For this, we use random to determine which one was triggered first.
            for j in range(i + 1, i + n + 1):
                print("O : {:.7}    H : {:.7}    L : {:.7}    C : {:.7}".format(o[j], h[j], l[j], c[j]))
                if c[j] > sl or h[j] > sl or o[j] > sl or l[j] > sl:
                    has_triggered_sl = True
                    print("-- SL triggered --")

                if c[j] < tp or h[j] < tp or o[j] < tp or l[j] < tp:
                    has_triggered_tp = True
                    print("-- TP triggered --")

                if has_triggered_sl and has_triggered_tp:
                    print("-- SL AND TP BOTH TRIGGERED --")
                    if random.randint(0, 1) == 1:
                        has_triggered_tp = False
                        print("-- RANDOM SAYS SL--")
                    else:
                        has_triggered_sl = False
                        print("-- RANDOM SAYS TP--")
                    break

                if has_triggered_tp or has_triggered_sl:
                    break

            # Let's plot stuff
            fig, ax = plt.subplots()
            candlestick2_ohlc(ax, o[i-2:i+n+1], h[i-2:i+n+1], l[i-2:i+n+1], c[i-2:i+n+1], width=1)
            plt.axhline(sl, color='r')
            plt.axhline(tp, color='g')

            if has_triggered_tp:
                ret.append(1)
                # print("tp was triggered after {} candles".format(j-i))
            elif has_triggered_sl:
                ret.append(-1)
                # print("sl was triggered after {} candles".format(j-i))
            else:
                ret.append(-1)
                # print('Neither tp or sl were triggered')
        else:
            ret.append(0)
    return ret


