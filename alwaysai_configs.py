class CentroidTracker:
        def __init__(self, config):
            '''
            '''
            self.deregister_frames = config.get('deregister_frames', 50)
            self.max_distance = config.get('max_distance', 50)


class ObjectDetector:
    def __init__(self, config):
        '''
        '''
        model_id = config.get('model_id', None)
        if model_id is None:
            raise ValueError(
                'alwaysai_config.py: __init__: Required model_id value not found in the constructor object')
        self.model_id = model_id
        self.confidence = config.get('confidence', 0.5)
        self.target_labels = config.get('target_labels', None)


class VideoStream:
    def __init__(self, config):
        '''
        '''
        self.mode = config.get('mode', 'camera')
        if self.mode == 'camera':
            self.camera_id = config.get('camera_id', 0)
        elif self.mode == 'file':
            self.filename = config.get('filename', None)
            if self.filename is None:
                raise ValueError(
                    'alwaysai_VS_config.py: __init__: No filename value provided by config')
        else:
            raise ValueError(
                'alwaysai_VS_config.py: __init__: Unsupported mode detected: {}'.format(self.mode))


class DummyStreamer:
    '''
    Empty streamer class if streamer output not requested
    '''

    def __init__(self):
        pass

    def setup(self):
        pass

    def send_data(self, arg1, arg2):
        pass

    def check_exit(self):
        pass

    def close(self):
        pass


def zones_from(list_of_zone_info):
    # result = [Zone(zone_info) for zone_info in list_of_zone_info]
    result = []
    for zone_info in list_of_zone_info:
        zone = Zone(zone_info)
        result.append(zone)
    return result


class Zone:
    '''
    '''

    def __init__(self, config):
        self.threshold = config.get('threshold', 0.5)
        self.start_x = config.get('start_x', None)
        self.start_y = config.get('start_y', None)
        self.end_x = config.get('end_x', None)
        self.end_y = config.get('end_y', None)
        self.box = None

    def __repr__(self):
        return "Zone(threshold:{}, start_x:{}, start_y:{}, end_x:{}, end_y:{}, box:{}".format(self.threshold, self.start_x, self.start_y, self.end_x, self.end_y, self.box)

    def __str__(self):
        return "Zone.str(threshold:{}, start_x:{}, start_y:{}, end_x:{}, end_y:{}, box:{}".format(self.threshold, self.start_x, self.start_y, self.end_x, self.end_y, self.box)

    def is_box_available(self):
        # TODO: Check for correct value as well
        if self.start_x is None:
            return False
        if self.start_y is None:
            return False
        if self.end_x is None:
            return False
        if self.end_y is None:
            return False
        return True
