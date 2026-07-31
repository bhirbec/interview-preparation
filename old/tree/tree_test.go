package tree

import (
	"testing"
)

func TestMakeBTS(t *testing.T) {
	array := []int{1, 3, 4, 6, 7, 8, 10, 12, 13, 15, 16, 17}
	root, _ := MakeBTS(array)

	if !IsBSTNaive(root) {
		t.Error("MakeBTS failed.")
	}
}

func TestIsBSTNaive(t *testing.T) {
	tree := &Node{
		value: 12,
		left: &Node{
			value: 8,
			left: &Node{
				value: 4,
				left:  nil,
				right: nil,
			},
			right: &Node{
				value: 11,
				left:  nil,
				right: nil,
			},
		},
		right: &Node{
			left:  nil,
			right: nil,
			value: 14,
		},
	}

	if !IsBSTNaive(tree) {
		t.Errorf("Excepted BTS")
	}
}
