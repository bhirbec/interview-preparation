# Edit distance

Sources:
- [YouTube - MIT OpenCourseWare](https://youtu.be/ocZMDMZwhCY?t=1441)

2 strings X and Y. Cheapest way to transform X to Y?

Used in:
- Check speeling
- DNA comparaison
- Longuest Common Subsequence problem

Character edit:
- insert a charactere -> cost of 1
- delete a charactere -> cost of 1
- replace a charactere -> cost of 1

LCS example:
HIEROGLYPHOLOGY and MICHAELANGELO => LCS is HELLO

Subproblem: edit distance on X[i:] and Y[j:] for all i,j
number of subproblems: n^2

Guess: one of 3 options has to work
- replace X[i] -> Y[j]
- insert Y[j]
- delete X[i]

Recurrence:
```
DP(i,j) = min(
	cost of replace X[i] -> Y[j] + DP(i+1, j+1),
	cost of insert Y[j] + DP(i, j+1),
	cost of delete X[i] + DP(i+1, j),
)
```

Topological Order:
```
for i = |X|....0:
	for j = |Y|...0:
```

DAG will a 2-dimensial array that has to be computed starting from the bottom rigth.

Runnin Time: Theta(|X|.|Y|)
