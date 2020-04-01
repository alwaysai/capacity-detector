# Capacity Counter Camera Detection Component
This application is meant to be run on an edge device with a camera to detect people and determine if they are entering or exiting to a location. That info is then sent via a POST call the server's url for processing.

## CONFIGURATION
Edit the `config.json` file to adjust the following parameters:

PARAMETER | DESCRIPTION | DEFAULT | REQUIRED
------ | ------- | -------- | ------
entry_areas | List of dictionaries defining bounding boxes for parts of a frame where targets will be entering from | None | Yes
exit_areas | List of dictionaries defining bounding boxes for parts of the frame where targets exiting a location will be last seen| None | Yes
camera_id | Id of camera to use for camera detection. 0 if only one camera attached. 0 is usually the id for a built-in web cam, and 1 or higher if usb external cams are used in addition to an embedded camera | 0 | No
deregister_frames | Number of frames to count past last seen before a centroid tracker should consider an object lost | 50 | No
enable_streamer | Enable streamer to display vision output to `localhost:5000` | false | No
filename | Optional filename path for a file to use with the `mode`:`File` option | None | No
max_distance | Maximum distance in pixels that a centroid tracker will search to maintain tracking on an object | 50 | No
mode | `Camera` or `File` supported. When using `File`, you must also provide a `filename` value | Camera | No
model_id | Model id to use for detecting target labels. If only 1 model specified in the `alwaysai.app.json` file, `models` object, then this value should match | None | No
target_labels | List of string labels that the model should filter for. If not provided than object detector will not filter | ["Person"] | No



