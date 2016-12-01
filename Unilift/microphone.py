import time


class Microphone:
    SLEEP_TIME = 0.33

    def __init__(self, cabin_link):
        self.cabin_link = cabin_link
        self.state = False

    def record_speech(self):
        message = input()
        self.cabin_link
        # TODO: А что дальше делать? По идеи нужно персылать сообщение диспетчеру.

    def main_cycle(self):
        print('[Microphone {}] Running...'.format(self.cabin_link.cabin_num))
        while True:
            if self.state:
                self.record_speech()
                # TODO: Что то тут еще надо написать...
            time.sleep(self.SLEEP_TIME)
