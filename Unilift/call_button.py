import time


class CallButton:
    SLEEP_TIME = 0.33

    def __init__(self, server_link):
        self.server_link = server_link

    def press(self, floor):
        self.server_link.call_cabin(floor)
