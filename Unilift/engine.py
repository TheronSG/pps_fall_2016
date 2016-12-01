import time


class Engine:
    SLEEP_TIME = 0.5

    def __init__(self):
        state = False
        motion_state = None
        motion_direction = None
        current_floor = None
        target_floor = None
        self.status = False

    # TODO: функия для выхода из программы
    def set_end_status(self):
        self.status = True

    def main_cycle(self):
        while True:
            if self.status:
                break
            time.sleep(self.SLEEP_TIME)


    def set_target_floor(self):
        pass

    def stop_motion(self):
        pass
