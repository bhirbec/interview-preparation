package sort

import (
	"testing"
)

func TestHeapSort(t *testing.T) {
	array := []int{2, 4, 6, 2, 2, -2, 2, 3, 6, -4, 5, 6, 8, 5, 7, 8}
	sorted := HeapSort(array)

	if !IsSorted(sorted) {
		t.Errorf("HeapSort returned an unsorted array")
	}
}

func TestInsertionSort(t *testing.T) {
	array := []int{112, 4, 3, 6, 9, 3, 4, 6, 45, 34, 6, 4, 23, 443, 13, 4, 543, 43}
	InsertionSort(array)

	if !IsSorted(array) {
		t.Errorf("InsertionSort returned an unsorted array")
	}
}

func TestMergeSort(t *testing.T) {
	array := []int{3, 7, 1, 5, 623, 3, 4, 65, 9, 42, 445, 23, 5, 1, 8, 6, 3, 1, 89, 324, 74, 23, 6}
	sorted := MergeSort(array)

	if !IsSorted(sorted) {
		t.Errorf("MergeSort returned an unsorted array")
	}
}

func TestSelectionSort(t *testing.T) {
	array := []int{1, 4, 5, 3, 4, 6, 7, 34, 5, 2, 3, 545, -43, 3}
	SelectionSort(array)

	if !IsSorted(array) {
		t.Errorf("SelectionSort returned an unsorted array")
	}
}

func TestQuickSort(t *testing.T) {
	array := []int{2, 4, 6, 2, 2, -2, 2, 3, 6, -4, 5, 6, 8, 5, 7, 8}
	QuickSort(array)

	if !IsSorted(array) {
		t.Errorf("QuickSort returned an unsorted array")
	}
}
