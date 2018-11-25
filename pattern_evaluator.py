import matplotlib.pyplot as plt
import numpy
import talib as ta
from influxdb import *

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
exchange = 'poloniex'
duration = '5m'
market_symbol = 'BTC/USDT'
base = market_symbol.split('/')[0]
quote = market_symbol.split('/')[1]
begin = "'2018-01-01T00:00:00Z'"
end = "'2018-10-01T00:00:00Z'"

# Getting the data
q = engine.query('SELECT * FROM {} WHERE time >= {} AND time <= {}'.format(exchange, begin, end))
data = q.get_points(tags={'duration': duration,
                          'market': market_symbol})

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

# Getting TA-lib analysis
result = ta.CDLTRISTAR(o, h, l, c)

# Plotting data and result
fig, axes = plt.subplots(nrows=2, ncols=1)
axes[0].plot(c)
axes[1].plot(result, c='orange')
plt.show()
