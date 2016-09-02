# Given an api which returns an array of chemical names and an array of chemical symbols,
# display the chemical names with their symbol surrounded by square brackets:

# Ex:
# Chemicals array: ['Amazon', 'Microsoft', 'Google']
# Symbols: ['I', 'Am', 'cro', 'Na', 'le', 'abc']

# Output:
# [Am]azon,  Mi[cro]soft,  Goog[le]

# If the chemical string matches more than one symbol, then choose the one with longest length.
# (ex. 'Microsoft' matches 'i' and 'cro')

# My solution:
# (I sorted the symbols array in descending order of length and ran loop over chemicals array
# to find a symbol match(using indexOf in javascript) which worked. But I din't make it through
# the interview, I am guessing my solution was O(n2) and they expected an efficient algorithm.

def main():
	chemicals = ['Amazon', 'Microsoft', 'Google']
	symbols = ['i', 'Am', 'cro', 'Na', 'le', 'abc']
	print_chemicals(chemicals, symbols)

def print_chemicals(chemicals, symbols):
	symbols = sorted(symbols, reverse=True)
	for c in chemicals:
		for s in symbols:
			try:
				i = c.index(s)
			except ValueError:
				continue
			print c[:i] + '[' + s + ']' + c[i+len(s) + 1:]
			break

main()
