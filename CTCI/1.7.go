package main

import (
	"fmt"
)

type matrix [][]int

func (m matrix) Print() {
	n := len(m)
	for i := 0; i < n; i++ {
		fmt.Println(m[i])
	}
}

func main() {
	mat := matrix{
		[]int{1, 1, 1, 1, 1, 1},
		[]int{2, 2, 2, 2, 2, 2},
		[]int{3, 3, 3, 3, 3, 3},
		[]int{4, 4, 4, 4, 4, 4},
		[]int{5, 5, 5, 5, 5, 5},
		[]int{6, 6, 6, 6, 6, 6},
	}

	rotate(mat)

	mat.Print()
}

func rotate(mat matrix) {
	n := len(mat)

	for l := 0; l < n/2; l++ {
		last := n - 1 - l
		for i := 0; i < n-1-2*l; i++ {
			// save top
			top := mat[l][last-i]

			// right to top
			mat[l][last-i] = mat[last-i][last]

			// bottom to left
			mat[last-i][last] = mat[last][l+i]

			// right to bottom
			mat[last][l+i] = mat[l+i][l]

			// top to right
			mat[l+i][l] = top
		}
	}
}
