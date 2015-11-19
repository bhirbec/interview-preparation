package sort

import (
	"fmt"
)

func HeapSort(array []int) []int {
	n := len(array)

	// heapify
	heap := &Heap{}
	for i := 0; i < n; i++ {
		heap.Insert(array[i])
	}

	// sort
	output := make([]int, n)
	for i := 0; i < n; i++ {
		output[i], _ = heap.Extract()
	}

	return output
}

type Heap []int

func (h *Heap) Insert(value int) {
	*h = append(*h, value)
	a := *h

	var child, parent int
	child = len(a) - 1

	for child > 0 {
		parent = (child - 1) / 2

		if a[child] < a[parent] {
			a[child], a[parent] = a[parent], a[child]
			child = parent
		} else {
			break
		}
	}
}

func (h *Heap) Extract() (int, error) {
	var parent, child int

	a := *h
	if len(a) == 0 {
		return 0, fmt.Errorf("Heap error: cannot extract value from an empty heap")
	}

	parent = 0
	last := len(a) - 1
	root := a[parent]
	a[parent] = a[last]
	*h = a[:last]
	last--

	for {
		child = 2*parent + 1 // left child
		if child > last {
			break
		}

		if right := child + 1; right <= last && a[right] < a[child] {
			child = right
		}

		if a[child] < a[parent] {
			a[parent], a[child] = a[child], a[parent]
			parent = child
		} else {
			break
		}
	}

	return root, nil
}
