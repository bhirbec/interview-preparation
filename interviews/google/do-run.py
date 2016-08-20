# https://www.careercup.com/question?id=5701279419465728

# GIven a list of words, and the number of rows and columns, return the number of words
# that can be fit into the rows and columns by stringing together each consecutive word. If the next word doesn't fit in the same line, it should move to the next line. Find an efficient solution for this. For eg.

# List of words: { "Do", "Run" }
# Number of columns: 9
# Number of rows: 2

# First row: "Do Run Do" (7 letters + 2 spaces fit into 9 columns)
# Second row: "Run Do" (Only 2 words fit into 9 columns)

# result: 5

def main():
    words = ['Do', 'Run']
    max_words(words, 2, 9)

def max_words(words, nb_rows, nb_cols):
    n = len(words)

    def f(i, r):
        if r > 1:
            return 0

        size = 0
        current_words = []
        max_words_count = 0

        while 1:
            w = words[i]
            size += len(w) + max(len(current_words) - 1, 0)

            if size < nb_cols:
                current_words.append(w)
                i = (i + 1) % n
                print r, current_words
                words_count = f(i, r+1) + len(current_words)
                if words_count > max_words_count:
                    max_words_count = words_count
            else:
                break

        return max_words_count

    print f(0, 0)


main()
