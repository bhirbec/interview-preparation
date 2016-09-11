
def main():
    array = [-1, 1, 3, 5, 7]
    print magix_index_distinct_array(array)

    array = [-1, 0, 3, 5, 7]
    print magix_index_distinct_array(array)

def magix_index_distinct_array(array):
    '''
    Time: O(log(n))
    space: O(log(n))
    '''
    n = len(array)

    def _f(i, j):
        if j < i:
            return -1

        index = int((i + j) / 2)
        if array[index] == index:
            return index
        elif array[index] > index:
            return _f(i, index-1)
        else:
            return _f(index+1, j)

    return _f(0, n-1)

main()
