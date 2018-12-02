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


def continuation_higher_than_risk_n_timeframe_with_stoploss(o, h, l, c, tab_cor, k=1, n=5):
    ret = []
    coef_adjust = 1.04
    for i in range(0, len(tab_cor) - n - 1):
        if tab_cor[i] == 100:

            risk = (c[i] - l[i]) * coef_adjust
            tp = c[i] + k * risk
            sl = c[i] - risk
            has_triggered_tp = False
            has_triggered_sl = False

            for j in range(i + 1, i + n + 1):
                if c[j] > tp or h[j] > tp or o[j] > tp or l[j] > tp:
                    has_triggered_tp = True
                    break
                if c[j] < sl or h[j] < sl or o[j] < sl or l[j] < sl:
                    has_triggered_sl = True
                    break

            if has_triggered_tp:
                ret.append(1)
            elif has_triggered_sl:
                ret.append(-1)
            else:
                ret.append(-1)

        elif tab_cor[i] == -100:
            risk = (h[i] - c[i]) * coef_adjust
            tp = c[i] - k * risk
            sl = c[i] + risk
            has_triggered_tp = False
            has_triggered_sl = False
            # print(' ')
            # print("################################")
            # print("buy price : {:.7}".format(c[i]))
            # print("tp price : {:.7}".format(tp))
            # print("sl price : {:.7}".format(sl))
            for j in range(i + 1, i + n + 1):
                if c[j] < tp or h[j] < tp or o[j] < tp or l[j] < tp:
                    has_triggered_tp = True
                    break
                if c[j] > sl or h[j] > sl or o[j] > sl or l[j] > sl:
                    has_triggered_sl = True
                    break

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
