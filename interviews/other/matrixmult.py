
def main():
    B = [
        [1, 1, 2],
        [1, 1, 6]
    ]

    A = [
        [1, 1],
        [1, 1],
        [1, 6]
    ]

    C = matrix_mult(A, B)
    print '\n'.join(str(r) for r in  C) + '\n'

class UncompatibleSizeError(Exception):
    pass

def matrix_mult(A, B):
    r1, c1 = len(A), len(A[0])
    r2, c2 = len(B), len(B[0])

    if c1 == r2:
        return _mult(A, B, r1, c2, c1)

    raise UncompatibleSizeError("Matrices must be the compatible in size to be multiplied")

def _mult(A, B, r, c, n):
    output = [ [0 for j in xrange(c)] for i in xrange(r) ]

    for i in xrange(r):
        for j in xrange(c):
            output[i][j] = sum(A[i][k] * B[k][j] for k in xrange(n))

    return output

main()
