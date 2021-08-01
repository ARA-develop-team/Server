import matplotlib.pyplot as plt
from PIL import Image  # ImageDraw
import os
print(os.name)
if os.name == 'posix':
    from subprocess import check_output
elif os.name == 'nt':
    import win32api, win32con, win32process
    from ctypes import windll
    user32 = windll.user32


def get_locale():
    if os.name == 'nt':
        w = user32.GetForegroundWindow()
        tid = user32.GetWindowThreadProcessId(w, 0)
        win32api.LoadKeyboardLayout('00000409', 1)  # to switch to english
        return hex(user32.GetKeyboardLayout(tid))
    elif os.name == 'posix':
        win32api.LoadKeyboardLayout('00000409', 1)

def test_matplotlib():
    y = [[574], [565.875], [609], [605], [606], [606], [612], [613], [610], [603], [607], [600], [589], [585], [586],
         [591],
         [592], [591], [543], [448], [588], [591], [597], [599], [524]]

    array = [[1, 2], [3, 5]]
    for x in array:
        print(x)

    # plt.plot(y, label='line', color='blue')
    # plt.plot(midline, label='line', color='red')
    plt.title('MAIN')
    plt.xlabel('seconds')
    plt.ylabel('cycle')
    plt.grid(True)
    plt.show()


def test_img_load():
    image = Image.open('map2.jpg')  # Открываем изображение
    # draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования
    width = image.size[0]  # Определяем ширину
    height = image.size[1]  # Определяем высоту
    pix = image.load()  # Выгружаем значения пикселей
    map_list = []
    empty = 0
    not_empty = 0
    for y in range(height):
        print(y)
        map_list.append([])
        for x in range(width):
            # print(pix)
            r = pix[x, y][0]  # узнаём значение красного цвета пикселя
            g = pix[x, y][1]  # зелёного
            b = pix[x, y][2]  # синего

            if r == 0 and g == 0 and b == 0:
                map_list[len(map_list) - 1].append(1)
                not_empty += 1
            else:
                map_list[len(map_list) - 1].append(0)
                empty += 1
            # sr = (r + g + b) // 1  # среднее значение
            # draw.point((x, y), (sr, sr, sr))  # рисуем пиксель
    # image.save("result.jpg", "JPEG")
    for element in map_list:
        print(element)
    print(empty)
    print(not_empty)
    return map_list


class Parent:
    def __init__(self, age):
        self.age = age


class Child(Parent):
    def __init__(self, age, name):
        super().__init__(age)
        self.name = name

    def __str__(self):
        return f"Child class"


if __name__ == "__main__":
    get_locale()
    # ch = Child(12, 'Alex')
    # print(ch.name, ch.age)
    # print(ch)

    # print(x.count(4))
    #
    # size = (800, 400)
    # print(size[0])
    #
    # test_img_load()
