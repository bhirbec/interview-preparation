import unittest


def _normalize(words):
  # Group words by anagram key and sort both the groups and their contents so
  # two groupings can be compared regardless of ordering.
  groups = {}
  for w in words:
    groups.setdefault(''.join(sorted(w)), []).append(w)
  return sorted(sorted(g) for g in groups.values())


class TestGroupAnagrams(unittest.TestCase):
  def assert_same_grouping(self, arr, result):
    # Same multiset of words, and anagrams are grouped the same way.
    self.assertEqual(sorted(arr), sorted(result))
    self.assertEqual(_normalize(arr), _normalize(result))

  def _assert_anagrams_contiguous(self, result):
    seen_keys = []
    last_key = None
    for w in result:
      key = ''.join(sorted(w))
      if key != last_key:
        self.assertNotIn(key, seen_keys, msg=f'group {key} is split')
        seen_keys.append(key)
        last_key = key

  def test_canonical(self):
    arr = ['add', 'kii', 'dad', 'iki']
    result = group_anagrams(arr)
    self.assert_same_grouping(arr, result)
    self._assert_anagrams_contiguous(result)

  def test_empty(self):
    self.assertEqual(group_anagrams([]), [])

  def test_single(self):
    self.assertEqual(group_anagrams(['abc']), ['abc'])

  def test_no_anagrams(self):
    arr = ['abc', 'def', 'ghi']
    result = group_anagrams(arr)
    self.assert_same_grouping(arr, result)

  def test_all_anagrams(self):
    arr = ['abc', 'bca', 'cab', 'acb']
    result = group_anagrams(arr)
    self.assert_same_grouping(arr, result)
    self._assert_anagrams_contiguous(result)

  def test_mixed_groups_stay_contiguous(self):
    arr = ['listen', 'silent', 'enlist', 'google', 'gooown', 'cat', 'act']
    result = group_anagrams(arr)
    self.assert_same_grouping(arr, result)
    self._assert_anagrams_contiguous(result)

  def test_duplicates_preserved(self):
    arr = ['ab', 'ba', 'ab']
    result = group_anagrams(arr)
    self.assert_same_grouping(arr, result)


if __name__ == '__main__':
  unittest.main()
