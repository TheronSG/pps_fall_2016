import time


class Microphone:
    SLEEP_TIME = 0.33

    def __init__(self, cabin_link):
        self.cabin_link = cabin_link
        self.state = False

    def start_record_speech(self):
        message = input()
        # TODO: А что дальше делать? По идеи нужно персылать сообщение диспетчеру.

    #     TODO: Понять, нужна ли эта функция, зачем вообще разделение этих функций
    def stop_record_speech(self):
        pass

    def main_cycle(self):
        print('[Microphone {}] Running...'.format(self.cabin_link.cabin_num))
        while True:
            if self.state:
                self.start_record_speech()
                # TODO: Что то тут еще надо написать...
            time.sleep(self.SLEEP_TIME)
