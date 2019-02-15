# Given an array of numbers and a total, find a mathematical expression
# that combines numbers from the array, + and - signs, and produces the total.

# Example:
# arr = [1, 2, 3, 4]
# total = 46
# output = 12 + 34


def find_expr(arr, total):
    def _f(i, j):
        if i >= j:
            return

        value = int(''.join(str(v) for v in arr[i:j+1]))
        print(value)

        # if value == total:
        #     print(value)

        mid = int((i+j) / 2)
        print(mid, i, j)
        for k in range(i, j):
            _f(i, k)
            _f(k, j)

    _f(0, len(arr)-1)


find_expr([1, 2, 3, 4], total=1234)
