# Notes:
# I really struggled on this one and didn't think about a recursive algorithm. I
# had to read the solution to understand that we could express the problem as
# subproblems of smaller size.

# Time: O(2^n) (drawing the tree of subproblems helped)
# Space: O(log(n))

def main():
    n = 5
    origin = range(1, n+1)
    buff = []
    dest = []
    move_disks(n, origin, buff, dest)
    print dest

def move_disks(n, origin, buff, dest):
    if n == 1:
        move_top(origin, dest)
        return

    move_disks(n-1, origin, dest, buff)
    move_top(origin, dest)
    move_disks(n-1, buff, origin, dest)

def move_top(origin, dest):
    dest.append(origin.pop())

main()
