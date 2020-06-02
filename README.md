# Capacity Detector
This application is meant to detect people from a live or recorded videostream and determine if they are entering or exiting a location. That info is then can be sent via a POST call to a URL endpoint for processing.


**ENTRY-EXIT ZONES**
The app uses configurable entry and exit zones to determine if someone is entering or exiting a location. Zones are made up of rectangular areas in the video frame. Multiple entry and exit zones may be added to fit complex environments.

ENTER CRITERIA: When a detected person crosses from an entry to an exit zone, then disappears from tracking.

EXIT CRITERIA: When a detected person crosses from exit to an entry zone, then disappears from tracking.

IGNORE CRITERIA: Any detected person who does not cross both an entry and exit zone before tracking of them ends.

**JSON PAYLOAD**
When either an entry or exit is detected, the app will send a call to the URL endpoints designated in the `config.json` file. The payload consists of the following:
```
{
    "device_id": "<id_of_app_instance>",
    "timestamp": <UTC seconds epoch>
}
```

## REQUIREMENTS
- Sign up for [alwaysAI](https://dashboard.alwaysai.co/auth?register=true)
- Install [alwaysAI tooling](https://dashboard.alwaysai.co/docs/getting_started/development_computer_setup.html)


## WORKFLOW OPTIONS
This app can run on either a desktop/laptop development machine or on an edge device such as a Jetson Nano, Dragonboard, or Raspberry Pi that has docker installed. See the above install instruction link for more details.


## CONFIGURATION
Edit the `config.json` file to adjust the following parameters:

| PARAMETER         | DESCRIPTION                                                                                                                                                                                          | DEFAULT            | REQUIRED |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | -------- |
| camera_id         | Id of camera to use for camera detection. 0 if only one camera attached. 0 is usually the id for a built-in web cam, and 1 or higher if usb external cams are used in addition to an embedded camera | 0                  | No       |
| confidence        | Threshold for accepting a detection as valid                                                                                                                                                         | 0.5                | No       |
| enable_logs       | Should print to console additional info                                                                                                                                                              | True               | No       |
| entry_zones       | List of dictionaries defining bounding zones for parts of a frame where targets will be entering from                                                                                                | None               | Yes      |
| exit_zones        | List of dictionaries defining bounding zones for parts of the frame where targets exiting a location will be last seen                                                                               | None               | Yes      |
| device_id         | Optional identifier for a different instance of the detector for multi-cam set ups                                                                                                                   | Device MAC Address | No       |
| deregister_frames | Number of frames to count past last seen before a centroid tracker should consider an object lost                                                                                                    | 50                 | No       |
| enable_streamer   | Enable streamer to display vision output to `localhost:5000`                                                                                                                                         | false              | No       |
| filename          | Optional filename path for a file to use with the `mode`:`File` option                                                                                                                               | None               | No       |
| max_distance      | Maximum distance in pixels that a centroid tracker will search to maintain tracking on an object                                                                                                     | 50                 | No       |
| mode              | `Camera` or `File` supported. When using `File`, you must also provide a `filename` value                                                                                                            | Camera             | No       |
| model_id          | Model id to use for detecting target labels. If only 1 model specified in the `alwaysai.app.json` file, `models` object, then this value should match                                                | None               | No       |
| server_entry_url  | Endpoint for processing entry event                                                                                                                                                                  | None               | Yes      |
| server_exit_url   | Endpoint for processing exit event                                                                                                                                                                   | None               | Yes      |
| target_labels     | List of string labels that the model should filter for. If not provided than object detector will not filter                                                                                         | ["Person"]         | No       |


## ENTRY-EXIT EXAMPLES
The following are different examples of entry and exit zone configurations that can be used in the `config.json` file.

For a camera placed perpendicular to traffic with a resolution of 1280x720:
![Walking Across example](/images/walking_across.png)
```
    "entry_zones": [
        {
            "threshold": 0.2,
            "start_x": 0,
            "start_y": 0,
            "end_x": 300,
            "end_y": 720
        }
    ],
    "exit_zones": [
        {
            "threshold": 0.2,
            "start_x": 1000,
            "start_y": 0,
            "end_x": 1280,
            "end_y": 720
        }
    ]
```

For a camera placed to the side and looking down a curved hallway, for a frame resolution of 1280x720:
![Output example](/images/curved_hallway.png)
```
    "entry_zones": [
        {
            "threshold": 0.2,
            "start_x": 400,
            "start_y": 200,
            "end_x": 650,
            "end_y": 400
        }
    ],
    "exit_zones": [
        {
            "threshold": 0.2,
            "start_x": 1000,
            "start_y": 0,
            "end_x": 1280,
            "end_y": 720
        }
    ]
```

For a camera looking straight down a walkway with a resolution of 1280x720:
![Output example](/images/crowded_walkway.png)
```
    "entry_zones": [
        {
            "threshold": 0.2,
            "start_x": 0,
            "start_y": 0,
            "end_x": 100,
            "end_y": 720
        },
        {
            "threshold": 0.2,
            "start_x": 100,
            "start_y": 0,
            "end_x": 1280,
            "end_y": 100
        },
        {
            "threshold": 0.2,
            "start_x": 100,
            "start_y": 620,
            "end_x": 1280,
            "end_y": 720
        },
        {
            "threshold": 0.2,
            "start_x": 1180,
            "start_y": 100,
            "end_x": 1280,
            "end_y": 620
        }
    ],
    "exit_zones": [
        {
            "threshold": 0.2,
            "start_x": 540,
            "start_y": 200,
            "end_x": 740,
            "end_y": 520
        }
    ]
```


## MISC
Frame x,y beging with 0,0 in the upper-left hand corner of the frame.

## Support
Docs: https://dashboard.alwaysai.co/docs/getting_started/introduction.html

Community Discord: https://discord.gg/rjDdRPT

Email: support@alwaysai.co

