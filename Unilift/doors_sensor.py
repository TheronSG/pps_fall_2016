import time


class DoorsSensor:
    SLEEP_TIME = 0.33

    def __init__(self, cabin_link):
        self.cabin_link = cabin_link
        self.status = True

    def set_end_status(self):
        self.status = False

    @staticmethod
    def check_barrier():
        return False

    def main_cycle(self):
        print('[Doors Sensor {}] Running...'.format(self.cabin_link.cabin_num + 1))
        while self.status:
            if (self.cabin_link.get_current_state()['doors_state'] == 'CLOSING'
                    and self.check_barrier()):
                self.cabin_link.open_doors()
            time.sleep(self.SLEEP_TIME)
