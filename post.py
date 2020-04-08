import requests
import cv2
import base64

'''
Handles delivery of data to specified endpoint
'''

SHOULD_LOG = True
TIME_KEY = 'timestamp'

def data(url, payload):
    """Send just tracking meta data to target endpoint"""
    # print('post.py: data')
    # final_payload = {"timestamp": time.time(), "data": payload}
    global SHOULD_LOG
    return _send(url=url, json=payload, files=None, should_log=SHOULD_LOG)


# def image(id, label, image):
#     """Send image of object to target endpoint"""
#     global IMAGES_URL
#     global SHOULD_LOG
#     if image is None:
#         return None
#     payload = {"object_id": id, "timestamp": time.time(), "label": label}

#     # Eric's route
#     # Encode image as jpeg
#     image = cv2.imencode('.jpg', image)[1].tobytes()
#     # Encode image in base64 representation and remove utf-8 encoding
#     image = base64.b64encode(image).decode('utf-8')
#     image = "data:image/jpeg;base64,{}".format(image)
#     filesToUpload = {'image': image}
#     # filesToUpload = {'image': (image, open(
#     #     image, 'rb'), "multipart/form-data")}
#     return _send(IMAGES_URL, payload, filesToUpload, SHOULD_LOG)


def _send(url, json=None, files=None, should_log=False):
    """Construct a post request and deliver"""
    try:
        r = requests.post(url=url, json=json)
        #r = requests.post(url=url, data=data, files=files)
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
