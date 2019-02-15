# Enter your code here. Read input from STDIN. Print output to STDOUT

# //========================
# // Grid (Upper case english letters)
# //========================
# // A R I D S
# // W E R O D
# // U E F B E
# // B E R E E

# //========================
# // Word
# //========================
# // "UBER"

# //========================
# // Rules to find a word in the grid:
# //========================
# // 1. Move one step at a time
# // 2. Move horizontally or vertically only
# // 3. Start from any position
# // 4. Cannot revisit position

# //========================
# // Question
# //========================
# // Given a letter grid and a word, return true if it can be found in the grid, false otherwise




from queue import Queue


def search_word(mat, word)
    x, y = 2, 0
    i = 0
    m = len(word)
    n = len(mat)

    def _dfs(i, x, y):
        if x > n-1 or y > n-1:
            return False

        expected_letter = word[i]
        current_letter = mat[x][y]
        if expected_letter != current_letter:
            return False

        if i < m:
            return (
                _dfs(i+1, x, y+1)
                or _dfs(i+1, x+1, y)
                or _dfs(i+1, x, y-1)
                or _dfs(i+1, x-1, y)
            )
        else:
            return False

    return _dfs(i, x, y)


def search_word(mat, word):
    q = Queue()
    q.put((0, 0))
    n = len(mat)
    visited = {}

    while not q.empty():
        i, j = q.get()

        if visited[(i, j)]:
            continue

        letter = arr[i][j]
        idx = word.find(letter)
        if idx == -1:
            continue

        # XXX
        if i == n - 1:
            q.put((i, j+1))

        elif j == n - 1:
            q.put((i+1, j))

        q.put((i+1, j))
        q.put((i, j+1))
        q.put((i-1, j))
        q.put((i, j-11))

