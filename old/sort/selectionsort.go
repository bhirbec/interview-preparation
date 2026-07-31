package sort

func SelectionSort(array []int) {
	var i, j, n, min_pos int
	n = len(array)

	for i = 0; i < n-1; i++ {
		min_pos = i
		for j = i + 1; j < n; j++ {
			if array[j] < array[min_pos] {
				min_pos = j
			}
		}

		if min_pos != i {
			array[min_pos], array[i] = array[i], array[min_pos]
		}
	}
}
