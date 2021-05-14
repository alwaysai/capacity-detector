import requests

'''
Handles delivery of data to specified endpoint
'''

SHOULD_LOG = True
TIME_KEY = 'timestamp'


def data(url, payload):
    """Send just tracking meta data to target endpoint"""
    global SHOULD_LOG
    return _send(url=url, json=payload, files=None, should_log=SHOULD_LOG)


def _send(url, json=None, files=None, should_log=False):
    """Construct a post request and deliver"""
    try:
        r = requests.post(url=url, json=json)
        if r.status_code != 200:
            if should_log:
                print(
                    'post.py: _send: non-200 status code returned: {}:{}'.format(r.status_code, r.text))
            return r
        if should_log:
            print('post.py: _send: response: {}'.format(r))
        return r
    except requests.exceptions.ConnectionError:
        if should_log:
            print('post.py: _send: connection error')
        return 'Connection refused'
    except Exception as err:
        exception_type = type(err).__name__
        if should_log:
            print('post.py: _send: unknown error: {}'.format(exception_type))
        return 'Unknown post request error'
