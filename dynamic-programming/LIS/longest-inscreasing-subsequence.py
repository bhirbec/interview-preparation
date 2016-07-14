

def main():
	array = [3, 4, -1, 0, 6, 2, 3]
	print longuest(array, len(array)-1)

def longuest(array, n):
	if n == 1:
		return 1

	lss = 0
	j = None
	for i in range(n):
		tmp = longuest(array, i)
		if tmp > lss:
			lss = tmp
			j = i

	if array[j] < array[n]:
		lss += 1

	return lss

main()
