Parenthesization

https://youtu.be/ocZMDMZwhCY?t=360

Optimal evaluation of associative expression like matrix multiplication:

```
(A0 * A1) * A2
A0 * (A1 * A2)
```

Guess: what the last/outermost multiplication?
`(A0...Ak-1).(Ak...An-1)`

Then we recurse:
`(A0...Ak'-1).(Ak'...Ak)` and we find that `(Ak'...Ak)` is a substring

Subproblem: 
Optimal evaluation of `(Ai...Ak-1).(Ak...Aj-1) i:j`

Number of choices:
`O(j-i+1) = O(n)`

Recurrence:
```
DP(i,j) = Min( DP(i,k) + DP(k,j) + Cost of product (Ai...Ak-1).(Ak...Aj)  for k range(i+1, j))
with DP(i,k) = cost of the left product
with DP(k,j) = cost of the right product
```
Running time:
Time/subproblem = O(n)
Number of subproblems = O(n^2)
Time => O(n^3)
