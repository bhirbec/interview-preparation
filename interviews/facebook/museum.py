# https://www.careercup.com/question?id=5722862468988928

# A museum was represented by a square matrix that was filled with O, G, and W where O represented open
# space G represented guards, and W represented walls. Write a function that accepts the square matrix
# and returns another square matrix where all of the O's in the matrix are replaced with the number of
# how many spaces they are away from a guard, without being able to go through any walls.

import heapq


def main():
    matrix = [
        ['O', 'W', 'G', 'O', 'O', 'O', 'O', 'O', 'W', 'G'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'W', 'W'],
        ['O', 'O', 'G', 'O', 'O', 'O', 'O', 'O', 'O', 'W'],
        ['O', 'W', 'O', 'O', 'W', 'O', 'O', 'O', 'O', 'O'],
        ['G', 'W', 'O', 'W', 'O', 'O', 'O', 'W', 'O', 'O'],
        ['O', 'W', 'O', 'W', 'O', 'O', 'O', 'G', 'O', 'O'],
        ['O', 'W', 'O', 'W', 'O', 'O', 'O', 'W', 'O', 'O'],
        ['O', 'W', 'O', 'W', 'O', 'O', 'O', 'W', 'O', 'O'],
        ['O', 'W', 'O', 'W', 'O', 'O', 'O', 'W', 'O', 'O'],
        ['O', 'W', 'O', 'W', 'G', 'O', 'O', 'O', 'O', 'O'],
    ]

    for row in museum(matrix):
        print ' '.join(str(i) for i in row)


def museum(matrix):
    '''
    Time: O(n^2)
    Space: O(n^2)
    '''
    dest = list(matrix)

    h = []
    for i, j in _find_guards(matrix):
        heapq.heappush(h, (0, i, j))

    n = len(matrix)
    visited = {}

    while len(h) > 0:
        d, i, j = heapq.heappop(h)
        if not _is_valid_coordinate(i, j, n) or dest[i][j] == 'W' or (i, j) in visited:
            continue

        heapq.heappush(h, (d+1, i-1, j-1))
        heapq.heappush(h, (d+1, i-1, j))
        heapq.heappush(h, (d+1, i-1, j+1))
        heapq.heappush(h, (d+1, i, j-1))
        heapq.heappush(h, (d+1, i, j+1))
        heapq.heappush(h, (d+1, i+1, j-1))
        heapq.heappush(h, (d+1, i+1, j))
        heapq.heappush(h, (d+1, i+1, j+1))

        if dest[i][j] == 'O':
            dest[i][j] = d

        visited[(i, j)] = 1

    return dest


def _find_guards(matrix):
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            if val == 'G':
                yield i, j

def _is_valid_coordinate(x, y, n):
    return 0 <= x < n and 0 <= y < n

if __name__ == '__main__':
    main()
