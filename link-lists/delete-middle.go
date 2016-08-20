/* implement an algorithm to delete a node in the middle of a singly linked list, give
only access to that node */

package main

import (
	"fmt"
)

type Node struct {
	data int
	next *Node
}

func (n *Node) Append(data int) *Node {
	for n.next != nil {
		n = n.next
	}

	n.next = &Node{data, nil}
	return n.next
}

func (n *Node) Print() {
	for n != nil {
		fmt.Printf("%d ", n.data)
		n = n.next
	}
	fmt.Print("\n")
}

func main() {
	list := &Node{1, nil}
	list.Append(2)
	middle := list.Append(3)
	list.Append(4)
	list.Append(5)
	list.Print()

	deleteNode(middle)
	list.Print()
}

func deleteNode(n *Node) {
	*n = *n.next
}
