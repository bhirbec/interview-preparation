# Given an api which returns an array of chemical names and an array of chemical symbols,
# display the chemical names with their symbol surrounded by square brackets:

# Ex:
# Chemicals array: ['Amazon', 'Microsoft', 'Google']
# Symbols: ['I', 'Am', 'cro', 'Na', 'le', 'abc']

# Output:
# [Am]azon,  Mi[cro]soft,  Goog[le]

# If the chemical string matches more than one symbol, then choose the one with longest length.
# (ex. 'Microsoft' matches 'i' and 'cro')

def main():
	chemicals = ['Amazon', 'Microsoft', 'Google']
	symbols = ['i', 'Am', 'cro', 'Na', 'le', 'abc']
	print_chemicals(chemicals, symbols)

def print_chemicals(chemicals, symbols):
	sort_func = lambda x, y: len(x) > len(y)
	symbols = sorted(symbols, cmp=sort_func)

	for c in chemicals:
		for s in symbols:
			try:
				i = c.index(s)
			except ValueError:
				continue
			print '{0}[{1}]{2}'.format(c[:i], s, c[i+len(s):])
			break

main()
