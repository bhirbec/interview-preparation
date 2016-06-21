# http://www.geeksforgeeks.org/tree-isomorphism-problem

# Write a function to detect if two trees are isomorphic. Two trees are called isomorphic if
# one of them can be obtained from other by a series of flips, i.e. by swapping left and right
# children of a number of nodes. Any number of nodes at any level can have their children swapped.
# Two empty trees are isomorphic.

A = dict(
	data=12,
	left=dict(
		data=15
	),
	right=dict(
		data=17
	)
)

B = dict(
	data=12,
	left=dict(
		data=17
	),
	right=dict(
		data=15
	)
)

def main():
	print isIsomorphic(A, B)

def isIsomorphic(a, b):
	if a is None and b is None:
		return True

	if a is None or b is None:
		return False

	if a['data'] != b['data']:
		return False

	a_left = a.get('left')
	a_right = a.get('right')
	b_left = b.get('left')
	b_right = b.get('right')

	return (isIsomorphic(a_left, b_left) and isIsomorphic(a_right, b_right)) \
		or (isIsomorphic(a_left, b_right) and isIsomorphic(a_right, b_left))


main()

