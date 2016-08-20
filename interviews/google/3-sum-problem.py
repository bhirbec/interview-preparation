# Google interview found on Glassdoor
# https://www.glassdoor.com/Interview/3-sum-problem-that-can-be-found-on-leetcode-QTN_1202200.htm

# solution descrive here:
# http://www.programcreek.com/2012/12/leetcode-3sum/

# from https://en.wikipedia.org/wiki/3SUM
# Suppose the input array is S[0..n-1]. 3SUM can be solved in O(n^2) time on average by
# inserting each number S[i] into a hash table, and then for each index i and j, checking
# whether the hash table contains the integer -(S[i]+S[j]).


def main():
    array = [-1, 0, 1, 2, -1, -4]
    triplets = three_sum(array, 0)
    for t in triplets:
        print t

def three_sum(array, sum):
    array.sort()

    positions = {}
    for i, v in enumerate(array):
        indexes = positions.setdefault(v, [])
        indexes.append(i)

    # the solution on programcreek.com doesn't use a set...
    triplets = set([])
    n = len(array)

    for i in xrange(n-3):
        for j in xrange(i+1, n-2):
            s = array[i] + array[j]
            reminder = sum - s
            indexes = positions.get(reminder, [])

            for k in indexes:
                if k > j:
                    triplet = array[i], array[j], array[k]
                    triplets.add(triplet)
                    break

    return list(triplets)

main()
