from datetime import datetime, timezone

ENTER_KEY = 'entered'
EXIT_KEY = 'exited'


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
        # print('direction_manager.py: in_entry')
        prior = self.records.get(object_id, None)
        if prior is None:
            self._add_new(object_id, datetime.now(timezone.utc))
            return self.in_entry(object_id)
        prior[ENTER_KEY] = datetime.now(timezone.utc)
        self.records[object_id] = prior

        # print('direction_manager.py: in_entry: record: {}'.format(prior))
        # self.check_enter_exit(object_id)

    def in_exit(self, object_id):
        # print('direction_manager.py: in_exit')
        prior = self.records.get(object_id, None)
        if prior is None:
            # No prior entry record, they begin in the location prior to start
            self._add_new(object_id, None)
            return self.in_exit(object_id)
        prior[EXIT_KEY] = datetime.now(timezone.utc)
        self.records[object_id] = prior
        # print('direction_manager.py: in_exit: record: {}'.format(prior))
        # self.check_enter_exit(object_id)

    def tracking_ended_for(self, object_ids):
        print('direction_manager.py: tracking_ended_for: object_ids: {}'.format(object_ids))
        for object_id in object_ids:
            self.check_enter_exit(object_id)

    def check_enter_exit(self, object_id):
        if self.did_enter(object_id):
            # print('direction_manager.py: check_enter_exit: triggering entry_callback: {}'.format(
            #     self.entry_callback))
            self.entry_callback(object_id)
            return True
        if self.did_exit(object_id):
            # print('direction_manager.py: check_enter_exit: triggering exit_callback: {}'.format(
            #     self.exit_callback))
            self.exit_callback(object_id)
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
            # print('direction_manager.py: did_enter: entered: {} exited: {}'.format(
            #     entered, exit))
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
            # print('direction_manager.py: did_exit: entered: {} exited: {}'.format(
                # entered, exit))
            return False
        return True

    def _add_new(self, object_id, dtime):
        self.records[object_id] = self._new_instance(dtime)

    def _new_instance(self, entered):
        return {ENTER_KEY: entered}
