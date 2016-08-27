 import json
import requests
from urlparse import parse_qs


def simple():
    host = 'https://api.stripe.com'
    path = 'requestlog-simple.json'

    with open(path, 'rb') as f:
        reqs = json.loads(f.read())

    for req in reqs:
        print 'Testing URL: %s ...' % req['request']['url']

        r = requests.request(
            method  = req['request']['method'],
            url     = host + req['request']['url'],
            headers = req['request']['headers'],
            data    = req['request']['body']
        )

        print r.status_code, req['response']['code']

        if r.status_code != req['response']['code']:
            print 'Failed: %s' % req['request']['url']

def intermediate():
    host = 'https://api.stripe.com'
    path = 'requestlog-intermediate.json'

    with open(path, 'rb') as f:
        reqs = json.loads(f.read())

    req_suites = [
        [({}, reqs[0]), ({'id': 'customer'}, reqs[2])],
        [({}, reqs[1])],
    ]

    for suites in req_suites:
        result = None
        for param_map, req in suites:
            print '\n\nTesting URL: %s ...' % req['request']['url']

            qs = parse_qs(req['request']['body'])
            for k1, k2 in param_map.iteritems():
                value = result.get(k1)
                if value is not None:
                    qs[k2] = value

            r = requests.request(
                method  = req['request']['method'],
                url     = host + req['request']['url'],
                headers = req['request']['headers'],
                data    = qs
            )

            print r.status_code, req['response']['code']

            if r.status_code != req['response']['code']:
                print 'Failed: %s' % req['request']['url']

            result = r.json()


if __name__ == '__main__':
    intermediate()
