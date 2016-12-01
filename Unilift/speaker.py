class Speaker:
    SLEEP_TIME = 0.33

    def __init__(self, cabin_link):
        self.cabin_link = cabin_link

    def play_speech(self, message):
        print('[Speaker {}] Type dispatchers\' answer'.format(self.cabin_link.cabin_num))
        message = input()
        print('[Speaker {}] Dispatcher says: '.format(self.cabin_link.cabin_num) + message)

    def init(self):
        print('[Speaker {}] Running...'.format(self.cabin_link.cabin_num))
