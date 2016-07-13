# Knapsack Problem

Sources:
- [Coursera - Algorithm & Design Analysis Part 2](https://www.coursera.org/learn/algorithm-design-analysis-2/lecture/LIgLJ/the-knapsack-problem)
- [YouTube - MIT OpenCourseWare](https://youtu.be/ocZMDMZwhCY?t=2589)

## Definition

**Input:**
- n items - each having a value v<sub>i</sub> and a size w<sub>i</sub> (both integrals)
- capacity W

**Output**: a subset S &sube; {1, 2, ..., n}:
- that maximizes &Sigma;w<sub>i</sub>
- &Sigma;w<sub>i</sub> &le; W

## Optimal Solution

### Formulate the Recurrence

Let S = a max-value solution to an instance of Knapsack

It helps to think of the items to be ordered. Either the last item belongs to S or it doesn't.
- last item &notin; S => S must be optimal with n - 1 items
- last item &isin; S => S - {n} is an optimal solution with respect to the first n - 1 items and capacity W - w<sub>n</sub>

Let V<sub>i, x</sub> equals value of the best solution that:
- uses only first i items
- has total size &le; W 

**Recurrence => V<sub>i, x</sub> = max(V<sub>i-1, x</sub> , v<sub>i</sub> + V<sub>i-1, x-1</sub>)**

If w<sub>i</sub> &gt; x, must have V<sub>i, x</sub> = V<sub>i-1, x</sub>

### Identify Subproblems

Subproblems are:
- all possible prefixes of items {1, 2, ..., n}
- all possible (integral) residual capacities x &isin; {0, 1, 2, ..., W}

Speudo-Code:
```
let A = 2-D array

for x = 0 to W:
	A[0, x] = 0

for i = 1 to n:
	for x = 0 to W:
		A[i][x] = max(A[i-1][x], A[i-1, x-1] + vi)
```

Time complexity is &Theta;(nW) - Pseudo-polynomial.
