package sort

func MergeSort(array []int) []int {
	n := len(array)

	if n == 1 {
		return []int{array[0]}
	}

	h := n / 2
	A := MergeSort(array[:h])
	B := MergeSort(array[h:])
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
