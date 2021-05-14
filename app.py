
import file_manager
import alwaysai
import direction_manager
import comm


def main():
    # 1. Load configuration
    config = file_manager.load_json('config.json')

    # 2. Setup communications to server
    server = comm.Server(config)

    # 3. Direction manager that translate detections to directions of travel
    dm = direction_manager.DirectionManager(
        server.track_entry, server.track_exit)

    # 4. Start CV Detection
    alwaysai.start_detection(config, detection_began,
                             dm.in_entry, dm.in_exit, dm.tracking_ended_for)


def detection_began():
    """Stub for reporting when detection actually begins"""
    print('app.py: detection_began:')


if __name__ == "__main__":
    main()
