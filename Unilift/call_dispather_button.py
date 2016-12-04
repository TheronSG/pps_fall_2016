import time


class CallDispatcherButton:
    SLEEP_TIME = 0.33

    def __init__(self, elevator_link):
        self.elevator_link = elevator_link
        self.state = False
        self.status = True

    def press(self):
        self.state = True

    def set_end_status(self):
        self.status = False

    def main_cycle(self):
        while self.status:
            if self.state:
                self.state = False
                self.elevator_link.start_record_speaker_message()
            time.sleep(self.SLEEP_TIME)
