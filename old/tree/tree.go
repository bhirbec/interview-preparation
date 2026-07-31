package tree

import (
	"fmt"

	"github.com/bhirbec/Algorithms-And-Data-Structures/sort"
)

type Node struct {
	left, right *Node
	value       int
}

// MakeBTS make a BTS from the given sorted array. It returns an
// error if the given array isn't sorted in ascending order.
func MakeBTS(array []int) (*Node, error) {
	if !sort.IsSorted(array) {
		return nil, fmt.Errorf("Tree error: input array must be sorted.")
	}
	return makeBTS(array), nil
}

func makeBTS(array []int) *Node {
	n := len(array)
	if n < 1 {
		return nil
	}

	l := n / 2
	left := makeBTS(array[:l])
	right := makeBTS(array[l+1:])
	return &Node{left, right, array[l]}
}

// IsBSTNaive returns true is the given tree is a BST. Otherwise returns false.
// Time complexity is O(n**2)
// Space complexity is O(h)
func IsBSTNaive(n *Node) bool {
	if n == nil {
		return true
	}

	return isSubtreeLesser(n.left, n.value) &&
		isSubtreeGreater(n.right, n.value) &&
		IsBSTNaive(n.left) &&
		IsBSTNaive(n.right)
}

func isSubtreeLesser(n *Node, value int) bool {
	if n == nil {
		return true
	}

	return n.value <= value &&
		isSubtreeLesser(n.left, value) &&
		isSubtreeLesser(n.right, value)
}

func isSubtreeGreater(n *Node, value int) bool {
	if n == nil {
		return true
	}

	return n.value >= value &&
		isSubtreeGreater(n.left, value) &&
		isSubtreeGreater(n.right, value)
}
