

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
            IS2.append(w)
            cache[i] = S2, IS2

        return cache[i]

    _, IS =  _f(n-1)
    return IS

if __name__ == '__main__':
    graph = [17, 4, 5, 4, 8, 12, 7]
    print recursive(graph)
