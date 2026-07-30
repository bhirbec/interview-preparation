/* Write code to remove duplicates from an unsorted linked list */
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

func removeDuplicate(n *Node) {
	distincts := make(map[int]bool)
	var previous *Node

	for n != nil {
		if distincts[n.data] {
			previous.next = n.next
			n = previous
		} else {
			distincts[n.data] = true
			previous = n
		}

		n = n.next
	}

}
