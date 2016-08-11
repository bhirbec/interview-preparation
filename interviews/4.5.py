

class Node():
	def __init__(self, value, left=None, right=None):
		self.value = value
		self.left = left
		self.right = right

def main():
	n = Node(
		value = 10,
		left = Node(
			value = 5,
			left = Node(
				value = 2,
				left = Node(
					value = 1
				),
				right = Node(
					value = 3
				)
			),
			right = Node(
				value = 7,
				left = Node(
					value = 6
				),
				right = Node(
					value = 8
				)
			)
		),
		right = Node(
			value = 15,
			left = Node(
				value = 12
			),
			right = Node(
				value = 41
			)
		)
	)

	print is_bst(n)

def is_bst(n):
	def _f(n, min_val, max_val):
		if n is None:
			return True

		if (min_val is not None and n.value <= min_val) or (max_val is not None and n.value >= max_val):
			return False

		return _f(n.left, min_val, n.value) and _f(n.right, n.value, max_val)

	return _f(n, None, None)

if __name__ == '__main__':
	main()
