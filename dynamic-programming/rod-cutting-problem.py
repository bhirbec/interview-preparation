# https://www.youtube.com/watch?v=sF7hzgUW5uY
# Given the n''-wide rod, that's the best way to cut it
# so it maximize your profit?

# Inputs:
# - a n''-wide rod
# - Pi => spot price for a i''-wide rod (P1, P2..., Pn)

# Goal: Maximize profit <=> find a set of cut i1, i2..., iK such that
#  K
# SUM ij <= n
# j=0

#      K
# max SUM Pij
#     j=0

def main():
	prices = [
		0,
		2,  # spot prices for a rod of size 1''
		7,  # spot prices for a rod of size 2''
		10, # spot prices for a rod of size 3''
		12,
		13,
		16,
		17,
		18,
		23
	]

	n = len(prices) - 1
	print rod_cutting_recursive(prices, n)
	print rod_cutting_bottom_up(prices, n)

def rod_cutting_recursive(prices, n):
	cache = {}

	def _rod_cutting(prices, n):
		if n < 1:
			return 0

		profit = cache.get(n)
		if profit is not None:
			return profit

		profit = prices[n]

		for i in xrange(1, n):
			tmp = prices[i] + _rod_cutting(prices, n-i)
			if tmp > profit:
				profit = tmp

		cache[n] = profit
		return profit

	return _rod_cutting(prices, n)

def rod_cutting_bottom_up(prices, n):
	profits = [0] * (n+1)

	for i in xrange(1, n+1):
		cut = None
		for j in xrange(1, i+1):
			tmp = prices[j] + profits[i-j]
			if tmp > profits[i]:
				profits[i] = tmp

	return profits[n]

main()
