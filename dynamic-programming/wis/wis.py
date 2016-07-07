
def recursive(graph):
    n = len(graph)
    cache = [None]*(n+1)
    cache[0], cache[1] = 0, graph[0]

    def _f(i):
        if cache[i] is None:
            w = graph[i-1]
            S2 = _f(i-2) + w
            S1 = _f(i-1)
            cache[i] = S1 if S1 > S2 else S2
        return cache[i]

    _f(n)
    return _reconstruct_solution(n, cache)

def bottom_up(graph):
    n = len(graph)
    cache = [0]*(n+1)
    cache[0], cache[1] = 0, graph[0]

    for i in range(1, n+1):
        w = graph[i-1]
        S2 = cache[i-2] + w
        S1 = cache[i-1]
        cache[i] = S1 if S1 > S2 else S2

    return _reconstruct_solution(n, cache)

def _reconstruct_solution(n, cache):
    i = n
    output = []
    while i >= 0:
        if cache[i] > cache[i-1]:
            output.append(graph[i-1])
            i -= 2
        else:
            i -= 1

    output.reverse()
    return output

if __name__ == '__main__':
    graph = [17, 14, 5, 4, 82, 12, 1, 34, 1080, 222]
    print recursive(graph)
    print bottom_up(graph)
