import time


class Display:
    SLEEP_TIME = 0.1

    def __init__(self, cabin_link):
        self.cabin_link = cabin_link
        self.current_cabin_floor = 1
        self.current_direction = 0
        # TODO: Лучше @current_direction сделать не булевым. Потому что кабина может и стоять.

    def set_direction(self, direction):
        self.current_direction = direction
        # TODO:  Будем ли использовать три состояния?
        if direction == 1:
            print('[Display {}] Moving up'.format(self.cabin_link.cabin_num + 1))
        elif direction == -1:
            print('[Display {}] Stay'.format(self.cabin_link.cabin_num + 1))
        else:
            print('[Display {}] Moving down'.format(self.cabin_link.cabin_num + 1))

    def set_cabin_floor(self, floor):
        self.current_cabin_floor = floor
        print('[Display {}] Current floor {}'.format(self.cabin_link.cabin_num + 1, floor))

    def main_cycle(self):
        print('[Display {}] Running...'.format(self.cabin_link.cabin_num + 1))
        while True:
            if ():
                pass
            #     TODO: Проверка, что состояние этажа изменилось и вывести его.
            time.sleep(self.SLEEP_TIME)