# Text Justification

Sources:
- [YouTube - MIT OpenCourseWare](https://youtu.be/ENyox7kNKeY?list=PLfMspJ0TLR5HRFu2kLh3U4mvStMO8QURm)

## Definition 

Input is a text (list of words) and we want to split it into "good" lines (justified to the right). 

```
~~~~ ~~ ~~~~~~ |
~~ ~~~ ~~~ ~~~ |
~~      ~~~~~~ | We want to avoid bid gaps
```

We define a quantity that we call `badness(i,j)` as a the "badness" of using words[i:j] as a line.

```
When line doesn't fit:
badness(i, j) = +infinity 

Otherwise:
badness(i, j) = (page_width - total_width)^3 
```

Overall problem is to *minimize the sum of the badnesses of the lines*.

## Subproblems 

In the brut force approach we would try all the different splits. For every
words does it start a new line or not? If there are N words them there are
2^N different splits.

## Guess

Where does the second line begin? Try all words after the first one. After we find 
the first line then we're left with another problem of the same type. Where does 
the third line begin? Subproblems are suffixes words[i:] and the number of subproblems is 
n.

## Recurrence
```
DP(i) = Min( DP(j) + badness(i,j) for j in range(i+1, n+1) )

Base case:
DP(n) = 0
```
