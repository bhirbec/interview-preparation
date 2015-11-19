package tree

import (
	"testing"
)

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
