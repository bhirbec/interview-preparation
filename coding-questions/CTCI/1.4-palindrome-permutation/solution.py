def check_perm_of_palindrome(s):
  s = s.lower().replace(' ', '')

  chars = {}
  for c in s:
    chars[c] = chars.setdefault(c, 0) + 1

  found_odd = False
  for counter in chars.values():
    if is_even(counter):
      continue

    if not found_odd:
      found_odd = True
    else:
      return False

  return True


def is_even(i):
  return (i & 1) == 0
