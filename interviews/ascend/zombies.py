# You're given a 2D-array representing relationship between zombies.

#    Z0 Z1 Z2 Z3
# Z0  1  1  0  0
# Z1  1  1  1  0
# Z2  0  1  1  0
# Z3  0  0  0  1

# When two zombies are on the same line or column then it means that
# they belong to the same clan. In the above example there're two
# clans: {Z0, Z1, Z2} and {Z3}.

# Write a function that takes a 2d-array of zombies and returns the number of clans.

def main():
    zombies = ['1100', '1110', '0110', '0001']
    print zombie_clans(zombies)

    zombies = ['10000', '01000', '00100', '00010', '00001']
    print zombie_clans(zombies)

def zombie_clans(zombies):
    '''
    The zombies matrix represents a Graph with connection between zombies.
    To find the number of clusters we need to find the number of connected
    components in the graph.
    '''
    visited = {}
    counter = 0
    n = len(zombies)

    for i in xrange(n):
        for j in xrange(i, n):
            if (i, j) in visited:
                continue
            if zombies[i][j] == '1':
                dfs(i, j, n, zombies, visited)
                counter += 1

    return counter

def dfs(i, j, n, zombies, visited):
    if (i, j) in visited or zombies[i][j] == '0':
        return

    visited[(i, j)] = 1

    for k in xrange(n):
        # add zombies on the same line
        dfs(i, k, n, zombies, visited)
        # add zombies on the same column
        dfs(k, j, n, zombies, visited)

if __name__ == '__main__':
    main()
