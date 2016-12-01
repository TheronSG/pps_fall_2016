class SimpleMotionAlgorithm:
    def __init__(self, elevators_num):
        self.elevators_task_queue = []
        for i in range(elevators_num):
            self.elevators_task_queue.append([])

    def add_target_floor(self, elevators_motion_params, new_target_floor, elevator_num):
        if elevator_num is not None:
            task_queue = self.elevators_task_queue[elevator_num]
            params = elevators_motion_params[elevator_num]
            target_floor = params['target_floor']
            if target_floor is not None:
                current_floor = params['current_floor']
                if (target_floor <= new_target_floor < current_floor - 1 or
                        current_floor + 1 < new_target_floor <= target_floor):
                    task_queue.insert(0, target_floor)
                    return elevator_num, new_target_floor
                else:
                    task_queue.append(new_target_floor)
                    return None, None
            else:
                task_queue.append(new_target_floor)
                return None, None
        else:
            min_queue_len = 100
            task_queue = None
            for i in range(len(self.elevators_task_queue)):
                queue_len = len(self.elevators_task_queue[i])
                if elevators_motion_params[i]['target_floor'] is not None:
                    queue_len += 1
                if queue_len < min_queue_len:
                    task_queue = self.elevators_task_queue[i]
                    min_queue_len = queue_len
            task_queue.append(new_target_floor)
            return None, None

    def get_next_target(self, current_floor, elevator_num):
        task_queue = self.elevators_task_queue[elevator_num]
        if len(task_queue) > 0:
            return task_queue.pop(0)
        else:
            return None
