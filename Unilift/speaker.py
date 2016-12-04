class Speaker:
    SLEEP_TIME = 0.33

    def __init__(self, elevator_link):
        self.elevator_link = elevator_link
        self.state = False

    def get_state(self):
        return self.state

    def set_state(self):
        self.state = False

    def play_speech(self, message):
        print('[Speaker {}] Type dispatchers\' answer'.format(self.elevator_link.elevator_num + 1))
        message = input()
        print('[Speaker {}] Dispatcher says: '.format(self.elevator_link.elevator_num + 1) + message)
        self.state = True

    def init(self):
        print('[Speaker {}] Running...'.format(self.elevator_link.elevator_num + 1))
