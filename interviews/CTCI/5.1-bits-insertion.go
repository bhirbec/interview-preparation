// From Cracking the coding interview (5.1)
// You're give two 32-bit numbers, N and M, and two bit positions, i and j. Write
// a method to insert M into N such that M starts at bit j and end at bit i. You
// can assume that the bits j throught i have enough space to fit all of M.

// Example
// N = 10000000000
// M = 10011
// i = 2 and j = 6
// output is 10001001100

package main

import (
	"fmt"
)

func main() {
	var n, m uint32
	var i, j uint

	n = 1024 * 1014
	m = 123
	i = 2
	j = 9

	output := insertBits(n, m, i, j)
	printBits(n)
	printBits(m << i)
	printBits(output)
}

func insertBits(n, m uint32, i, j uint) uint32 {
	var left, right, mask, shifted, cleared uint32

	left = ^(1<<j - 1)
	right = 1<<i - 1
	mask = left | right

	shifted = m << 2
	cleared = n & mask
	return cleared | shifted
}

func printBits(n uint32) {
	fmt.Printf("%032b\n", n)
}
