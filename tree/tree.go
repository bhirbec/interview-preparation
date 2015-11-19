package tree

type Node struct {
	left, right *Node
	value       int
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
