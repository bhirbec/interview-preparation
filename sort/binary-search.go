package sort

import (
	"fmt"
)

func main() {
	array := []int{1, 2, 4, 5, 6, 7, 8, 12, 14, 16, 17, 19, 21, 23, 25, 34, 45, 46}
	fmt.Println(BinarySearch(array, 12))
	fmt.Println(BinarySearch(array, 13))
}

func BinarySearch(array []int, value int) int {
	return binarySearch(array, 0, len(array)-1, value)
}

func binarySearch(array []int, start, end, value int) int {
	if end < start {
		return -1
	}

	middle := (start + end) / 2
	current := array[middle]

	if current == value {
		return middle
	} else if value < current {
		return binarySearch(array, start, middle-1, value)
	} else {
		return binarySearch(array, middle+1, end, value)
	}
}
