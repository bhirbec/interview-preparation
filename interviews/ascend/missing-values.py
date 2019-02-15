# Enter your code here. Read input from STDIN. Print output to STDOUT
import os
import sys
from time import time
from math import exp, sqrt
from random import gauss

import numpy


def main():
    f = open(os.environ['OUTPUT_PATH'], 'w')

    prices = get_prices(f)
    for value in find_missing(prices):
        f.write(str(value) + "\n")

    f.close()

def get_prices(f):
    '''
    Read sys.input and return a list of prices. We indicate a missing price with None
    '''
    n = int(raw_input())
    prices = []
    for i in xrange(n):
        value = raw_input().split('\t')[1]
        if value.startswith('Missing'):
            prices.append(None)
        else:
            prices.append(float(value))
    return prices

def find_missing(prices):
    '''
    find_missing compute the missing prices using a Geometric Brownian Motion:
    S[t] = S[t-1]*exp((mu - 0.5*sigma**2)*dt + epsilon*sigma*sqrt(dt))

    With:
    - mu = mean of daily ROI
    - sigma = standard deviation of the prices
    - dt = time interval
    - epsilon = gauss(0, 1)
    '''

    nb_periods = len(prices)
    rates = get_rates(prices)

    sigma = numpy.std(rates)
    mu = numpy.mean(rates)

    path = [prices[0]]
    dt = 1.0 / nb_periods
    missings = []

    for t in range(1, nb_periods):

        if prices[t] is None:
            # rate_windows = rates[t-10:t+10]
            # sigma = numpy.std(rate_windows)
            # mu = numpy.mean(rate_windows)
            epsilon = gauss(0.0, 1.0)
            St = path[t - 1] * exp((mu - 0.5 * sigma ** 2) * dt + sigma * sqrt(dt) * epsilon)
            missings.append(St)
        else:
            St = prices[t]

        path.append(St)

    return missings

def get_rates(prices):
    n = len(prices)
    rates = []
    for t in xrange(n):
        prev = prices[t-1]
        current = prices[t]
        if prev is not None and current is not None:
            rates.append(current / prev - 1)
    return rates

main()

prices = [
    27.47,
    None,
    27.47,
    27.728,
    28.19,
    28.1,
    28.15,
    27.52,
    None,
    27.215,
    27.63,
    27.73,
    None,
    27.49,
    27.25,
    27.2,
    27.09,
    26.9,
    26.77
]

for v in find_missing(prices):
    print v
