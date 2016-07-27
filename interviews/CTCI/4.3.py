# Given a sorted (increasing order) array with unique integer elements, write an
# algotithm to create a binary search tree with minimal height.

class Node(object):
	def __init__(self, left, right, value):
		self.left = left
		self.right = right
		self.value = value

def main():
	array = [1, 2, 3, 4]
	n = make_bst(array)
	in_order_traversal(n)

def make_bst(array):
	n = len(array)
	return _make_bst(array, 0, n-1)

def _make_bst(array, i, j):
	n = j - i
	if n < 0:
		return None

	mid = i + n / 2
	left = _make_bst(array, i, mid-1)
	right = _make_bst(array, mid+1, j)
	return Node(left, right, array[mid])

def in_order_traversal(n):
	if n is None:
		return

	in_order_traversal(n.left)
	print n.value
	in_order_traversal(n.right)

main()
