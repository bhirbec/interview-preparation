package main

import (
	"bytes"
	hash "crypto/sha1"
	"encoding/binary"
	"fmt"
	"strconv"
)

// --- Hash table

type Hashtable struct {
	buckets      []*Node
	nbOfBuckets  uint32
	nbOfElements int64
}

func New(nbOfBuckets uint32) *Hashtable {
	buckets := make([]*Node, nbOfBuckets)
	return &Hashtable{buckets, nbOfBuckets, 0}
}

func (h *Hashtable) Insert(key string, value int64) {
	num := hashFunc(key) % h.nbOfBuckets
	node := h.buckets[num]
	newNode := &Node{&NodeData{key, value}, nil}

	if node == nil {
		h.buckets[num] = newNode
		h.nbOfElements++
	} else {
		update := findNode(node, key)
		if update != nil {
			update.data.value = value
		} else {
			newNode.next = node
			h.buckets[num] = newNode
			h.nbOfElements++
		}
	}
}

func (h Hashtable) Lookup(key string) (int64, bool) {
	num := hashFunc(key) % h.nbOfBuckets
	node := h.buckets[num]
	node = findNode(node, key)
	if node != nil {
		return node.data.value, true
	}
	return 0, false
}

func findNode(n *Node, key string) *Node {
	for n != nil {
		if n.data.key == key {
			return n
		}
		n = n.next
	}
	return nil
}

func hashFunc(key string) uint32 {
	var out uint32
	hashBytes := hash.Sum([]byte(key))
	buf := bytes.NewBuffer(hashBytes[:])
	binary.Read(buf, binary.LittleEndian, &out)
	return out
}

// --- link list
type NodeData struct {
	key   string
	value int64
}

type Node struct {
	data *NodeData
	next *Node
}

func (n *Node) Insert(data *NodeData) *Node {
	for n.next != nil {
		n = n.next
	}
	n.next = &Node{data, nil}
	return n.next
}

func (n *Node) Count() int64 {
	var i int64
	for n != nil {
		n = n.next
		i++
	}
	return i
}

func (n *Node) Print() {
	for n != nil {
		fmt.Println(n.data.value)
		n = n.next
	}
}

func main() {
	table := New(1000)

	for i := 0; i < 20000; i++ {
		key := strconv.Itoa(i)
		table.Insert(key, int64(i))
	}

	missing := 0
	for i := 0; i < 20000; i++ {
		key := strconv.Itoa(i)
		_, ok := table.Lookup(key)
		if !ok {
			missing++
		}
	}

	fmt.Println("Missing: ", missing)

	for _, n := range table.buckets {
		if n != nil {
			fmt.Println(n.Count())
		} else {
			fmt.Println("Empty")
		}
	}
}
