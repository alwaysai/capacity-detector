
from uuid import getnode as get_mac
import os
import post

DEVICE_KEY = 'device_id'
TIME_KEY = 'timestamp'
ENTRY_KEY = 'server_entry_url'
EXIT_KEY = 'server_exit_url'

class Server:
    def __init__(self, config):
        did = config.get(DEVICE_KEY, get_mac())
        enurl = config.get(ENTRY_KEY, None)
        exurl = config.get(EXIT_KEY, None)
        self.device_id = did
        self.entry_url = enurl
        self.exit_url = exurl

    def track_entry(self, timestamp):
        print('comm.py: track_entry: {}'.format(timestamp))
        post.data(self.entry_url,
            {DEVICE_KEY: self.device_id, TIME_KEY:timestamp})

    def track_exit(self, timestamp):
        print('comm.py: track_exit: {}'.format(timestamp))
        post.data(self.exit_url,
            {DEVICE_KEY: self.device_id, TIME_KEY:timestamp})