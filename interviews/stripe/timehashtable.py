import time

class TimeHashTable(object):
	def __init__(self):
		self._storage = {}

	def set(self, key, value):
		l = self._storage.get(key)
		if l is None:
			self._storage[key] = l = []

		ts = time.time()
		l.append( (ts, value) )
		return ts

	def get(self, key, ts=None):
		target_ts = ts or time.time()
		l = self._storage.get(key, [])
		select_i = None

		for i, (ts, value) in enumerate(l):
			if ts == target_ts:
				return value
			elif ts > target_ts:
				select_i = i - 1
				break

		if len(l) == 0 or select_i <= 0:
			return None
		elif select_i is None:
				return l[-1][1]
		else:
		 	return l[select_i][1]

def main():
	h = TimeHashTable()
	t0 = h.set('a', 1)
	t1 = h.set('a', 4)
	# t2 = h.set('a', 8)
	print t0, t1
	print h.get('a', t0-10)

main()
