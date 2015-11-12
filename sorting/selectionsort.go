package main

import (
	"fmt"
)

func main() {
	array := []int64{1, 4, 5, 3, 4, 6, 7, 34, 5, 2, 3, 545, -43, 3}
	sort(array)
	fmt.Println(array)
}

func sort(array []int64) {
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
