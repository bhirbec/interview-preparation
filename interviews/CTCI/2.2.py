
class Node():
	def __init__(self, value, next_node=None):
		self.value = value
		self.next_node = next_node

def main():
	head = Node(12, Node(10, Node(3, Node(1, Node(156, Node(43))))))
	print find_kth_from_tail(head, 2)
	print find_kth_from_tail_runner(head, 2)

	print find_kth_from_tail(None, 2)
	print find_kth_from_tail_runner(None, 2)


def find_kth_from_tail_runner(n, k):
	runner = n
	for _ in xrange(k):
		if runner is None:
			return None
		runner = runner.next_node

	while runner.next_node:
		n = n.next_node
		runner = runner.next_node

	return n.value

def find_kth_from_tail(n, k):
	def _f(n, k):
		if n is None:
			return None, -1

		k_node, l = _f(n.next_node, k)
		if k_node is not None:
			return k_node, l

		l += 1
		if l == k:
			return n, l

		return None, l

	n, l = _f(n, k)
	if n is None:
		return None
	return n.value

main()
