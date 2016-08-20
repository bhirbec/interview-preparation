/* Write code to partition a linked list around a value x, such that all nodes
less than x come before all node greater than or equal to x */

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
	list := makeList()
	list.Print()
	partition(list, 4)
	list.Print()
}

func makeList() *Node {
	list := &Node{1, nil}
	list.Append(2)
	list.Append(3)
	list.Append(4)
	list.Append(5)
	list.Append(3)
	list.Append(7)
	list.Append(8)
	list.Append(10)
	return list
}

func partition(n *Node, x int) *Node {
	var l1, l2, n1, n2, next *Node

	for n != nil {
		next = n.next
		n.next = nil

		if n.data < x {
			if l1 == nil {
				l1 = n
				n1 = l1
			} else {
				n1.next = n
				n1 = n1.next
			}
		} else {
			if l2 == nil {
				l2 = n
				n2 = l2
			} else {
				n2.next = n
				n2 = n2.next
			}
		}
		n = next
	}

	if l1 == nil {
		return l2
	}

	n1.next = l2
	return l1
}
