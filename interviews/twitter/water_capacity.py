
def sum_water_1(arr):
    n = len(arr)
    x, m = _find_max(arr, 0, n-1)
    return left_problem(arr, 0, x-1, m) + right_problem(arr, x+1, n-1, m)

def left_problem(arr, start, end, m):
    if end <= start:
        return 0

    x, new_m = _find_max(arr, start, end)
    return left_problem(arr, start, x-1, new_m) + compute_water_level(arr, x+1, end, min(m, new_m))

def right_problem(arr, start, end, m):
    if end <= start:
        return 0

    x, new_m = _find_max(arr, start, end)
    return right_problem(arr, start, x-1, new_m) + compute_water_level(arr, start, x-1, min(m, new_m))

def compute_water_level(arr, start, end, m):
    s = 0
    for i in xrange(start, end+1):
        s += m - arr[i]
    return s

def _find_max(arr, start, end):
    m = 0
    x = start
    for i in range(start, end+1):
        if arr[i] >= m:
            m = arr[i]
            x = i
    return x, m


main()
