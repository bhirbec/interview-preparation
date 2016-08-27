# your given a 2d-map with:
# - mountains = #
# - mining Sites = *
# - open spaces = ' '

# A rover can move left, right, top, bottom and cannot go on the mountains.
# Find the best location for a base that minimizes the distance to reach
# all mining sites.

############
#    *#    #
#     #    #
#          #
##         #
#  *#  ##  #
#   #  #  *#
############

from Queue import Queue

def main():
    array = [
        ['#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', '*', ' ', '#', ' ', ' ', ' ', '#'],
        ['#', ' ', ' ', '#', ' ', ' ', ' ', '#'],
        ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
        ['#', '#', '#', '#', '#', '#', ' ', '#'],
        ['#', '*', ' ', ' ', ' ', ' ', ' ', '#'],
        ['#', ' ', ' ', '*', ' ', ' ', '*', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#'],
    ]

    result = base(array)
    if not result:
        print 'The base cannot be setup'
        return

    x, y = result
    array[x][y] = 'B'
    _print_map(array)

def base(array):
    mining_sites = list(_iter_mining_sites(array))
    k = len(mining_sites)

    # no mining sites
    if k == 0:
        return None

    destination = [ [(0 if v == ' ' else v) for v in row] for row in array]
    for x, y in mining_sites:
        m = _bfs(x, y, destination)

        # if we're not able to reach all the mining sites then we return None
        if m < k:
            return None

    return _find_min_distance(destination)

def _bfs(x, y, destination):
    n = len(destination)
    q = Queue()
    q.put((0, x, y))
    visited = {}
    m = 0

    while not q.empty():
        d, i, j = q.get()
        if (i, j) in visited or not _is_valid_coordinate(i, j, n) or destination[i][j] == '#':
            continue

        q.put((d+1, i-1, j-1))
        q.put((d+1, i-1, j))
        q.put((d+1, i-1, j+1))
        q.put((d+1, i, j-1))
        q.put((d+1, i, j+1))
        q.put((d+1, i+1, j-1))
        q.put((d+1, i+1, j))
        q.put((d+1, i+1, j+1))
        visited[(i, j)] = 1

        if destination[i][j] == '*':
            m += 1
        else:
            destination[i][j] += d

    return m

def _is_valid_coordinate(i, j, n):
    return (0 <= i < n) and (0 <= j < n)

def _iter_mining_sites(array):
    for x, row in enumerate(array):
        for y, v in enumerate(row):
            if v == '*':
                yield x, y

def _find_min_distance(destination):
    m, x, y = None, None, None
    for i, row in enumerate(destination):
        for j, v in enumerate(row):
            if m is None or v < m :
                m, x, y = v, i, j
    return x, y

def _print_map(array):
    for row in array:
        print ' '.join('{:>2}'.format(v) for v in row)

main()
