
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


ENTER_CALLBACK = None
EXIT_CALLBACK = None

# def start_detection(config, did_start_callback, detection_callback, detection_lost_callback, should_log=True):
def start_detection(config, did_start_callback, enter_callback, exit_callback, did_end_object_callback, should_log=True):
    '''
    '''
    global ENTER_CALLBACK
    global EXIT_CALLBACK
    ENTER_CALLBACK = enter_callback
    EXIT_CALLBACK = exit_callback
    print('alwaysai.py: start_detection: enter_callback: {}'.format(ENTER_CALLBACK))

    # Configs
    od_config = alwaysai_configs.ObjectDetector(config)
    ct_config = alwaysai_configs.CentroidTracker(config)
    vs_config = alwaysai_configs.VideoStream(config)
    od = object_detector(od_config.model_id)
    t = edgeiq.CentroidTracker(
        deregister_frames=ct_config.deregister_frames, max_distance=ct_config.max_distance
    )
    en_zones_config = config.get('entry_zones', [])
    ex_zones_config = config.get('exit_zones', [])
    entry_zones = zones_from_config(en_zones_config)
    exit_zones = zones_from_config(ex_zones_config)
    vs = None

    # print('alwaysai.py: start_detection: en_zones_config: {}'.format(en_zones_config))
    # print('alwaysai.py: start_detection: entry_zones: {}'.format(entry_zones))

    # Inits
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

    # Start
    start_video_detection_with_streamer(vs, od_config, od, streamer, t, entry_zones, exit_zones, did_start_callback, did_detect, did_end_object_callback)

def did_detect(tuple_list, entry_zones, exit_zones):
    '''
    Determine if objects are coming or going
    '''
    # print('alwaysai.py: did_detect: entry zones: {}'.format(entry_zones))
    global ENTER_CALLBACK
    global EXIT_CALLBACK
    for object_id, prediction in tuple_list:
        box = prediction.box
        if is_box_in_zones(box, entry_zones):
            # print('alwaysai.py: did_detect: object_id {} in entry zone'.format(object_id))
            ENTER_CALLBACK(object_id)
        if is_box_in_zones(box, exit_zones):
            # print('alwaysai.py: did_detect: object_id {} in exit zone'.format(object_id))
            EXIT_CALLBACK(object_id)
    # print('alwaysai.py: did_detect: {}'.format(tuple_list))
    return None

def start_video_detection_with_streamer(
        video_stream,
        od_config,
        object_detector,
        streamer,
        centroid_tracker,
        entry_zones,
        exit_zones,
        did_start_callback,
        detection_callback,
        did_end_object_callback):
    '''
    Start video detection with browser accessible streamer enabled
    '''
    labels = od_config.target_labels
    displayed_frame_size = False

    try:
        video_stream.start()
        streamer_enabled = isinstance(streamer, edgeiq.Streamer)
        if streamer_enabled:
            entry_predictions = entry_predictions_from(entry_zones)
            exit_predictions = exit_predictions_from(exit_zones)
            streamer.setup()
        did_start_callback()

        prior_track = {}

        while True:
            frame = video_stream.read()

            # Print out the frame size
            if displayed_frame_size == True:
                height, width, channels = frame.shape
                print('alwaysai.py: start_video_detection_with_streamer: frame w x h: {} x {}'.format(width, height))
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
            current_track = centroid_tracker.update(predictions)

            if len(predictions) > 0:
                # print('alwaysai.py: start_video_detection_with_streamer: objects detected: {}'.format(current_track.items()))
                detection_callback(current_track.items(), entry_zones, exit_zones)

            # Find diff in object ids to see if we've stopped tracking anything
            current_keys = current_track.keys()
            prior_keys = prior_track.keys()
            diff_keys = prior_keys - current_keys
            if len(diff_keys) != 0:
                tracked_predictions = prior_track.items()
                # print('alwaysai.py: start_video_detection_with_streamer: diff_keys: {}. prior_tracks: {}'.format(diff_keys, tracked_predictions))
                did_end_object_callback(list(diff_keys))
            
            prior_track = copy.deepcopy(current_track)

            # Update image and info for debug streamer 
            if streamer_enabled:
                marked_predictions = []
                for (object_id, prediction) in current_track.items():                
                    prediction.label = "Person {}".format(object_id)
                    marked_predictions.append(prediction)
                frame = edgeiq.markup_image(
                    frame, marked_predictions, show_labels=True,
                    show_confidences=False, colors=object_detector.colors)
                frame = edgeiq.markup_image(
                    frame, entry_predictions, show_labels=True,
                    show_confidences=False, colors=[(0, 255, 0)])
                frame = edgeiq.markup_image(
                    frame, exit_predictions, show_labels=True,
                    show_confidences=False, colors=[(0,0,255)])
                frame = edgeiq.transparent_overlay_boxes(frame, entry_predictions, alpha=0.2, colors=[(0, 200, 0)])
                frame = edgeiq.transparent_overlay_boxes(frame, exit_predictions, alpha=0.2, colors=[(0,0,200)])
                text = []
                text.append("Model: {}".format(object_detector.model_id))
                text.append(
                    "Inference time: {:1.3f} s".format(results.duration))
                streamer.send_data(frame, text)

            # Check exit conditions
            # File video streams need to check for additional frames before stopping
            more = getattr(video_stream, "more", None)
            if callable(more) and video_stream.more() == False:
                print('alwaysai.py: start_video_detection_with_streamer: file video stream ended')
                break
            if streamer.check_exit():
                break
    finally:
        video_stream.stop()
        streamer.close()


def entry_predictions_from(zones):
    '''
    Converts entry zones into predictions for use in marking up image
    '''
    # result = [edgeiq.ObjectDetectionPrediction(zone.box,1.0,"ENTRY_ZONE: Threshold {}".format(zone.threshold)) for zone in zones]
    result = []
    for i, zone in enumerate(zones):
        record = edgeiq.ObjectDetectionPrediction(zone.box, 1.0, "ENTRY_ZONE: Threshold {}".format(zone.threshold), 100 + i)
        result.append(record)
    return result

def exit_predictions_from(zones):
    '''
    Converts exit zones into predictions for use in marking up image
    '''
    # result = [edgeiq.ObjectDetectionPrediction(zone.box,1.0,"EXIT_ZONE: Threshold {}".format(zone.threshold)) for zone in zones]
    result = []
    for i, zone in enumerate(zones):
        record = edgeiq.ObjectDetectionPrediction(zone.box, 1.0, "EXIT_ZONE: Threshold {}".format(zone.threshold), 200 + i)
        result.append(record)
    return result

def zones_from_config(zones_config):
    # available_zones = [zone for zone in zones_list if zone.is_box_available()]
    result = []
    for zone_config in zones_config:
        zone = alwaysai_configs.Zone(zone_config)
        if zone.is_box_available()==False:
            continue
        zone.box = edgeiq.BoundingBox(zone.start_x, zone.start_y, zone.end_x, zone.end_y)
        result.append(zone)
    return result

def is_box_in_zones(box, zones):
    # print('alwaysai.py: is_box_in_zones: box: {} - zones: {}'.format(box, zones))
    for zone in zones:
        # print('alwaysai.py: is_box_in_zones: zone: {}'.format(box, zone))
        if zone.box is None:
            # zone.box = edgeiq.BoundingBox(zone.start_x, zone.start_y, zone.end_x, zone.end_y)
            print('alwaysai.py: is_box_in_zones: skipping zone with no bounding box')
            continue
        overlap = box.compute_overlap(zone.box)
        # print('alwaysai.py: is_box_in_zones: overlap: {} - threshold: {}'.format(overlap, zone.threshold))
        if overlap >= zone.threshold:
            return True
    return False

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
