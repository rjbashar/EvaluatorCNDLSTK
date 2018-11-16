import talib as ta
import numpy
import matplotlib.pyplot as plt

original_data = [
    ['1/22/14', 10, 18,  5, 20],
    ['1/23/14', 12, 21,  7, 22],
    ['1/24/14', 14, 24, 9 , 24],
    ['1/25/14', 16, 27, 11, 26],
    ['1/26/14', 18, 30, 13, 28],
    ['1/27/14', 20, 33, 15, 30],
    ['1/28/14', 22, 36, 17, 32],
    ['1/29/14', 24, 39, 19, 34],
    ['1/30/14', 26, 41, 21, 38],
    ['1/31/14', 30, 45, 25, 40],
    ['2/01/14', 43, 44, 42, 43],
    ['2/02/14', 46, 47, 45, 46],
    ['2/03/14', 44, 45, 43, 44],
    ['2/04/14', 40, 55, 35, 50]
]

# convert data to columns
columnar_data = numpy.column_stack(original_data)

# extract the columns we need, making sure to make them 64-bit floats
dates = columnar_data[0].astype(str)
open = columnar_data[1].astype(float)
high = columnar_data[2].astype(float)
low = columnar_data[3].astype(float)
close = columnar_data[4].astype(float)

result = ta.CDLTRISTAR(open, high, low, close)

plt.plot(close)
plt.plot(result)
plt.show()
