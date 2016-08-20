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

func main() {
	list := &Node{2, nil}
	list.Append(12)
	list.Append(13)
	list.Append(15)
	list.Append(13)
	list.Append(2)
	list.Append(15)
	list.Append(2)
	list.Print()

	removeDuplicate(list)
	list.Print()
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
