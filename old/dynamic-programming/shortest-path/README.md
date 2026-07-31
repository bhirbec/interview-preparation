# Shortest Paths

https://youtu.be/OQ5jsbhAv_M?t=1879

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
