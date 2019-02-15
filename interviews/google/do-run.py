# https://www.careercup.com/question?id=5701279419465728

# Given a list of words, and the number of rows and columns, return the number of words
# that can be fit into the rows and columns by stringing together each consecutive word. If the next word doesn't fit in the same line, it should move to the next line. Find an efficient solution for this. For eg.

# List of words: { "Do", "Run" }
# Number of columns: 9
# Number of rows: 2

# First row: "Do Run Do" (7 letters + 2 spaces fit into 9 columns)
# Second row: "Run Do" (Only 2 words fit into 9 columns)

# result: 5

def main():
    text = 'Please use this doc to code'
    max_words(text, 5, 20)

def max_words(text, nb_rows, nb_cols):
    words = text.split(' ')
    n = len(words)
    size = 0
    r = 0
    k = 0

    row = []
    rows = []

    while r < nb_rows:
        i = k % n
        w = words[i]
        w_length = len(w)

        if size + w_length <= nb_cols:
            row.append(w)
            size += w_length + 1
            k += 1
        else:
            rows.append(row)
            row = []
            size = 0
            r += 1

    for row in rows:
        print row

    print k // n


main()
