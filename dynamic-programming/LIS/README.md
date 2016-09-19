# Longest Increasing Subsequence

Problem:
For a vector of size N, find its LIS

Example:
```
D = 3, 2, 6, 4, 5 1
LIS = 2, 4, 5
```

## Naive Algo:

```
for i = N; i > 0; i-- {
  find all subsequence of D with length i
  if there is one subsequence:
      break
}
```

Time complexity: O(2^N)

## Dynamic Programming Algorithm

subproblem: we define a vector L such that:
- L[i] = LIS of D that end with D[i]
- L[0] = {D[0]}

```
D = 3, 2, 6, 4, 5 1
L[0] = {3}
L[1] = {2}
L[2] = {2, 6}
L[3] = {2, 4}
L[4] = {2, 4, 5}
L[5] = {1}
```

General formula:
```
L[i] = MAX(L[i] | i<j, D[j] < D[i]) + D[i]
```

Time Complexity: O(n^2)
