"""Program for working with sprites before using them in the game"""

from PIL import Image

box = (76, 27, 155, 170)

for img in range(0, 7):
    with Image.open(f'battery{img}.png') as battery:
        crop_battery = battery.crop(box)
        # crop_battery.show()
        crop_battery.save(f'icon_battery{img}.png')
        # small_battery = crop_battery.resize((19, 35))
        # small_battery.show()
        # small_battery.save(f'crop_battery{img}.png')


# with Image.open('ara2-large.png') as battery:
#     crop_battery = battery.crop(box)
#     crop_battery.save('ara2.png')
#     # crop_battery.show()
#     # small_battery = crop_battery.resize((19, 35))
#     # small_battery.show()
#     # small_battery.save(f'crop_battery_error.png')
