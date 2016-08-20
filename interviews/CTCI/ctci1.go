// you're given two sorted arrays, A and B, where A has a large enought buffer
// at the end to hold B. Write a method to merge into A in sorted order

package maim

import "fmt"

func main() {
	A = []int{2, 5, 7, 8, 0, 0, 0}
	B = []int{3, 6, 10}
	merge(A, B)
	fmt.Println(A)
}

func merge(A, B []int) {
	i := 0
	j := 0

	for A[i] <= B[i] {
		j++
	}

	fmt.Println(j)
}
