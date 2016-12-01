import time


class SmokeSensor:
    SLEEP_TIME = 0.33

    def __init__(self, server_link):
        self.server_link = server_link
        self.smokeThreshold = False

    def set_smoke(self):
        self.smokeThreshold = True

    def check_smoke_level(self):
        return self.smokeThreshold

    def main_cycle(self):
        print('[Smoke Sensor] Running...')
        while True:
            if self.check_smoke_level():
                self.server_link.smoke_exit()
            time.sleep(self.SLEEP_TIME)
