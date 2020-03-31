
import file_manager
import alwaysai
import os

from dotenv import load_dotenv
load_dotenv(verbose=True)

def main():
    # server_token = os.getenv("SERVER_TOKEN")
    config = file_manager.load_json('config.json')

    # 2. Start the CV Detection
    alwaysai.start_detection(config, detection_began, object_detected, object_lost)

def detection_began():
    '''
    '''
    print('app.py: detection_began:')

def object_tracked(object_id, label, center):
    '''
    '''
    print('app.py: object_tracked: object_id: {} center: {}'.format(object_id, center))

def object_lost(object_id, label, center):
    '''
    '''
    print('app.py: object_lost: {}: center: {}'.format(object_id, center))

# TODO: What's the best way to track when an object is lost

if __name__ == "__main__":
    main()
