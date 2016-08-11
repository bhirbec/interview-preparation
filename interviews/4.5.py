

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
					value = 5
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

		# root node
		if min_val is None and max_val is None:
			return _f(n.left, min_val, n.value) and _f(n.right, n.value, max_val)

		# left only nodes
		if min_val is None:
			return (
				n.value <= max_val
				and _f(n.left, min_val, n.value)
				and _f(n.right, n.value, max_val)
			)

		# right only nodes
		if max_val is None:
			return (
				n.value >= min_val
				and _f(n.left, min_val, n.value)
				and _f(n.right, n.value, max_val)
			)

		return (
			n.value <= max_val
			and n.value >= min_val
			and _f(n.left, min_val, n.value)
			and _f(n.right, n.value, max_val)
		)


	return _f(n, None, None)

if __name__ == '__main__':
	main()
