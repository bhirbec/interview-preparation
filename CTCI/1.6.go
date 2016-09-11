package main

import (
	"fmt"
	"strings"
)

func main() {
	str := "aaaannnnfffgggnngg"
	comp := compress(str)
	fmt.Println(comp == "a4n4f3g3n2g2")
}

func compress(str string) string {
	n := len(str)
	count := 1
	prevChar := str[0]
	buf := []string{}

	for i := 1; i < n; i++ {
		if str[i] == prevChar {
			count++
		} else {
			buf = append(buf, string(prevChar))
			buf = append(buf, fmt.Sprintf("%d", count))
			count = 1
		}

		prevChar = str[i]
	}

	buf = append(buf, string(prevChar))
	buf = append(buf, fmt.Sprintf("%d", count))

	return strings.Join(buf, "")
}
