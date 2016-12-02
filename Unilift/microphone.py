import time


class Microphone:
    SLEEP_TIME = 0.33

    def __init__(self, cabin_link):
        self.cabin_link = cabin_link
        self.state = False
        self.status = True

    def record_speech(self):
        print('[Microphone {}] Type your request'.format(self.cabin_link.cabin_num + 1))
        message = input()
        self.cabin_link.send_message_to_dispatcher(message)

    def set_true_state(self):
        self.state = True

    def set_end_status(self):
        self.status = False

    def main_cycle(self):
        print('[Microphone {}] Running...'.format(self.cabin_link.cabin_num + 1))
        while self.status:
            if self.state:
                self.record_speech()
                self.state = False
            time.sleep(self.SLEEP_TIME)
