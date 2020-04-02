
import file_manager
import alwaysai
import os

entry_zones = []
exit_zones = []

def main():
    # server_token = os.getenv("SERVER_TOKEN")
    config = file_manager.load_json('config.json')

    # 2. Start the CV Detection
    alwaysai.start_detection(config, detection_began, enter_detected, exit_detected)

def detection_began():
    '''
    '''
    print('app.py: detection_began:')

def enter_detected(object_id):
    print('app.py: enter_detected: {}'.format(object_id))

def exit_detected(object_id):
    print('app.py: exit_detected: {}'.format(object_id))

# object_ids = {}
# def object_detected(object_id, label, center):
#     '''
#     '''
#     # print('app.py: object_detected: label: {}: object_id: {} center: {}'.format(label, object_id, center))

#     # Enable to only report the first instance of a detection
#     prior = object_ids.get(object_id, False)
#     if prior is False:
#         print('app.py: object_detected: label: {}: object_id: {} center: {}'.format(label, object_id, center))
#         object_ids[object_id] = True

# def objects_lost(list_of_objects):
#     '''
#     '''
#     print('app.py: objects_lost: {}'.format(list_of_objects))


if __name__ == "__main__":
    main()
