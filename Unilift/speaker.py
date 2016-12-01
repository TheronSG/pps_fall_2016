import time


class Speaker:
    SLEEP_TIME = 0.33

    def __init__(self, cabin_link):
        self.cabin_link = cabin_link
        self.state = False
        self.status = True

    def play_speech(self, message):
        message = input()
    # TODO: Нужна ли вторая функция?

    def main_cycle(self):
        print('[Speaker {}] Running...'.format(self.cabin_link.cabin_num))
        while True:
            if self.state:
                self.start_play_speech()
                # TODO: Что еще?
            time.sleep(self.SLEEP_TIME)

