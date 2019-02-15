

def  maxLength(a, k):
	s = sum(a)
	start = 0
	end = len(a) - 1

	while start < end:
		if a[start] > a[end]:
			s -= a[start]
			start += 1
		else:
			s -= a[end]
			end -= 1

		if s <= k:
			return end - start + 1

	return 0

print maxLength([3, 1, 2, 3, 4], 3)


