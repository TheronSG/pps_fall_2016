import time


class SmokeSensor:
    SLEEP_TIME = 0.33

    def __init__(self, cabin_link):
        self.cabin_link = cabin_link
        self.smokeThreeshold = False
        # TODO: Зачем @smokeThreeshold int? Типо уровень? Не проще сделать булево значение?

    def set_smoke(self):
        self.smokeThreeshold = True

    def check_smoke_level(self):
        return self.smokeThreeshold

    def main_cycle(self):
        print('[Smoke Sensor {}] Running...'.format(self.cabin_link.cabin_num))
        while True:
            if self.check_smoke_level():
                # TODO(): придумать интерфейс для передачи информации о дыме
                pass
            time.sleep(self.SLEEP_TIME)
