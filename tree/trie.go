// http://www.careercup.com/question?id=5651322294501376&PageSpeed=noscript
// Given an infinite stream of characters and a list L of strings, create a function that calls
// an external API when a word in L is recognized during the processing of the stream.

// L = ["ok","test","one","try","trying"]
// stream = a,b,c,o,k,d,e,f,t,r,y,i,n,g.............

package main

import (
	"fmt"
	"strings"
)

type Node map[string]Node

func (n Node) Insert(w string) {
	for _, s := range w {
		str := string(s)
		_, ok := n[str]
		if !ok {
			n[str] = make(Node)
		}
		n = n[str]
	}
	n[`\0`] = nil
}

func makeTrie(list []string) Node {
	n := make(Node)
	for _, w := range list {
		n.Insert(w)
	}
	return n
}

func main() {
	words := []string{"ok", "test", "one", "try", "trying"}
	trie := makeTrie(words)

	// n1 := trie["o"]["k"]
	// fmt.Println("==", n1)

	// for k, v := range trie {
	// 	fmt.Println("==", k, v)
	// }

	stream := []string{"a", "b", "c", "o", "k", "d", "t", "e", "s", "t", "t", "r", "y", "i", "n", "g"}
	word := []string{}
	n := trie

	for _, c := range stream {
		n = n[c]

		// fmt.Println(n, c)

		if n == nil {
			n = trie
			word = []string{}
		} else {
			word = append(word, c)

			if _, ok := n[`\0`]; ok {
				fmt.Println(strings.Join(word, ""))
			}
		}
	}

	// fmt.Println(stream)
}
