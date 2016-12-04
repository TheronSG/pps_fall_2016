class SetTargetFloorButton:
    def __init__(self, server_link, elevator_num):
        self.server_link = server_link
        self.elevator_num = elevator_num

    def press(self, floor):
        self.server_link.move_elevator(self.elevator_num, floor)
