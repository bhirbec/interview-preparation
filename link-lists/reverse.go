/* Write code to partition that reverse a singly linked-list */

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
	list.Append(3)
	list.Append(4)
	list.Append(5)
	list.Append(3)
	list.Append(7)
	list.Append(8)
	list.Append(10)

	list.Print()
	list = reverse(list)
	list.Print()
}

func reverse(n *Node) *Node {
	if n.next == nil {
		return n
	}
	next := n.next
	node := reverse(next)
	n.next = nil
	next.next = n
	return node
}
