import requests
import time
import cv2
import base64

'''
Handles delivery of data to specified endpoint
'''

SHOULD_LOG = False

def data(id, label):
    """Send just tracking meta data to target endpoint"""
    print('delivery.py: send_data')
    payload = {"object_id": id, "timestamp": time.time(), "label": label}
    global DATA_URL
    global SHOULD_LOG
    return _send(url=DATA_URL, data=payload, files=None, should_log=SHOULD_LOG)


def image(id, label, image):
    """Send image of object to target endpoint"""
    global IMAGES_URL
    global SHOULD_LOG
    if image is None:
        logger.log(
            'delivery.py: send_image: no image passed to send command', SHOULD_LOG)
        return None
    payload = {"object_id": id, "timestamp": time.time(), "label": label}

    # Eric's route
    # Encode image as jpeg
    image = cv2.imencode('.jpg', image)[1].tobytes()
    # Encode image in base64 representation and remove utf-8 encoding
    image = base64.b64encode(image).decode('utf-8')
    image = "data:image/jpeg;base64,{}".format(image)
    filesToUpload = {'image': image}
    # filesToUpload = {'image': (image, open(
    #     image, 'rb'), "multipart/form-data")}
    return _send(IMAGES_URL, payload, filesToUpload, SHOULD_LOG)


def _send(url, data=None, files=None, should_log=False):
    """Construct a post request and deliver"""
    try:
        r = requests.post(url=url, data=data)
        #r = requests.post(url=url, data=data, files=files)
        if r.status_code != 200:
            logger.log('delivery.py: send: post response code: {}, reason: {}'.format(
                r.status_code, r.reason), should_log)
            return r
        logger.log('delivery.py: send: successful', should_log)
        return r
    except requests.exceptions.ConnectionError:
        logger.log(
            'Connection refused for connection to: {}'.format(url), should_log)
        return 'Connection refused'
    except:
        logger.log(
            'Unknown post request error for connection to: {}'.format(url), should_log)
        return 'Unknown post request error'