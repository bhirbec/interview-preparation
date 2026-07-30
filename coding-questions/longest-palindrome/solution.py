from collections import Counter


def longest_palindrome(s):
  counts = Counter(s)
  half = []
  middle = ''

  for ch in sorted(counts):
    cnt = counts[ch]
    half.append(ch * (cnt // 2))
    if cnt % 2 == 1 and middle == '':
      middle = ch

  left = ''.join(half)
  return left + middle + left[::-1]
