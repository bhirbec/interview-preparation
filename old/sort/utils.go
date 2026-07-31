package sort

// IsSorted returns true if the given array is sorted. Otherwise returns false.
func IsSorted(array []int) bool {
	n := len(array)
	if n == 1 {
		return true
	}

	value := array[0]
	for i := 1; i < n; i++ {
		if value > array[i] {
			return false
		}
	}

	return true
}
