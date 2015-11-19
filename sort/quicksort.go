package sort

import (
	"math/rand"
	"time"
)

func QuickSort(array []int) {
	n := len(array)
	if n > 1 {
		p := partition(array, n)
		QuickSort(array[:p])
		QuickSort(array[p+1:])
	}
}

func partition(array []int, n int) int {
	p := rand.Intn(n)
	pivot := array[p]
	array[p], array[0] = array[0], array[p]
	left := 0

	for i := 1; i < n; i++ {
		if array[i] < pivot {
			left++
			array[left], array[i] = array[i], array[left]
		}
	}

	if left == 0 {
		return 0
	}

	array[left], array[0] = array[0], array[left]
	return left
}

func init() {
	rand.Seed(time.Now().Unix())
}
