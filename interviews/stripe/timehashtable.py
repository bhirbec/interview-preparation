

class TimeHashTable(object):
    def __init__(self, start_ts=0):
        self._ts = start_ts
        self._storage = {}

    def set(self, key, value):
        l = self._storage.get(key)
        if l is None:
            self._storage[key] = l = []

        l.append( (self._ts, value) )
        self._ts += 1

    def get(self, key, ts=None):
        l = self._storage.get(key, [])
        if len(l) == 0:
            return None

        target_ts = self._ts if ts is None else ts
        prev_value = None

        for ts, value in l:
            if ts == target_ts:
                return value
            elif ts > target_ts:
                return prev_value
            prev_value = value

        return l[-1][1]

def main():
    h = TimeHashTable()
    print h.get('a') is None

    h = TimeHashTable(10)
    h.set('a', 1)
    print h.get('a') == 1

    h.set('a', 123)
    print h.get('a', 10) == 1
    print h.get('a') == 123
    print h.get('a', 32) == 123
    print h.get('a', 2) is None

main()
