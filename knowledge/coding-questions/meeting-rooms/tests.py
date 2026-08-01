import unittest


class TestCanAttendMeetings(unittest.TestCase):
  def test_example_overlap(self):
    self.assertFalse(can_attend_meetings([[0, 30], [5, 10], [15, 20]]))

  def test_example_no_overlap(self):
    self.assertTrue(can_attend_meetings([[7, 10], [2, 4]]))

  def test_empty(self):
    self.assertTrue(can_attend_meetings([]))

  def test_single_meeting(self):
    self.assertTrue(can_attend_meetings([[3, 9]]))

  def test_back_to_back_is_fine(self):
    self.assertTrue(can_attend_meetings([[1, 5], [5, 8]]))

  def test_identical_meetings_overlap(self):
    self.assertFalse(can_attend_meetings([[2, 4], [2, 4]]))

  def test_contained_meeting_overlaps(self):
    self.assertFalse(can_attend_meetings([[1, 10], [3, 4]]))

  def test_overlap_only_in_later_pair(self):
    self.assertFalse(can_attend_meetings([[1, 2], [4, 6], [5, 7]]))

  def test_unsorted_non_overlapping(self):
    self.assertTrue(can_attend_meetings([[10, 12], [1, 3], [5, 7]]))

  def test_one_minute_overlap(self):
    self.assertFalse(can_attend_meetings([[1, 5], [4, 6]]))


if __name__ == '__main__':
  unittest.main()
