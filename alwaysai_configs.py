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
