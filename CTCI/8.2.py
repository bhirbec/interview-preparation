
def main():
    matrix = [
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 1],
        [0, 0, 1, 0, 0, 0],
    ]
    print find_path(matrix)

def find_path(matrix):
    '''
    Time: O(n x m)
    '''
    n = len(matrix)
    if n == 0:
        return []

    m = len(matrix[0])
    if m == 0:
        return []

    visited = {}

    def dfs(i, j):
        if (i, j) in visited or i == n or j == m or matrix[i][j]:
            return []

        if i == n - 1 and j == m - 1 and matrix[i][j] == 0:
            return [(i, j)]

        path = dfs(i, j+1) or dfs(i+1, j)
        if path:
            path.append((i, j))

        visited[(i, j)] = 1
        return path

    return list(reversed(dfs(0, 0)))

main()
