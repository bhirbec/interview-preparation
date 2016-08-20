# https://www.careercup.com/question?id=20308668

# A string consists of '0', '1' and '?'. The question mark can be either '0' or '1'.
# Find all possible combinations for a string.

def find_combinations(s):
    output = []
    chars = [c for c in s]
    combine(chars, 0, len(s), output)
    return output

def combine(chars, pos, n, output):
    if pos == n:
        output.append(''.join(chars))
    elif chars[pos] == '?':
        chars[pos] = '0'
        combine(chars, pos+1, n, output)
        chars[pos] = '1'
        combine(chars, pos+1, n, output)
        chars[pos] = '?'
    else:
        combine(chars, pos+1, n, output)

combinations = find_combinations('10??1??01???')
print '\n'.join(combinations)
