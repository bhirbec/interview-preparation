

def recursive(graph):
    n = len(graph)
    cache = [None]*n

    def _f(i):
        if i < 0:
            return 0, []

        w = graph[i]
        if i == 0:
            return graph[i], [w]
        elif i in cache:
            return cache[i]

        S2, IS2 = _f(i-2)
        S1, IS1 = _f(i-1)
        S2 += w

        if S1 > S2:
            cache[i] = S1, IS1
        else:
            # TODO: remove list concat. It makes this algorithm O(n**2)
            cache[i] = S2, IS2 + [w]

        return cache[i]

    _, IS =  _f(n-1)
    return IS

def bottom_up(graph):
    n = len(graph)
    cache = [0]*n
    cache[0] = graph[0], [graph[0]]

    for i in range(1, n):
        w = graph[i]

        if i-2 < 0:
            S2, IS2 = 0, []
        else:
            S2, IS2 = cache[i-2]

        S1, IS1 = cache[i-1]
        S2 += w

        if S1 > S2:
            cache[i] = S1, IS1
        else:
            # TODO: remove list concat. It makes this algorithm O(n**2)
            cache[i] = S2, IS2 + [w]

    return cache[n-1][1]

if __name__ == '__main__':
    graph = [17, 14, 5, 4, 8, 12, 1, 34, 108, 22]
    print recursive(graph)
    print bottom_up(graph)
