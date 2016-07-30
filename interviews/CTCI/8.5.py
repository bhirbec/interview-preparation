# Note: I used the first two hints to solve this problem

def multiply(a, b):
	if b == 1:
		return a

	s = multiply(a, b >> 1) << 1
	if b & 1:
		s += a

	return s

def main():
	a = 123
	b = 123312
	print multiply(a, b)
	print a * b

main()
