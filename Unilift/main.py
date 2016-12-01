from server import Server
from threading import Thread
import time


def print_available_command():
    print('To open door type: open <lift number>')
    print('To close door type: close <lift number>')
    print('To call elevator type: call <floor number>')
    print('To exit programme type: exit')
    # TODO: написать остальные команды


# noinspection PyShadowingNames
def handle(server, command):
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
        if parts[1] > server.ELEVATORS_NUM or parts[1] < 1:
            print('Error! The {} lift does not exist.'.format(parts[1]))
            return False
        server.cabins[parts[1] - 1].open_doors()
        server.cabins[parts[1] - 1].wait_doors()

    elif parts[0] == 'close':
        if len(parts) > 2 or len(parts) == 1:
            print('Error! Expected 1 argument for command \'close\', got {}'.format(len(parts) - 1))
            return False
        try:
            parts[1] = int(parts[1])
        except ValueError:
            print('Error! Type of parameter for command \'close\' must be int')
            return False
        if parts[1] > server.ELEVATORS_NUM or parts[1] < 1:
            print('Error! The {} lift does not exist.'.format(parts[1]))
            return False
        server.cabins[parts[1] - 1].close_doors()
        server.cabins[parts[1] - 1].wait_doors()

    if parts[0] == 'call':
        if len(parts) > 2 or len(parts) == 1:
            print('Error! Expected 1 argument for command \'call\', got {}'.format(len(parts) - 1))
            return False
        try:
            parts[1] = int(parts[1])
        except ValueError:
            print('Error! Type of parameter for command \'call\' must be int')
            return False
        if parts[1] > server.FLOORS_NUMBER or parts[1] < 1:
            print('Error! The {} floor does not exist.'.format(parts[1]))
            return False
        server.call_cabin(parts[1] - 1)

    elif parts[0] == 'smoke':
        if len(parts) > 1:
            print('Error! Expected 0 argument for command \'smoke\', got {}'.format(len(parts) - 1))
            return False
        server.smoke_exit()
        return True

    elif parts[0] == 'go':
        if len(parts) > 2 or len(parts) == 1:
            print('Error! Expected 1 argument for command \'close\', got {}'.format(len(parts) - 1))
            return False
        try:
            parts[1] = int(parts[1])
        except ValueError:
            print('Error! Type of parameter for command \'close\' must be int')
            return False
        if parts[1] > server.ELEVATORS_NUM or parts[1] < 1:
            print('Error! The {} lift does not exist.'.format(parts[1]))
            return False
        print(server.cabins[parts[1]].get_current_state())
        server.cabins[parts[1]].close_doors()
        print(server.cabins[parts[1]].get_current_state())

    elif parts[0] == 'exit':
        if len(parts) > 1:
            print('Error! Expected 0 argument for command \'exit\', got {}'.format(len(parts) - 1))
            return False
        server.set_end_status()
        return True
    else:
        print('Wrong command: {}'.format(command))
    return False


if __name__ == '__main__':
    server = Server()

    call_dispatcher_buttons = []
    threads = [Thread(target=server.run)]
    for i in range(server.ELEVATORS_NUM):
        call_dispatcher_buttons.append(server.cabins[i])
        # threads.append(Thread(target=call_dispatcher_buttons[i].press))

    for thread in threads:
        thread.start()

    time.sleep(0.5)

    print('Choose action:')
    print_available_command()
    while True:
        command = input()
        status = handle(server, command)
        if status:
            break

    for thread in threads:
        thread.join()
