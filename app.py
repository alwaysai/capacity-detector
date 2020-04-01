
import file_manager
import alwaysai
import os

def main():
    # server_token = os.getenv("SERVER_TOKEN")
    config = file_manager.load_json('config.json')

    # 2. Start the CV Detection
    alwaysai.start_detection(config, detection_began, object_detected, objects_lost)

def detection_began():
    '''
    '''
    print('app.py: detection_began:')

def object_detected(object_id, label, center):
    '''
    '''
    print('app.py: object_detected: label: {}: object_id: {} center: {}'.format(label, object_id, center))

def objects_lost(list_of_objects):
    '''
    '''
    print('app.py: objects_lost: {}'.format(list_of_objects))


if __name__ == "__main__":
    main()
