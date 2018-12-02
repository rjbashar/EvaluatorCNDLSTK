import matplotlib.pyplot as plt
import numpy
import talib as ta
from influxdb import *

import eval


def get_data(begin, end, exchange, duration, market_symbol):
    # InfluxDB configuration
    db_host = 'black'
    db_port = 8086
    db_user = 'CryptoMarketDataCollector'
    db_pw = '01101011'
    db_name = 'CryptoMarketData'
    engine = InfluxDBClient(host=db_host, port=db_port, username=db_user, password=db_pw, database=db_name)
    engine.switch_database(db_name)
    engine.switch_user(db_user, db_pw)

    # Configure input data
    base = market_symbol.split('/')[0]
    quote = market_symbol.split('/')[1]

    # Getting the data
    q = engine.query('SELECT * FROM {} WHERE time >= {} AND time <= {}'.format(exchange, begin, end))
    data = q.get_points(tags={'duration': duration,
                              'market': market_symbol})
    return data


def format_data(data):
    # Formatting data
    closes = []
    opens = []
    highs = []
    lows = []
    for line in data:
        closes.append(line['close'])
        opens.append(line['open'])
        highs.append(line['high'])
        lows.append(line['low'])

    o = numpy.array(opens, dtype=float)
    h = numpy.array(highs, dtype=float)
    l = numpy.array(lows, dtype=float)
    c = numpy.array(closes, dtype=float)
    return o, h, l, c


def plot(o, h, l, c, tab_cor, eval):
    # Plotting data and result
    fig, axes = plt.subplots(nrows=3, ncols=1)
    axes[0].plot(c)
    axes[1].plot(tab_cor, c='orange')
    axes[2].plot(eval, c='green')
    plt.show()


def main():
    begin = "'2017-01-05T00:00:00Z'"
    end = "'2018-11-01T10:00:00Z'"
    exchange = 'poloniex'
    duration = '5m'
    market_symbol = 'BTC/USDT'
    data = get_data(begin, end, exchange, duration, market_symbol)
    o, h, l, c = format_data(data)

    tab_cor = ta.CDLSHOOTINGSTAR(o, h, l, c)

    koef = 5
    candle_timeframe = 30
    evaluation = eval.continuation_higher_than_risk_n_timeframe_with_stoploss(o, h, l, c, tab_cor, k=koef,
                                                                              n=candle_timeframe)
    plot(o, h, l, c, tab_cor, evaluation)

    win = 0
    loss = 0
    for i in evaluation:
        if i > 0:
            win += 1
        elif i < 0:
            loss += 1

    # Let's print all the stuff
    print("##################################################################")
    print("Benchmark between {} {} and {} {}".format(begin[1:11], begin[12:-2], end[1:11], end[12:-2]))
    print("Benchmark on {} {} chart from {}".format(market_symbol, duration, exchange))
    print("Win Trade          : {}".format(win))
    print("Loss Trade         : {}".format(loss))
    total = win + loss
    print("Total Trade        : {}".format(total))
    win_rate = 100 * (win / total)
    print("Win Rate           : {:.5} %".format(win_rate))
    loss_rate = 100 * (loss / total)
    print("Loss Rate          : {:.5} %".format(loss_rate))
    print("TP/SL coef (k)     : {}".format(koef))
    exp = win * koef - 1 * loss
    print("Expectancy (R)     : {} R".format(exp))
    exp_moy = exp / total
    print("Expectancy (R moy) : {:.5}".format(exp_moy))
    gain = (100 * (1 + (exp_moy / 100)) ** total)
    print("With R=1%          : {:.5} % final capital".format(gain))
    print("TODO : Add max_drawdown, longest_loss_streak")
    print("##################################################################")


if __name__ == '__main__':
    main()
