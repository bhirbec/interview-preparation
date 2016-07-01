# Weighed Independent Sets in Path Graph

Taken from Couresera: [Algorithm & Design Analysis Part 2](https://www.coursera.org/learn/algorithm-design-analysis-2/supplement/mfwuk/week-3-overview)

## Introduction

**Input**: a path graph G=(V, E) with non-negative weight (w) on vertices.

**Problem**: the responsability of the algorithm is to output an independent set (subset
of G so no two vertices are adjacent) with maximum total weigth.

Example:

```
o----o----o----o
1    4    5    4
```

Valid independent sets are:
- empty set
- any single vertex
- vertices 1 and 3
- vertices 1 and 4
- vertices 2 and 4

Max weigthed independent set is: vertices 2 and 2

## Optimal Solution

Notation:
- Let S = a max-weight independent set (IS)
- Let Vn = last vertex of G

Case 1: Vn not in S
- Let G' = G with Vn deleted
- S also an IS of G'
- S must be a max-weight IS of G'

Case 2: Vn in S
- Let G'' = G without Vn-1 and Vn
- previous vertex Vn-1 not in S
- S - {Vn} is an IS of G''
- S - {Vn} must in fact be a max-weight IS of G''

A max-weight IS must be either:
- (i) a max-weight IS of G' or
- (ii) vn + a max-weight IS of G''

## Proposed Algorithm

```
- recursively compute S1 = max-weight IS of G'
- recursively compute S2 = max-weight IS of G''
- return S1 or S2 U {Vn}, whichever is better
```

This algorithm is exponential time. However, there're O(n) distinct subproblems - at any time the algorithm holds a prefix of the graph. An obvious way to speed up this algorithm is to cache the solutions of the subproblems (memoization) and reuse the solutions.

With memoization the algorithm is O(n). Python implementation available [here](https://github.com/bhirbec/interview-preparation/blob/master/dynamic-programming/wis/wis.py).

## Bottom-up Algorithm

- Gi = first i vertices of G
- A = an array with A[i] = max-weight IS of Gi

```
A[0] = 0, A[1] = w1
For i = 2, 3, 4, ..., n:
	A[i] = max(A[i-1], A[i-2] + wi)
```
