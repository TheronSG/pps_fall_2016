import time


class DoorsSensor:
    SLEEP_TIME = 0.33

    def __init__(self, elevator_link):
        self.elevator_link = elevator_link
        self.status = True

    def set_end_status(self):
        self.status = False

    @staticmethod
    def check_barrier():
        return False

    def main_cycle(self):
        print('[Doors Sensor {}] Running...'.format(self.elevator_link.elevator_num + 1))
        while self.status:
            if (self.elevator_link.get_current_state()['doors_state'] == 'CLOSING'
                    and self.check_barrier()):
                self.elevator_link.open_doors()
            time.sleep(self.SLEEP_TIME)
