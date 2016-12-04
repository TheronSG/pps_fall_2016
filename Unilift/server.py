from engine import Engine
from elevator import Elevator
from threading import Thread
from simple_motion_algorithm import SimpleMotionAlgorithm
import time


class Server:
    SLEEP_TIME = 0.01

    def __init__(self):
        self.FLOORS_NUMBER = 10
        self.ELEVATORS_NUM = 2
        self.elevators_motion_params = []
        self.engines = []
        self.elevators = []
        self.motion_algo = SimpleMotionAlgorithm(self.ELEVATORS_NUM)
        for i in range(self.ELEVATORS_NUM):
            engine = Engine(self, i)
            self.engines.append(engine)
            elevator = Elevator(self, i)
            self.elevators.append(elevator)
            self.elevators_motion_params.append(engine.get_motion_params())
        self._threads = []
        self.status = False

    def move_elevator(self, elevator_num, target_floor):
        elevator_state = self.elevators[elevator_num].get_current_state()
        if elevator_state['weight_status'] == 'LOW_WEIGHT':
            return False, 'Elevator is empty'
        elif elevator_state['weight_status'] == 'HIGH_WEIGHT':
            return False, 'Elevator is overloaded'

        elevator_num, new_target_floor = self.motion_algo.add_target_floor(self.elevators_motion_params,
                                                                           target_floor,
                                                                           elevator_num=elevator_num)
        if elevator_num is not None:
            self.engines[elevator_num].set_target_floor(new_target_floor)
        return True, None

    def call_elevator(self, target_floor):
        elevator_num, new_target_floor = self.motion_algo.add_target_floor(self.elevators_motion_params,
                                                                           target_floor,
                                                                           elevator_num=None)
        if elevator_num is not None:
            self.engines[elevator_num].set_target_floor(new_target_floor)

    def send_message_to_dispatcher(self, message, elevator_num):
        self.elevators[elevator_num].speaker.play_speech(message)

    def receive_motion_params(self, engine_num, motion_params):
        self.elevators_motion_params[engine_num] = motion_params

    def run(self):
        for i in range(self.ELEVATORS_NUM):
            self._threads.append(Thread(target=self.engines[i].main_cycle))
            self._threads.append(Thread(target=self.elevators[i].main_cycle))

        for thread in self._threads:
            thread.start()

        print('[Server] Running...')

        waiting_states = [False] * self.ELEVATORS_NUM
        self.status = True
        while True:
            for i, motion_params in enumerate(self.elevators_motion_params):
                if motion_params['motion_state'] == 'WAITING':
                    elevator_state = self.elevators[i].get_current_state()
                    if elevator_state['doors_state'] == 'CLOSED':
                        if waiting_states[i]:
                            self.elevators[i].open_doors()
                            waiting_states[i] = False
                        else:
                            target_floor = self.motion_algo.get_next_target(motion_params['current_floor'], i)
                            if target_floor is not None:
                                self.engines[i].set_target_floor(target_floor)
                                waiting_states[i] = True
            if not self.status:
                for i in range(self.ELEVATORS_NUM):
                    self.engines[i].set_end_status()
                    self.elevators[i].set_end_status()
                break
            time.sleep(self.SLEEP_TIME)

        for thread in self._threads:
            thread.join()

    def set_end_status(self):
        self.status = False
