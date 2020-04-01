
import edgeiq
import alwaysai_configs
import copy

def engine():
    """Switch Engine modes if an Intel accelerator is available"""
    if is_accelerator_available() == True:
        return edgeiq.Engine.DNN_OPENVINO
    return edgeiq.Engine.DNN


def is_accelerator_available():
    """Detect if an Intel Neural Compute Stick accelerator is attached"""
    if edgeiq.find_ncs1():
        return True
    if edgeiq.find_ncs2():
        return True
    return False


def object_detector(model, should_log=True):
    """Return an object detector for a given model"""
    if model is None:
        raise Exception(
            "alwaysai.py: object_detector: model name parameter not found")
    od = edgeiq.ObjectDetection(model)
    e = engine()
    od.load(e)
    if should_log == True:
        print("alwaysai.py: object_detector: Engine: {}".format(od.engine))
        print("alwaysai.py: object_detector: Accelerator: {}\n".format(
            od.accelerator))
        print("alwaysai.py: object_detector: Model:\n{}\n".format(od.model_id))
    return od


def start_detection(config, did_start_callback, detection_callback, detection_lost_callback, should_log=True):
    '''
    '''
    od_config = alwaysai_configs.ObjectDetector(config)
    ct_config = alwaysai_configs.CentroidTracker(config)
    vs_config = alwaysai_configs.VideoStream(config)
    od = object_detector(od_config.model_id)
    t = edgeiq.CentroidTracker(
        deregister_frames=ct_config.deregister_frames, max_distance=ct_config.max_distance
    )
    vs = None
    if vs_config.mode == 'camera':
        if should_log:
            print('alwaysai.py: start_detection: enabling camera w/ id: {}'.format(vs_config.camera_id))
        vs = edgeiq.WebcamVideoStream(cam=vs_config.camera_id)
    if vs_config.mode == 'file':
        if should_log:
            print('alwaysai.py: start_detection: reading from file')
        vs = edgeiq.FileVideoStream(vs_config.filename, play_realtime=True)
    enable_streamer = config.get('enable_streamer', False)
    streamer = alwaysai_configs.DummyStreamer()
    if enable_streamer:
        print('alwaysai.py: start_detection: ENABLING streamer')
        streamer = edgeiq.Streamer()
    start_video_detection_with_streamer(vs, od_config, od, streamer, t, did_start_callback, detection_callback, detection_lost_callback)

# def start_video_detection(
#         video_stream,
#         od_config: alwaysai_configs.ObjectDetector,
#         object_detector: edgeiq.ObjectDetection,
#         callback):
#     '''
#     '''
#     try:
#         video_stream.start()
#         while True:
#             frame = video_stream.read()
#             results = object_detector.detect_objects(
#                 frame, confidence_level=od_config.confidence)
#             for prediction in results.predictions:
#                 callback("test", prediction.label, prediction.box.center)

#             # File video streams need to check for additional frames before stopping
#             more = getattr(video_stream, "more", None)
#             if callable(more):
#                 if video_stream.more() == False:
#                     break

#     finally:
#         video_stream.stop()



def start_video_detection_with_streamer(
        video_stream,
        od_config,
        object_detector,
        streamer,
        centroid_tracker,
        did_start_callback,
        detection_callback,
        detection_lost_callback):
    '''
    Start video detection with browser accessible streamer enabled
    '''
    labels = od_config.target_labels

    # Store list of object_ids detected in prior cycle
    last_detected_ids = []
    try:
        video_stream.start()
        streamer.setup()
        did_start_callback()
        while True:
            frame = video_stream.read()
            # print('alwaysai.py: start_video_detection_with_streamer: frame: {}'.format(frame))
            results = object_detector.detect_objects(
                frame, confidence_level=od_config.confidence)
            predictions = results.predictions

            # If target labels passed in, filter for them
            if labels:
                predictions = edgeiq.filter_predictions_by_label(
                    predictions, labels)
            
            tracked_predictions = centroid_tracker.update(predictions).items()

            # Check for objects no longer being tracked
            tracked_prediction_ids = [object_id for object_id, _ in tracked_predictions]
            # print('alwaysai.py: tracked_prediction_ids: {}'.format(tracked_prediction_ids))
            # print('alwaysai.py: last_detected_ids: {}'.format(last_detected_ids))
            if len(last_detected_ids) > 0:
                lost = list(set(tracked_prediction_ids) - set(last_detected_ids))
                if len(lost) > 0:
                    detection_lost_callback(lost)            
            last_detected_ids = tracked_prediction_ids

            text = []
            text.append("Model: {}".format(object_detector.model_id))
            text.append(
                "Inference time: {:1.3f} s".format(results.duration))
            for (object_id, prediction) in tracked_predictions:
                detection_callback(object_id, prediction.label, prediction.box.center)

            frame = edgeiq.markup_image(
                frame, predictions, show_labels=True,
                show_confidences=False, colors=object_detector.colors)
            streamer.send_data(frame, text)

            # File video streams need to check for additional frames before stopping
            more = getattr(video_stream, "more", None)
            if callable(more):
                if video_stream.more() == False:
                    break
            if streamer.check_exit():
                break
    finally:
        video_stream.stop()
        streamer.close()