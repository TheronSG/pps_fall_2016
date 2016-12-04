import time

from call_dispather_button import CallDispatcherButton
from doors_sensor import DoorsSensor
from set_target_floor_button import SetTargetFloorButton
from weight_sensor import WeightSensor
from speaker import Speaker
from microphone import Microphone
from threading import Thread


class Elevator:
    LIGHT = {'ON': 1, 'OFF': 0,
             1: 'ON', 0: 'OFF'}
    DOORS = {'OPENED': 3, 'OPENING': 2, 'CLOSING': 1, 'CLOSED': 0,
             3: 'OPENED', 2: 'OPENING', 1: 'CLOSING', 0: 'CLOSED'}
    DOORS_OPENED_STAGE = 0
    DOORS_CLOSED_STAGE = 4
    DOORS_OPENED_TIME = 10
    SLEEPING_TIME = 0.33

    def __init__(self, server_link, elevator_num):
        self.server_link = server_link
        self.elevator_num = elevator_num
        self.light_state = self.LIGHT['OFF']
        self.doors_state = self.DOORS['CLOSED']
        self.doors_sensor = DoorsSensor(self)
        self.weight_sensor = WeightSensor(self)
        self.speaker = Speaker(self)
        self.microphone = Microphone(self)
        self.set_target_floor_button = SetTargetFloorButton(self.server_link, self.elevator_num)
        self.call_dispatcher_button = CallDispatcherButton(self)
        self.doors_closing_stage = self.DOORS_CLOSED_STAGE
        self.status = True
        self._threads = []

    def set_end_status(self):
        self.status = False

    def start_record_speaker_message(self):
        self.microphone.set_record_state()

    def send_message_to_server(self, message):
        self.server_link.send_message_to_dispatcher(message, self.elevator_num)

    def light_on(self):
        if self.light_state != self.LIGHT['ON']:
            self.light_state = self.LIGHT['ON']
            print('[Elevator {}] Light was turned on'.format(self.elevator_num))

    def light_off(self):
        if (self.light_state != self.LIGHT['OFF'] and self.doors_state not in
                (self.DOORS['OPENING'], self.DOORS['OPENED'], self.DOORS['CLOSING'])):
            self.light_state = self.LIGHT['OFF']
            print('[Elevator {}] Light was turned off'.format(self.elevator_num))

    def close_doors(self):
        if self.doors_state not in (self.DOORS['CLOSED'], self.DOORS['CLOSING']):
            print('[Elevator {}] Start closing doors'.format(self.elevator_num))
            self.doors_state = self.DOORS['CLOSING']
        else:
            print('[Elevator {}] Doors already closed'.format(self.elevator_num))

    def open_doors(self):
        if self.doors_state not in (self.DOORS['OPENING'], self.DOORS['OPENED']):
            self.light_on()
            print('[Elevator {}] Start opening doors'.format(self.elevator_num))
            self.doors_state = self.DOORS['OPENING']
        else:
            print('[Elevator {}] Doors already opened'.format(self.elevator_num))

    def get_current_state(self):
        return {'doors_state': self.DOORS[self.doors_state],
                'light_state': self.LIGHT[self.light_state],
                **self.weight_sensor.get_weight_status()}

    def main_cycle(self):
        self._threads.append(Thread(target=self.doors_sensor.main_cycle))
        self._threads.append(Thread(target=self.weight_sensor.main_cycle))
        self._threads.append(Thread(target=self.microphone.main_cycle))
        self._threads.append(Thread(target=self.call_dispatcher_button.main_cycle))

        for thread in self._threads:
            thread.start()
        doors_opened_time = 0

        print('[Elevator {}] Running...'.format(self.elevator_num + 1))
        while True:
            if self.doors_state == self.DOORS['CLOSING']:
                self.doors_closing_stage += 1
                if self.doors_closing_stage >= self.DOORS_CLOSED_STAGE:
                    self.doors_state = self.DOORS['CLOSED']
                    self.doors_closing_stage = self.DOORS_CLOSED_STAGE
                    print('[Elevator {}] Doors closed'.format(self.elevator_num + 1))
            elif self.doors_state == self.DOORS['OPENING']:
                self.doors_closing_stage -= 1
                if self.doors_closing_stage <= self.DOORS_OPENED_STAGE:
                    self.doors_state = self.DOORS['OPENED']
                    self.doors_closing_stage = self.DOORS_OPENED_STAGE
                    print('[Elevator {}] Doors opened'.format(self.elevator_num + 1))
                    weight_status = self.weight_sensor.get_weight_status()
                    if weight_status['weight'] == 0:
                        self.weight_sensor.weight = 20
                        print('You are now in elevator {}'.format(self.elevator_num + 1))
                    else:
                        self.weight_sensor.weight = 0
                        print('You left elevator {}'.format(self.elevator_num + 1))
            elif self.doors_state == self.DOORS['OPENED']:
                doors_opened_time += 1
                if doors_opened_time == self.DOORS_OPENED_TIME:
                    doors_opened_time = 0
                    self.close_doors()
            if not self.status:
                self.doors_sensor.set_end_status()
                self.weight_sensor.set_end_status()
                self.microphone.set_end_status()
                self.call_dispatcher_button.set_end_status()
                break
            time.sleep(self.SLEEPING_TIME)

        for thread in self._threads:
            thread.join()
