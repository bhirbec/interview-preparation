# https://www.careercup.com/question?id=5631060781039616

# Given a string return the longest palindrome that can be constructed by removing or shuffling characters.

# Example:
# 'aha'  -> 'aha'
# 'ttaatta' -> ' ttaaatt'
# 'abc' -> 'a' or 'b' or 'c'
# 'gggaaa' -> 'gaaag' or 'aggga'

# Note if there are multiple correct answers you only need to return 1 palindrome.</p>

def main(s):
	'''
	Time complexity: O(n x log(n))
	Space complexity: O(n)
	- set a map that stores number of occurences per character
	- we can keep characters having an even number of occurences
	- characters having odd number of occurences can only go in the middle. So
	  we take them by decreasing order and remove 1 to keep them
	TODO: can we do O(n)?
	'''
	char_counts = {}
	for c in s:
		if c in char_counts:
			char_counts[c] += 1
		else:
			char_counts[c] = 1

	kept = []
	odd_chars = []

	for c, count in char_counts.iteritems():
		if (count % 2) == 0:
			kept.append((count, c))
		else:
			odd_chars.append((count, c))

	odd_chars.sort(key=lambda item: item[0], reverse=1)

	nb_odds = len(odd_chars)
	for i in xrange(nb_odds-1):
		count, c = odd_chars[i]
		if count > 1:
			kept.append((count-1, c))

	output = []
	for count, c in kept:
		for i in xrange(count / 2):
			output.append(c)

	middle = odd_chars[nb_odds-1][1] if nb_odds > 0 else ''
	print ''.join(output) + middle + '' .join(reversed(output))

main(s="baazzxkkkuiuoioiikaab")
