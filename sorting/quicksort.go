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
	n := len(array)
	if n > 1 {
		p := partition(array, n)
		Quicksort(array[:p])
		Quicksort(array[p:])
	}
}

func partition(array []int, n int) int {
	p := rand.Intn(n)
	pivot := array[p]

	start := 0
	stop := n - 1

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
