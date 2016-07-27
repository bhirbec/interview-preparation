# Implement a function to check if a binary tree is balanced. For the purpose of this
# question, a balanced tree is defined to be a tree such that the heigths of the two
# subtrees of any node nver differ by more one.


def is_balanced(n):
	return check_depth(n) != -1

def check_depth(n):
	if n is None:
		return 0

	left = check_depth(n.get('left'))
	if left == -1:
		return -1

	right = check_depth(n.get('right'))
	if right == -1:
		return -1

	diff = abs(left - right)
	if diff > 1:
		return -1

	return max(left, right) + 1


root = {
	'left': {
		'left': {
			'left': {
				'left': {},
				'right': {},
			},
			'right': {
				'left': {},
				'right': {},
			},
		},
		'right': {
			'left': {
				'left': {},
				'right': {},
			},
			'right': {
				'left': {},
				'right': {},
			},
		},
	},
	'right': {
		'left': {
			'left': {
				'left': {},
				'right': {},
			},
			'right': {
				'left': {},
				'right': {},
			},
		},
		'right': {
			'left': {
				'left': {},
				'right': {},
			},
			'right': {
				'left': {},
				'right': {},
			},
		},
	},
}

print is_balanced(root)
