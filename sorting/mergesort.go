package main

import (
	"fmt"
)

func main() {
	array := []int{3, 7, 1, 5, 623, 3, 4, 65, 9, 42, 445, 23, 5, 1, 8, 6, 3, 1, 89, 324, 74, 23, 6}
	sorted := mergesort(array)
	fmt.Println(sorted)
}

func mergesort(array []int) []int {
	n := len(array)

	if n == 1 {
		return []int{array[0]}
	}

	h := n / 2
	A := mergesort(array[:h])
	B := mergesort(array[h:])
	return merge(A, B)
}

func merge(A, B []int) []int {
	i, j := 0, 0
	n1, n2 := len(A), len(B)

	n := n1 + n2
	merged := make([]int, n)

	for k := 0; k < n; k++ {
		if i < n1 && (j == n2 || A[i] < B[j]) {
			merged[k] = A[i]
			i++
		} else {
			merged[k] = B[j]
			j++
		}
	}
	return merged
}
