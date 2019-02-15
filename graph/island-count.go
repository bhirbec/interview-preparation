package main

import (
	"errors"
	"fmt"
)

// You're given a matrix that stores the following values:
// - "L" (land)
// - "W" (water)
//
// For instance:
// "W", "L", "W", "L"
// "W", "L", "L", "W"
// "W", "L", "W", "L"
//
// Compute the size of the biggest island (4 )

func main() {
	matrix := [][]string{
		[]string{"L", "W", "W", "L"},
		[]string{"L", "W", "L", "L"},
		[]string{"L", "W", "W", "L"},
	}

	fmt.Println(findBiggestLand(matrix))
	fmt.Println(findBiggestLand2(matrix))
}

func findBiggestLand(matrix [][]string) int {
	/* DFS with recursion  */
	visitedNodes := make(map[[2]int]bool)
	var dfs func(i, j int) int

	dfs = func(i, j int) int {
		if i < 0 || j < 0 {
			return 0
		}

		key := [2]int{i, j}
		_, visited := visitedNodes[key]

		if visited {
			return 0
		} else {
			visitedNodes[key] = true
		}

		s := 0
		var value string

		func() {
			defer func() {
				err := recover()
				if err != nil {
					value = "W"
				}
			}()

			value = matrix[i][j]
		}()

		if value == "L" {
			s += 1
		} else {
			return 0
		}

		s += dfs(i+1, j)
		s += dfs(i, j+1)
		s += dfs(i-1, j)
		s += dfs(i, j-1)

		return s
	}

	max_s := 0

	for i, n := 0, len(matrix); i < n; i++ {
		for j, m := 0, len(matrix[i]); j < m; j++ {
			if s := dfs(i, j); s > max_s {
				max_s = s
			}
		}
	}

	return max_s
}

type point struct {
	i, j int
}

func findBiggestLand2(matrix [][]string) int {
	/* BFS based version */
	visited := make(map[point]bool)

	explore := func(p point) int {
		var value string
		var area int
		stack := NewStack()
		stack.Push(p)

		for stack.Length() > 0 {
			iPoint, err := stack.Pop()
			if err != nil {
				return -1
			}

			p := iPoint.(point)

			if visited[p] {
				continue
			} else {
				visited[p] = true
			}

			func() {
				defer func() {
					err := recover()
					if err != nil {
						value = "W"
					}
				}()

				value = matrix[p.i][p.j]
			}()

			if value == "W" {
				continue
			} else {
				area += 1
			}

			points := []point{
				point{p.i + 1, p.j},
				point{p.i, p.j + 1},
				point{p.i - 1, p.j},
				point{p.i, p.j - 1},
			}

			for i := 0; i < 4; i++ {
				p := points[i]
				if p.i > -1 && p.j > -1 {
					stack.Push(p)
				}
			}
		}
		return area
	}

	maxArea := 0
	for i, n := 0, len(matrix); i < n; i++ {
		for j, m := 0, len(matrix[i]); j < m; j++ {
			area := explore(point{i, j})
			if area > maxArea {
				maxArea = area
			}
		}
	}

	return maxArea
}

type Stack struct {
	s []interface{}
}

func NewStack() *Stack {
	list := make([]interface{}, 0)
	return &Stack{list}
}

func (s *Stack) Length() int {
	return len(s.s)
}

func (s *Stack) Push(v interface{}) {
	s.s = append(s.s, v)
}

func (s *Stack) Pop() (interface{}, error) {
	l := len(s.s)
	if l == 0 {
		return nil, errors.New("Empty Stack")
	}

	res := s.s[l-1]
	s.s = s.s[:l-1]
	return res, nil
}
