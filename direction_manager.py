import time

ENTER_KEY = 'in_entry'
EXIT_KEY = 'in_exit'

class DirectionManager:
    '''
    Keeps track of object times when they enter an entry or exit zone. The order
    of crossing determines if they are entering or leaving a given area.
    '''

    def __init__(self, new_entry_callback, new_exit_callback):
        self.records = {}
        self.entry_callback = new_entry_callback
        self.exit_callback = new_exit_callback
        # No callback for when tracking finishes yet

    def in_entry(self, object_id):
        prior = self.records.get(object_id, None)
        if prior is None:
            self._add_new(object_id, time.time())
            return self.in_entry(object_id)
        prior[ENTER_KEY] = time.time()
        self.records[object_id] = prior

    def in_exit(self, object_id):
        prior = self.records.get(object_id, None)
        if prior is None:
            # No prior entry record, they begin in the location prior to start
            self._add_new(object_id, None)
            return self.in_exit(object_id)
        prior[EXIT_KEY] = time.time()
        self.records[object_id] = prior

    def tracking_ended_for(self, object_ids):
        print('direction_manager.py: tracking_ended_for: object_ids: {}'.format(object_ids))
        for object_id in object_ids:
            self.check_enter_exit(object_id)

    def check_enter_exit(self, object_id):
        now = time.time()
        if self.did_enter(object_id):
            self.entry_callback(now)
            return True
        if self.did_exit(object_id):
            self.exit_callback(now)
            return True
        return False

    def did_enter(self, object_id):
        prior = self.records.get(object_id, None)
        if prior is None:
            return False
        entered = prior.get(ENTER_KEY, None)
        if entered is None:
            return False
        exit = prior.get(EXIT_KEY, None)
        if exit is None:
            return False
        if entered < exit:
            return False
        return True

    def did_exit(self, object_id):
        prior = self.records.get(object_id, None)
        if prior is None:
            return False
        entered = prior.get(ENTER_KEY, None)
        if entered is None:
            return False
        exit = prior.get(EXIT_KEY, None)
        if exit is None:
            return False
        if entered > exit:
            return False
        return True

    def _add_new(self, object_id, dtime):
        self.records[object_id] = {ENTER_KEY: dtime}

