
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
    # Pull configuration
    config = file_manager.load_json('config.json')
    global DEVICE_ID
    global SERVER_URL
    DEVICE_ID = config.get('device_id', get_mac())
    SERVER_URL = config.get('server_url', None)

    # Prep direction manager
    #  which determines if an object had gone from an entry point to exit or vice versa
    dm = direction_manager.DirectionManager(enter_detected, exit_detected)

    # Start the CV Detection
    #  The alwaysAI convenience class is only checking to see if target objects are
    #  in entry or exit zones, then passes this info to the direction manager
    #  to make determination on direction of travel
    alwaysai.start_detection(config, detection_began, dm.in_entry, dm.in_exit, dm.tracking_ended_for)

def detection_began():
    '''
    '''
    print('detector: app.py: detection_began:')

def enter_detected(object_id):
    '''
    Pass detection of object in an entry zone to the traffic manager
    '''
    print('detector: app.py: enter_detected: {}'.format(object_id))
    
    # traffic_manager.new_entry(object_id, time.time())
    # global SERVER_URL
    # global TIME_KEY
    # post.data(SERVER_URL+'/new_entry',
    #           {'object_id': object_id, TIME_KEY:time.time()})


def exit_detected(object_id):
    '''
    Pass detection of object in an exit zone to the traffic manager
    '''
    print('detector: app.py: exit_detected: {}'.format(object_id))
    # traffic_manager.new_exit(object_id, time.time())
    # global SERVER_URL
    # global TIME_KEY
    # post.data(SERVER_URL+'/new_exit',
    #   {'object_id': object_id, TIME_KEY: time.time()})

if __name__ == "__main__":
    main()
