
def main():
    n = 134859
    print count_twos(n)
    print brut_force(n)

def count_twos(n):
    digits = [int(d) for d in str(n)]
    nb_digits = len(digits)

    A = [0] * (nb_digits + 1)
    for i in range(1, nb_digits+1):
        A[i] = A[i-1] * 10 + 10**(i-1)

    s = 0
    for i in xrange(nb_digits):
        digit = digits[nb_digits - i - 1]
        if digit >= 2:
            base = 10 ** i
            s += base
        s += A[i] * digit

    return s

def brut_force(n):
    s = 0
    for i in range(1, n+1):
        for c in str(i):
            if c == '2':
                s += 1
    return s

if __name__ == '__main__':
    main()

