
class Node():
	def __init__(self, value, next=None):
		self.value = value
		self.next = next

def main():
	l1 = Node(1, Node(5, Node(7))) # 751
	l2 = Node(5, Node(6, Node(9))) # 965
	s = sum_reversed_linked_list(l1, l2) # 1716
	print_list(s)

def sum_reversed_linked_list(l1, l2):
	def _f(l1, l2, carry):
		if l1 is None and l2 is None and carry == 0:
			return None

		v = carry
		l1_next = None
		l2_next = None

		if l1 is not None:
			l1_next = l1.next
			v += l1.value

		if l2 is not None:
			l2_next = l2.next
			v += l2.value

		carry = 1 if v > 9 else 0
		n = Node(v % 10, _f(l1_next, l2_next, carry))
		return n

	return _f(l1, l2, 0)

def print_list(n):
	digits = []
	while n is not None:
		digits.append(n.value)
		n = n.next
	print ''.join(str(d) for d in digits)

if __name__ == '__main__':
	main()

