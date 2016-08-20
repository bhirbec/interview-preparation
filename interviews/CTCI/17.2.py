import random


def main():
    print shuffle(52)

def shuffle(n):
    if n == 0:
        return []

    # shuffle n-1
    result = shuffle(n-1)
    # pick a pos between 0 and n-1
    i = int(random.uniform(0, n))
    # append the nth number
    result.append(n)
    # swap nth with ith
    result[i], result[n-1] = result[n-1], result[i]
    return result

if __name__ == '__main__':
    main()
