package main

import (
	"fmt"
	"math/rand"
	"time"
)

func main() {
	array := []int{2, 4, 6, 2, 2, -2, 2, 3, 6, -4, 5, 6, 8, 5, 7, 8}
	Quicksort(array)
	fmt.Println(array)
}

func Quicksort(array []int) {
	n := len(array)
	if n > 1 {
		p := partition(array, n)
		Quicksort(array[:p])
		Quicksort(array[p+1:])
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
