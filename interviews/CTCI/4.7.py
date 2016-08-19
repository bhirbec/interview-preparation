
def main():
    projects = 'a', 'b', 'c', 'd', 'e', 'f'
    dependencies = ('a', 'd'), ('f', 'b'), ('b', 'd'), ('f', 'a'), ('d', 'c')
    print build_order(projects, dependencies)

def build_order(projects, dependencies):
    adjacency_list = _build_adjacency_list(projects, dependencies)
    n = len(projects)
    order = [0] * n
    visited = {}
    visiting = {}

    # We don't use an int because it's not possible to mutate closure variables in Python 2
    # http://stackoverflow.com/questions/21959985/why-cant-python-increment-variable-in-closure
    class _nonlocal:
        index = n - 1

    def _dfs(p):
        if p in visiting:
            # we're currently visiting this node which means that we're in a cyble
            return False

        if p in visited:
            return True

        visiting[p] = True
        for p1 in adjacency_list[p]:
            if not _dfs(p1):
                return False

        visited[p] = visiting.pop(p)
        order[_nonlocal.index] = p
        _nonlocal.index -= 1
        return True

    for p in projects:
        if p not in visited:
            if not _dfs(p):
                return 'ERROR'

    return order

def _build_adjacency_list(projects, dependencies):
    adjacency_list = dict((p , []) for p in projects)
    for dep, p in dependencies:
        adjacency_list[dep].append(p)
    return adjacency_list


if __name__ == '__main__':
    main()
