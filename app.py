
import file_manager
import alwaysai
import direction_manager
import os
import post
import time
import comm

def main():
    # Pull configuration
    config = file_manager.load_json('config.json')

    # Setup communications to server
    server = comm.Server(config)

    # Direction manager that translate detections to directions of travel 
    dm = direction_manager.DirectionManager(server.track_entry, server.track_exit)

    # CV Detection
    alwaysai.start_detection(config, detection_began, dm.in_entry, dm.in_exit, dm.tracking_ended_for)

def detection_began():
    print('detector: app.py: detection_began:')

if __name__ == "__main__":
    main()
