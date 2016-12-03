class Speaker:
    SLEEP_TIME = 0.33

    def __init__(self, cabin_link):
        self.cabin_link = cabin_link
        self.state = False

    def get_state(self):
        return self.state

    def set_state(self):
        self.state = False

    def play_speech(self, message):
        print('[Speaker {}] Type dispatchers\' answer'.format(self.cabin_link.cabin_num + 1))
        message = input()
        print('[Speaker {}] Dispatcher says: '.format(self.cabin_link.cabin_num + 1) + message)
        self.state = True

    def init(self):
        print('[Speaker {}] Running...'.format(self.cabin_link.cabin_num + 1))
