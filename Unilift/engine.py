import time


class Engine:
    SLEEP_TIME = 0.33
    MOTION_STATE = {'MOVING': 1, 'WAITING': 0,
                    1: 'MOVING', 0: 'WAITING'}

    def __init__(self, server_link, engine_num):
        self.server_link = server_link
        self.engine_num = engine_num
        self.motion_state = self.MOTION_STATE['WAITING']
        self.motion_stage = 0
        self.current_floor = 0
        self.target_floor = None
        self.status = False

    def set_end_status(self):
        self.status = False

    def get_motion_params(self):
        return {'current_floor': self.current_floor,
                'target_floor': self.target_floor,
                'motion_state': self.MOTION_STATE[self.motion_state]}

    def main_cycle(self):
        self.status = True
        while self.status:
            if self.motion_state == self.MOTION_STATE['MOVING']:
                if self.motion_stage == 0:
                    if self.target_floor - self.current_floor > 0:
                        self.current_floor += 1
                    elif self.target_floor - self.current_floor < 0:
                        self.current_floor -= 1
                    if self.current_floor == self.target_floor:
                        self.target_floor = None
                        self.motion_state = self.MOTION_STATE['WAITING']
                    print('[Engine {}] Current floor: {}'.format(self.engine_num,
                                                                 self.current_floor + 1))
                    self.server_link.receive_motion_params(self.engine_num,
                                                           self.get_motion_params())
                self.motion_stage = (self.motion_stage + 1) % 4
            time.sleep(self.SLEEP_TIME)

    def set_target_floor(self, target_floor):
        self.target_floor = target_floor
        self.motion_state = self.MOTION_STATE['MOVING']
        self.server_link.receive_motion_params(self.engine_num, self.get_motion_params())

    def stop_motion(self):
        if self.target_floor - self.current_floor > 0:
            self.target_floor = self.current_floor + 1
        elif self.target_floor - self.current_floor < 0:
            self.target_floor = self.current_floor + 1
        self.server_link.receive_motion_params(self.engine_num, self.get_motion_params())
