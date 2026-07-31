# Array Essentials

Arrays are the bread and butter of coding interviews. Before any clever
technique, most problems yield to a **single deliberate pass**: walk the array
once while maintaining just enough state to answer the question.

## The single-pass mindset

Ask: *what running state do I need as I scan?* A best-so-far, a running total, a
count, the previous element. If you can name it, you can usually solve the
problem in O(n) with O(1) extra space.

```python
# Best pair of adjacent elements — track only what the next step needs
best = arr[0] * arr[1]
for i in range(1, len(arr) - 1):
    best = max(best, arr[i] * arr[i + 1])
```

## Prefix and suffix passes

When position `i` needs to know about *everything before and after it*, do two
passes: accumulate from the left, then from the right.

```python
# product of all elements except self — no division
n = len(nums)
res = [1] * n
left = 1
for i in range(n):
    res[i] = left
    left *= nums[i]
right = 1
for i in range(n - 1, -1, -1):
    res[i] *= right
    right *= nums[i]
```

## The essentials

Mind the edges: empty input, single element, all-equal values. Off-by-one
errors live at the loop bounds — decide up front whether an index means "item
i" or "boundary between i-1 and i". When a formula exists (min/max, arithmetic
sums), prefer it over simulation.
