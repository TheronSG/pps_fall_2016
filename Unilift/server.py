from engine import Engine
from cabin import Cabin
from threading import Thread
from smoke_sensor import SmokeSensor
from simple_motion_algorithm import SimpleMotionAlgorithm
import time


class Server:
    SLEEP_TIME = 0.01

    def __init__(self):
        self.FLOORS_NUMBER = 10
        self.ELEVATORS_NUM = 2
        self.engines = []
        self.cabins = []
        self.motions_params = []
        self.motion_algo = SimpleMotionAlgorithm(self.ELEVATORS_NUM)
        self.smoke_sensor = SmokeSensor(self)
        for i in range(self.ELEVATORS_NUM):
            engine = Engine(self, i)
            self.engines.append(engine)
            cabin = Cabin(i)
            self.cabins.append(cabin)
            self.motions_params.append({})
        self._threads = []
        self.status = False

    def call_cabin(self, target_floor):
        elevator_num = self.motion_algo.add_target_floor(self.motions_params,
                                                         target_floor,
                                                         elevator_num=None)
        if elevator_num is not None:
            self.engines[elevator_num].set_target_floor(target_floor)

    def smoke_exit(self):
        print("Alarm! Smoke is detected!")
        #TODO: реализовать интерфейс
        for i in range(self.ELEVATORS_NUM):
            self.engines[i].set_end_status()
            self.cabins[i].set_end_status()

    def send_message_to_dispatcher(self, message):
        pass

    def send_message_to_passenger(self, message):
        pass

    def receive_motion_params(self, engine_num, motion_params):
        self.motions_params[engine_num] = motion_params

    def run(self):
        for i in range(self.ELEVATORS_NUM):
            self._threads.append(Thread(target=self.engines[i].main_cycle))
            self._threads.append(Thread(target=self.cabins[i].main_cycle))

        self._threads.append(Thread(target=self.smoke_sensor.main_cycle()))

        for thread in self._threads:
            thread.start()

        waiting_states = [True] * self.ELEVATORS_NUM
        self.status = True
        while self.status:
            for i, motion_params in enumerate(self.motions_params):
                if motion_params['motion_state'] == 'WAITING':
                    cabin_state = self.cabins[i].get_current_state()
                    if cabin_state['doors_state'] == 'CLOSED':
                        if waiting_states[i]:
                            self.cabins[i].open_doors()
                            waiting_states[i] = False
                        else:
                            target_floor = self.motion_algo.get_next_target(motion_params['current_floor'], i)
                            if target_floor is not None:
                                self.engines[i].set_target_floor(target_floor)
                            waiting_states[i] = True
            time.sleep(self.SLEEP_TIME)

        for thread in self._threads:
            thread.join()
