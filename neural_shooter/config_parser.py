"""get IP and port for the neural shooter"""

import yaml


def getting_start_data(file_name):
    with open(file_name) as file:
        data_yml = yaml.load(file, yaml.Loader)
        for data in data_yml:
            if data_yml[data] is None:
                print(f"[ValueError] {data} is empty! \nMake changes in the file '{file_name}'")
                return False
            elif type(data_yml[data]) is str:
                try:
                    data_yml[data] = tuple(map(int, data_yml[data].split(', ')))

                except ValueError:
                    print(f"[WARNING] '{data_yml[data]}' still str!")

        return data_yml


def getting_socket_data(file_name):
    with open(file_name) as file:
        data = {}
        data_yml = yaml.load(file, yaml.Loader)

        try:
            data['PORT'] = int(data_yml[1]['PORT'])
        except ValueError:
            print(f"[ValueError]  PORT must consist only of numbers! \nMake changes in the file '{file_name}'")
            quit()

        if data_yml[0]['IP'].lower() == 'default' or data_yml[0]['IP'].lower() is None:
            import socket
            data['IP'] = socket.gethostbyname(socket.gethostname())

        else:
            data['IP'] = data_yml[0]['IP']

        return data


if __name__ == "__main__":
    using_file = [r"start.yml"]  # temp data
    for path in using_file:
        result = getting_start_data(path)
        print(result)
