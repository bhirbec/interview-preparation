
def main():
	m = 5
	n = 161
	r = insert_bits(n=n, m=m, i=2, j=4)
	print_bin(n)
	print_bin(m)
	print_bin(r)

def insert_bits(n, m, i, j):
	left = (1 << (j + 1)) - 1
	right = (1 << i) - 1
	mask = ~(left ^ right)
	n &= mask
	m = m << i
	return n | m

def print_bin(v):
	print v, '{0:08b}'.format(v)

if __name__ == '__main__':
	main()
