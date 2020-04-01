
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
        displayed_frame_size = False
        while True:
            frame = video_stream.read()

            # Print out the frame size
            if displayed_frame_size == False:
                height, width, channels = frame.shape
                print('alwaysai.py: start_video_detection_with_streamer: frame h x w: {} x {}'.format(height, width))
                displayed_frame_size = True

            # Run the object detector
            results = object_detector.detect_objects(
                frame, confidence_level=od_config.confidence)
            predictions = results.predictions

            # Filter by target labels if arg passed in
            if labels:
                predictions = edgeiq.filter_predictions_by_label(
                    predictions, labels)
            
            # Update the tracker so we can id each instance of an object
            tracked_predictions = centroid_tracker.update(predictions).items()

            # Create a list of current tracked prediction object ids
            tracked_prediction_ids = [object_id for object_id, _ in tracked_predictions]

            #  Enable to blank out current tracked ids based on zero results from object detector
            # if len(predictions) > 0:
            #     # The centroid tracker doesn't blank itself out for the last known
            #     #  detected object
            #     tracked_prediction_ids = [object_id for object_id, _ in tracked_predictions]
            # else:
            #     tracked_prediction_ids = []

            # Checked for lost predictions by comparing the current list against the
            #  last cycle's detected list
            lost_ids = lost_object_ids(tracked_prediction_ids, last_detected_ids)
            if len(lost_ids) > 0:
                detection_lost_callback(lost_ids)

            # Assign current ids to last detected for reference in the next loop
            last_detected_ids = copy.deepcopy(tracked_prediction_ids)

            # Notify callback of connections
            marked_predictions = []
            for (object_id, prediction) in tracked_predictions:                
                detection_callback(object_id, prediction.label, prediction.box.center)

                prediction.label = "Person {}".format(object_id)
                marked_predictions.append(prediction)

            frame = edgeiq.markup_image(
                frame, marked_predictions, show_labels=True,
                show_confidences=False, colors=object_detector.colors)

            # Streamer Info
            text = []
            text.append("Model: {}".format(object_detector.model_id))
            text.append(
                "Inference time: {:1.3f} s".format(results.duration))
            streamer.send_data(frame, text)

            # Check exit conditions
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

def lost_object_ids(current_ids, last_ids):
    if len(last_ids) == 0:
        # print('alwaysai.py: lost_object_ids: No ids listed in last_ids')
        return []
    lost = list(set(last_ids) - set(current_ids))
    if len(lost) == 0:
        # print('alwaysai.py: lost_object_ids: No lost ids detected between current: {} and last: {}:'.format(current_ids, last_ids))
        return []
    return lost

# SIMPLE IMPLEMENTATION
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
