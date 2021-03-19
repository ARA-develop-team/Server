"""ADDITIONAL CODE"""

import matplotlib.pyplot as plt
import time


class CAnalysis:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.start_time = None
        self.speed_data = [[]]
        self.time_period = 1
        self.time_aim = None

    def launch(self):
        print("\033[33m{}".format("Hello from the ARA ADDITIONAL CODE \n[ANALYSING]"))
        self.start_time = time.time()
        self.time_aim = self.start_time + self.time_period

    def processing(self):
        time_time = time.time()
        if time_time >= self.time_aim:
            self.time_aim = time_time + self.time_period
            self.speed_data.append([])

        if len(self.speed_data[len(self.speed_data) - 1]) != 0:
            self.speed_data[len(self.speed_data) - 1][0] += 1
        else:
            self.speed_data[len(self.speed_data) - 1].append(1)

    def result(self):
        total = 0
        midline = []
        print(self.speed_data)
        for x in self.speed_data:
            total += x[0]
        average = total / len(self.speed_data)
        print(average)
        for _ in self.speed_data:
            midline.append([average])
        print("\033[33m{}".format("[RESULT]"))
        plt.plot(self.speed_data, label='line', color='blue')
        plt.plot(midline, label='line', color='red')
        plt.title('MAIN')
        plt.xlabel('seconds')
        plt.ylabel('cycle')
        plt.grid(True)
        plt.show()


if __name__ == '__main__':
    analysis = CAnalysis()
    analysis.launch()
    run = True
    while run:
        try:
            analysis.processing()
            # time.sleep(1)

        except KeyboardInterrupt:
            analysis.result()
            run = False
