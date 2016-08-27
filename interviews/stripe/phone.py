

# https://gist.github.com/ChimeraCoder/1906326162eb88742952
class Tracker(object):
    def __init__(self):
        self.pools = {}

    def allocate(self, hostname):
        if hostname not in self.pools:
            self.pools[hostname] = []

        pool = self.pools[hostname]
        next_server = next_server_number(pool)
        pool.append(next_server)
        return '{0}{1}'.format(hostname, next_server)

    def deallocate(self, hostname):
        select_i = 0
        for i, c in enumerate(hostname):
            if c.isdigit():
                select_i = i

        # invalid hostname with digits only?
        host = hostname[:select_i]
        server_number = int(hostname[select_i:]) # do we need to convert?

        if host in self.pools:
            new_pool = [i for i in self.pools[host] if server_number != i]
            self.pools[host] = new_pool

        return None


# https://gist.github.com/antifuchs/dd5344b60693dd1d073b
def next_server_number(servers):
    if len(servers) == 0:
        return 1

    max_value = max(servers)

    allocated_servers = {}
    for s in servers:
        allocated_servers[s] = 1

    for i in xrange(1, max_value):
        if i not in allocated_servers:
            return i

    return max_value + 1


if __name__ == '__main__':
    print next_server_number([5, 3, 1])
    print next_server_number([5, 4, 1, 2])
    print next_server_number([3, 2, 1])
    print next_server_number([2, 3])
    print next_server_number([])

    tracker = Tracker()
    print tracker.allocate("apibox")
    # "apibox1"
    print tracker.allocate("apibox")
    # "apibox2"
    print tracker.deallocate("apibox1")
    # None
    print tracker.allocate("apibox")
    # "apibox1"
    print tracker.allocate("sitebox")
    # "sitebox1"
