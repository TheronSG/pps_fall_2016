from server import Server
from call_button import CallButton
from threading import Thread
import time


SLEEP_TIME = 0.33


def print_available_command():
    print('To open door type: open <lift number>')
    print('To close door type: close <lift number>')
    print('To call elevator type: call <floor number>')
    print('To go inside elevator type: go <floor number>')
    print('To call dispatcher type calldis <lift number>')
    print('To exit programme type: exit')


# noinspection PyShadowingNames
def handle(server, command, **kwargs):
    parts = command.split(' ')
    while True:
        try:
            parts.remove('')
        except ValueError:
            break

    if parts[0] == 'call':
        if len(parts) > 2 or len(parts) == 1:
            print('Error! Expected 1 argument for command \'call\', got {}'.format(len(parts) - 1))
            return False, kwargs['last_call_floor']
        try:
            parts[1] = int(parts[1])
        except ValueError:
            print('Error! Type of parameter for command \'call\' must be int')
            return False, kwargs['last_call_floor']
        if parts[1] > server.FLOORS_NUMBER or parts[1] < 1:
            print('Error! The {} floor does not exist.'.format(parts[1]))
            return False, kwargs['last_call_floor']
        call_button.press(parts[1] - 1)
        kwargs['last_call_floor'] = parts[1] - 1

    elif parts[0] == 'calldis':
        if len(parts) > 2 or len(parts) == 1:
            print('Error! Expected 1 argument for command \'calldis\', got {}'.format(len(parts) - 1))
            return False, kwargs['last_call_floor']
        try:
            parts[1] = int(parts[1])
        except ValueError:
            print('Error! Type of parameter for command \'calldis\' must be int')
            return False, kwargs['last_call_floor']
        if parts[1] > server.FLOORS_NUMBER or parts[1] < 1:
            print('Error! The {} floor does not exist.'.format(parts[1]))
            return False, kwargs['last_call_floor']
        server.elevators[parts[1] - 1].call_dispatcher_button.press()
        while not server.elevators[parts[1] - 1].speaker.get_state():
            time.sleep(SLEEP_TIME)
        server.elevators[parts[1] - 1].speaker.set_state()

    elif parts[0] == 'go':
        if len(parts) > 2 or len(parts) == 1:
            print('Error! Expected 1 argument for command \'go\', got {}'.format(len(parts) - 1))
            return False, kwargs['last_call_floor']
        try:
            parts[1] = int(parts[1])
        except ValueError:
            print('Error! Type of parameter for command \'go\' must be int')
            return False, kwargs['last_call_floor']
        if parts[1] > server.FLOORS_NUMBER or parts[1] < 1:
            print('Error! The {} floor does not exist.'.format(parts[1]))
            return False, kwargs['last_call_floor']
        last_call_floor = kwargs['last_call_floor']
        if last_call_floor is not None:
            elevator_num = None
            for i, engine in enumerate(server.engines):
                if engine.current_floor == last_call_floor:
                    elevator_num = i
                    break
            if elevator_num is not None:
                server.elevators[elevator_num].set_target_floor_button.press(parts[1] - 1)
            else:
                print('Error! You aren\'t in elevator yet!')
        else:
            print('Error! You haven\'t call elevator yet')

    elif parts[0] == 'exit':
        if len(parts) > 1:
            print('Error! Expected 0 argument for command \'exit\', got {}'.format(len(parts) - 1))
            return False
        server.set_end_status()
        return True, None
    else:
        print('Wrong command: {}'.format(command))
    return False, kwargs['last_call_floor']


if __name__ == '__main__':
    server = Server()
    call_button = CallButton(server)
    server_thread = Thread(target=server.run)
    server_thread.start()

    time.sleep(2 * SLEEP_TIME)

    print('Choose action:')
    print_available_command()
    last_call_floor = None
    while True:
        command = input()
        status, last_call_floor = handle(server, command, last_call_floor=last_call_floor)
        if status:
            break

    server_thread.join()
