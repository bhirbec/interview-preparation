GRID_SIZE = 8

def place_queens(row, columns, result):
    if row == GRID_SIZE:
        result.append(list(columns))
    else:
        for col in xrange(GRID_SIZE):
            if check_valid(columns, row, col):
                columns[row] = col
                place_queens(row+1, columns, result)

def check_valid(columns, row, col):
    for r in xrange(row):
        c  = columns[r]

        if c == col:
            return False

        row_distance = row - r
        column_distance = abs(c - col)
        if column_distance == row_distance:
            return False

    return True

def main():
    result = []
    columns = [0 for i in xrange(GRID_SIZE)]
    place_queens(0, columns, result)
    for r in result:
        print r

main()
