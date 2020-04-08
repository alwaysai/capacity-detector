
import file_manager
import alwaysai
import direction_manager
import os
import post
import time
from uuid import getnode as get_mac

SERVER_URL = None
TIME_KEY = 'timestamp'
DEVICE_ID = None

def main():
    # server_token = os.getenv("SERVER_TOKEN")
    config = file_manager.load_json('config.json')
    global DEVICE_ID
    global SERVER_URL
    DEVICE_ID = config.get('device_id', get_mac())
    SERVER_URL = config.get('server_url', None)

    # TODO: Load Traffic Manager from last run
    dm = direction_manager.DirectionManager(enter_detected, exit_detected)

    # 2. Start the CV Detection
    alwaysai.start_detection(config, detection_began, dm.in_entry, dm.in_exit)


def detection_began():
    '''
    '''
    print('detector: app.py: detection_began:')


def enter_detected(object_id):
    print('detector: app.py: enter_detected: {}'.format(object_id))
    global SERVER_URL
    global TIME_KEY
    post.data(SERVER_URL+'/new_entry',
              {'object_id': object_id, TIME_KEY:time.time()})


def exit_detected(object_id):
    print('detector: app.py: exit_detected: {}'.format(object_id))
    global SERVER_URL
    global TIME_KEY
    post.data(SERVER_URL+'/new_exit',
              {'object_id': object_id, TIME_KEY:time.time()})


if __name__ == "__main__":
    main()
