import time


class WeightSensor:
    SLEEP_TIME = 0.33
    WEIGHT = {'LOW_WEIGHT': 2, 'NORMAL_WEIGHT': 1, 'HIGH_WEIGHT': 0,
              2: 'LOW_WEIGHT', 1: 'NORMAL_WEIGHT', 0: 'HIGH_WEIGHT'}

    def __init__(self, cabin_link):
        self.min_weight = 10
        self.max_weight = 100
        self.cabin_link = cabin_link
        self.weight = 0
        self.status = False

    # TODO: функция для выхода
    def set_end_status(self):
        self.status = False

    def get_current_weight(self):
        return self.weight

    def get_weight_status(self):
        current_weight = self.get_current_weight()
        if current_weight < self.min_weight:
            weight_status = self.WEIGHT[2]
        elif current_weight < self.max_weight:
            weight_status = self.WEIGHT[1]
        else:
            weight_status = self.WEIGHT[0]

        return {'weight': current_weight, 'weight_status': weight_status}

    def main_cycle(self):
        print('[Weight Sensor {}] Running...'.format(self.cabin_link.cabin_num))
        self.status = True
        while self.status:
            if self.min_weight <= self.get_current_weight() <= self.max_weight:
                self.cabin_link.light_on()
            elif self.get_current_weight() > self.max_weight:
                self.cabin_link.light_on()
                pass
            else:
                self.cabin_link.light_off()
            time.sleep(self.SLEEP_TIME)
