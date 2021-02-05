"""get IP and port for the neural shooter"""

import yaml


def getting_data(file_name):
    with open(file_name) as file:
        data = {}
        data_yml = yaml.load(file, yaml.Loader)

        try:
            data['PORT'] = int(data_yml[1]['PORT'])
        except ValueError:
            print(f"[ValueError]  PORT must consist only of numbers! \nMake changes in the file '{file_name}'")
            quit()

        if data_yml[0]['IP'].lower() == 'default':
            import socket
            data['IP'] = socket.gethostbyname(socket.gethostname())

        else:
            data['IP'] = data_yml[0]['IP']

        return data


if __name__ == "__main__":
    using_file = [r"client.yml", r"server.yml"]      # temp data
    for path in using_file:
        result = getting_data(path)
        print(result)


