package sort

import (
	"math/rand"
	"time"
)

func QuickSort(array []int) {
	n := len(array)
	if n > 0 {
		quickSort(array, 0, n-1)
	}
}

func quickSort(array []int, l, r int) {
	if r-l > 0 {
		p := partition(array, l, r)
		quickSort(array, 0, p-1)
		quickSort(array, p+1, r)
	}
}

func partition(array []int, l, r int) int {
	p := rand.Intn(r-l+1) + l
	pivot := array[p]
	array[p], array[l] = array[l], array[p]
	i := l + 1

	for j := l + 1; j < r+1; j++ {
		if array[j] < pivot {
			array[j], array[i] = array[i], array[j]
			i++
		}
	}

	array[l], array[i-1] = array[i-1], array[l]
	return i - 1
}

func init() {
	rand.Seed(time.Now().Unix())
}
