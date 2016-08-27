# https://careercup.com/question?id=5726440612954112

def main():
    print sum_to_x([1, 5, 10, 3], 18)

def sum_to_x(arr, target):
    '''
    Time: O(n)
    Space: O(1)
    '''
    start, end, s = 0, 0, 0
    while end < len(arr):
        if s + arr[end] == target:
            return start, end
        elif s + arr[end] <= target:
            s += arr[end]
            end += 1
        else:
            s -= arr[start]
            start += 1

    return None

main()
