'''
This is a simple text-justification implementation that uses Dynamic Programming. The purpose
of this script is to illustrate the Text-Justification section of the MIT OpenCourseWare available
on YouTube:

https://youtu.be/ENyox7kNKeY?list=PLfMspJ0TLR5HRFu2kLh3U4mvStMO8QURm

Please, note this implementation doesn't take into account punctuation and doesn't flush the line
to the right.
'''

import sys


def justify(words, page_width=40):
	n = len(words)
	memo = {}

	def _dp(i):
		if i == n:
			return 0, None

		if i in memo:
			return memo[i]

		min_cost = None
		parent_pointer = None
		for j in range(i+1, n+1):
			cost_dp_j, pointer = _dp(j)
			cost = _cost(i, j) + cost_dp_j
			if cost < min_cost or min_cost is None:
				min_cost = cost
				parent_pointer = (j, pointer)

		memo[i] = min_cost, parent_pointer
		return memo[i]

	def _cost(i, j):
		line_width = sum(len(words[k]) for k in xrange(i, j)) + (j - i - 1)
		if line_width > page_width:
			return sys.maxint
		else:
			return (page_width - line_width)**3

	_, seq = _dp(0)

	i = 0
	while seq is not None:
		j, seq = seq[0], seq[1]
		print ' '.join(words[i:j])
		i = j

if __name__ == '__main__':
	words = [
		'A', 'common', 'type', 'of', 'text', 'alignment', 'in', 'print', 'media', 'is', '"justification",',
		'where', 'the', 'spaces', 'between', 'words,', 'and,', 'to', 'a', 'lesser', 'extent,', 'between', 'glyphs',
		'or', 'letters,', 'are', 'stretched', 'or', 'compressed', 'to', 'align', 'both', 'the', 'left', 'and', 'right',
		'ends', 'of', 'each', 'line', 'of', 'text.', 'When', 'using', 'justification,', 'it', 'is', 'customary', 'to',
		'treat', 'the', 'last', 'line', 'of', 'a', 'paragraph', 'separately', 'by', 'simply', 'left', 'or', 'right',
		'aligning', 'it,', 'depending', 'on', 'the', 'language', 'direction.', 'Lines', 'in', 'which', 'the', 'spaces',
		'have', 'been', 'stretched', 'beyond', 'their', 'normal', 'width', 'are', 'called', 'loose', 'lines,', 'while',
		'those', 'whose', 'spaces', 'have', 'been', 'compressed', 'are', 'called', 'tight', 'lines.'
	]
	justify(words, 50)
