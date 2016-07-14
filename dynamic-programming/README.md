# Dynamic Programming 006

https://www.youtube.com/watch?v=OQ5jsbhAv_M

# Introduction
- General, powerful algorithm design technique
- DP good for optimization problems
- DP ~ "Carreful Brut force"
- DP ~ "break problem into subproblems, solve subproblems, and reuse solutions"
- DP ~ "shortest path in some DAG"
- Invented by Richard Bellman (same Bellman-Ford)

5 "easy" steps to DP:
- define subproblems
- guess something
- reuse subproblem with recurence
- build an algorithm recurse + memoization or bottom-up + table
- solve the original problem

# 2. Shortest Paths

Guessing: don't know this answer? Then guess! Try them all guesses and take the best.

```
  						  \ |
s --> s' --> ... --> u -->  v
						  / |
```

Guess the last edge incoming to v:
```
dist(s, v) = dist(s, u) + weight(u, v)
```

Guess all the possible edges and take the best:
```
dist(s, v) = Min(dist(s, u) + weight(u, v)) for any (u, v)
dist(s, u) is a subproblem => recursive calls
```

# 4. Text Justification

https://youtu.be/ENyox7kNKeY?list=PLfMspJ0TLR5HRFu2kLh3U4mvStMO8QURm

Input is a text (list of words) and we want to split it into "good" lines (justified 
to the right). 

```
~~~~ ~~ ~~~~~~ |
~~ ~~~ ~~~ ~~~ |
~~      ~~~~~~ | We want to avoid bid gaps
```

We define a quantity that we call `badness(i,j)` as a the "badness" of 
using words[i:j] as a line.

```
When line doesn't fit:
badness(i, j) = +infinity 

Otherwise:
badness(i, j) = (page_width - total_width)^3 
```

Overall problem is:
*Minimize sum of badnesses of the lines*

**Subproblems:**

In the brut force approach we would try all the different splits. For every
words does it start a new line or not? If there are N words them there are
2^N different splits.

**Guess:**

Where does the second line begin? Try all words after the first one. After we find 
the first line then we're left with another problem of the same type. Where does 
the third line begin? Subproblems are suffixes words[i:] and the number of subproblems is 
n.

**Recurrence:**
```
DP(i) = Min( DP(j) + badness(i,j) for j in range(i+1, n+1) )

Base case:
DP(n) = 0
```

# 5. Blackjack
https://youtu.be/ENyox7kNKeY?list=PLfMspJ0TLR5HRFu2kLh3U4mvStMO8QURm&t=2333

# 6. Subproblems for strings/sequences
- suffixes x[i:] => Theta(n)
- prefixes x[:i] => Theta(n)
- substrings x[i:j] with i <= j => => Theta(n^2)

# 7. Parenthesization
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

Topoligical order:
