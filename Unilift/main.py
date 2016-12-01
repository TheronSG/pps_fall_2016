from server import Server
from threading import Thread


def print_available_command():
    print('To open door type: open <lift number>')
    print('To close door type: close <lift number>')
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

        # TODO

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
        for i in range(server.ELEVATORS_NUM):
            server.engines[i].set_end_status()
            server.cabins[i].set_end_status()
        return True
    else:
        print('Wrong command: {}'.format(command))
    return False


if __name__ == '__main__':
    server = Server()
    Thread(target=server.run()).start()

    while True:
        print('Choose action:')
        print_available_command()
        command = input()
        status = handle(server, command)
        if status:
            break
