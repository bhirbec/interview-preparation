# Given an RxC matrix of distinct numbers from 1 to R*C, print the "best" path from the top
# left corner to the bottom right corner. A path is a sequence of numbers in the matrix where
# each number is down or right from the previous number. To determine if a path A is better
# than a path B, sort the numbers in each path and pick the smallest lexicographically
# (ie, [1,3,4,5,7] < [1,4,5,6,7]).

#|R|,|C| < 5000

# Example:
# 4 5 9
# 8 1 3
# 2 6 7

# The best path is: 4, 5, 1, 3, 7

# --------------------------------------------------------------------------

# Hight level approach in O(R*C):
# - We precompute the position of each number in O(R*C) in an array of size R*C+1
# - then we iterate through the numbers from 1 through R*C,
#   - if the number is available then we select it. Then we mark the top-right and bottom-left of
#     the matrix as unavailable (without double marking)
#   - otherwise continue to the next numner

# .....xxxxxxxx
# .....xxxxxxxx
# .....xxxxxxxx
# ....1.....yyy
# xxxx......yyy
# xxxx.....2...
# xxxxyyyyy....
# xxxxyyyyy....

# - we can store the location of the selected numners in the previous stop. To get the final
#   path we sort the locations and retrieve the corresponding numbers. Alternatively, we can
#   scan the matrix again, and record the numbers that survived, which we return as a vector.

def main():
    matrix = [
        [7,  4,  6,  10],
        [8,  1,  9,  11],
        [3,  5,  2,  13],
        [14, 15, 16, 12],
    ]

    R = len(matrix)
    C = len(matrix[0])
    path = find_best_path(matrix, R, C)
    print path

def find_best_path(matrix, R, C):
    locations = [0]*(R*C+1)
    for i in xrange(R):
        for j in xrange(C):
            number = matrix[i][j]
            locations[number] = (i,j)

    positions = []
    for number in xrange(1, R*C+1):
        i, j = locations[number]

        if matrix[i][j] == 0:
            continue

        positions.append((i, j))
        mark_top_right(matrix, i, j, C)
        mark_bottom_left(matrix, i, j, R)

    positions.sort()
    return [matrix[i][j] for i, j in positions]

def mark_top_right(matrix, i, j, C):
    for row in xrange(i-1, -1, -1):
        for col in xrange(j+1, C):
            if matrix[row][col] == 0:
                return
            matrix[row][col] = 0

def mark_bottom_left(matrix, i, j, R):
    for row in xrange(i+1, R):
        for col in xrange(j-1, -1, -1):
            if matrix[row][col] == 0:
                return
            matrix[row][col] = 0

if __name__ == '__main__':
    main()
