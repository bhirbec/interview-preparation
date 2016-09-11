from Queue import Queue

def main():
    graph = {
        1: [2, 3],
        2: [4, 3],
        3: [],
        4: [1, 5],
        5: [2],
        6: [5]
    }

    print exists_path(graph, 1, 5)

def exists_path(graph, origin, dest):
    q = Queue()
    q.put(origin)
    visited = {}

    while not q.empty():
        n = q.get()
        if n in visited:
            continue

        if n == dest:
            return True

        for ni in graph[n]:
            q.put(ni)

        visited[n] = True

    return False

if __name__ == '__main__':
    main()
