from engine import Engine
from cabin import Cabin
from threading import Thread
from smoke_sensor import SmokeSensor
import time


class Server:
    def __init__(self):
        self.FLOORS_NUMBER = 10
        self.ELEVATORS_NUM = 2
        self.engines = []
        self.cabins = []
        self.smoke_sensor = SmokeSensor(self)
        for i in range(self.ELEVATORS_NUM):
            engine = Engine(self, i)
            self.engines.append(engine)
            cabin = Cabin(i)
            self.cabins.append(cabin)
        self._threads = []

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

    @staticmethod
    def print_available_command():
        print('To open door type: open <lift number>')
        print('To close door type: close <lift number>')
        print('To exit programme type: exit')
        # TODO: написать остальные команды

    def handle(self, command):
        parts = command.split(' ')
        while True:
            try:
                parts.remove('')
            except ValueError:
                break
        if parts[0] == 'open':
            if len(parts) > 2 or len(parts) == 1:
                print('Error! Expected 1 arguments for command \'open\', got {}'.format(len(parts) - 1))
                return False
            try:
                parts[1] = int(parts[1])
            except ValueError:
                print('Error! Type of parameter for command \'open\' must be int')
                return False
            if parts[1] > self.ELEVATORS_NUM or parts[1] < 1:
                print('Error! The {} lift does not exist.'.format(parts[1]))
                return False
            self.cabins[parts[1] - 1].open_doors()
            self.cabins[parts[1] - 1].wait_doors()

        elif parts[0] == 'close':
            if len(parts) > 2 or len(parts) == 1:
                print('Error! Expected 1 argument for command \'close\', got {}'.format(len(parts) - 1))
                return False
            try:
                parts[1] = int(parts[1])
            except ValueError:
                print('Error! Type of parameter for command \'close\' must be int')
                return False
            if parts[1] > self.ELEVATORS_NUM or parts[1] < 1:
                print('Error! The {} lift does not exist.'.format(parts[1]))
                return False
            self.cabins[parts[1] - 1].close_doors()
            self.cabins[parts[1] - 1].wait_doors()

        elif parts[0] == 'call':
            if len(parts) > 2 or len(parts) == 1:
                print('Error! Expected 1 argument for command \'call\', got {}'.format(len(parts) - 1))
                return False
            try:
                parts[1] = int(parts[1])
            except ValueError:
                print('Error! Type of parameter for command \'call\' must be int')
                return False

            print(self.cabins[parts[1]].get_current_state())

            # TODO: реализовать данную функцию, только ли вызов лифта тут будет обрабатываться?

            print(self.cabins[parts[1]].get_current_state())

        elif parts[0] == 'smoke':
            if len(parts) > 1:
                print('Error! Expected 0 argument for command \'smoke\', got {}'.format(len(parts) - 1))
                return False
            print(self.cabins[0].get_current_state())
            print(self.cabins[1].get_current_state())
            self.smoke_exit()
            return True
            # TODO: реализовать данную функцию, и скорее всего здесь нужно выводить информацию о состояниях всех лифтов

            # print(self.cabins[0].get_current_state())
            # print(self.cabins[1].get_current_state())
        elif parts[0] == 'go':
            if len(parts) > 2 or len(parts) == 1:
                print('Error! Expected 1 argument for command \'close\', got {}'.format(len(parts) - 1))
                return False
            try:
                parts[1] = int(parts[1])
            except ValueError:
                print('Error! Type of parameter for command \'close\' must be int')
                return False
            if parts[1] > self.ELEVATORS_NUM or parts[1] < 1:
                print('Error! The {} lift does not exist.'.format(parts[1]))
                return False
            print(self.cabins[parts[1]].get_current_state())
            self.cabins[parts[1]].close_doors()
            print(self.cabins[parts[1]].get_current_state())

        elif parts[0] == 'exit':
            if len(parts) > 1:
                print('Error! Expected 0 argument for command \'exit\', got {}'.format(len(parts) - 1))
                return False
            for i in range(self.ELEVATORS_NUM):
                self.engines[i].set_end_status()
                self.cabins[i].set_end_status()
            return True
        else:
            print('Wrong command: {}'.format(command))
        return False

    def receive_motion_params(self, engine_num):
        pass

    def run(self):
        for i in range(self.ELEVATORS_NUM):
            self._threads.append(Thread(target=self.engines[i].main_cycle))
            self._threads.append(Thread(target=self.cabins[i].main_cycle))

        self._threads.append(Thread(target=self.smoke_sensor.main_cycle()))

        for thread in self._threads:
            thread.start()

        time.sleep(0.5)

        while True:
            print('Choose action:')
            self.print_available_command()
            command = input()
            status = self.handle(command)
            if status:
                break

        for thread in self._threads:
            thread.join()
