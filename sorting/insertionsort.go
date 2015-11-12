package main

import (
	"fmt"
)

func main() {
	array := []int{112, 4, 3, 6, 9, 3, 4, 6, 45, 34, 6, 4, 23, 443, 13, 4, 543, 43}
	sort(array)
	fmt.Println(array)
}

func sort(array []int) {
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
