package sort

func InsertionSort(array []int) {
	n := len(array)

	for i := 1; i < n; i++ {
		saved := array[i]

		j := i - 1
		for j >= 0 && array[j] > saved {
			array[j+1] = array[j]
			j--
		}
		j++

		if i != j {
			array[j] = saved
		}
	}
}
