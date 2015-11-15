package main

import (
	"fmt"
	"math/rand"
	"time"
)

func main() {
	array := []int{2, 4, 6, 5, 7, 3, 4, 6, 7, 8, 5, 4}
	Quicksort(array)
	fmt.Println(array)
}

func Quicksort(array []int) {
	quicksort(array, 0, len(array)-1)
}

func quicksort(array []int, start, stop int) {
	if stop > start {
		p := partition(array, start, stop)
		quicksort(array, start, p-1)
		quicksort(array, p+1, stop)
	}
}

func partition(array []int, start, stop int) int {
	p := uniform(start, stop)
	pivot := array[p]

	for start < stop {
		for array[start] < pivot {
			start++
		}

		for array[stop] > pivot {
			stop--
		}

		array[start], array[stop] = array[stop], array[start]

		if start == p {
			p = stop
		} else if stop == p {
			p = start
		}

		if p != start {
			start++
		}

		if p != stop {
			stop--
		}
	}
	return p
}

func init() {
	rand.Seed(time.Now().Unix())
}

func uniform(min, max int) int {
	return rand.Intn(max+1-min) + min
}
