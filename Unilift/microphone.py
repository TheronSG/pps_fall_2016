import time


class Microphone:
    SLEEP_TIME = 0.33

    def __init__(self, elevator_link):
        self.elevator_link = elevator_link
        self.record_state = False
        self.status = True

    def record_speech(self):
        print('[Microphone {}] Type your request'.format(self.elevator_link.elevator_num + 1))
        message = input()
        self.elevator_link.send_message_to_server(message)

    def set_record_state(self):
        self.record_state = True

    def set_end_status(self):
        self.status = False

    def main_cycle(self):
        print('[Microphone {}] Running...'.format(self.elevator_link.elevator_num + 1))
        while self.status:
            if self.record_state:
                self.record_speech()
                self.record_state = False
            time.sleep(self.SLEEP_TIME)
