# type: ignore

from microbit import *

print('start')
reading = False
while True:
    if button_a.is_pressed():
        reading = True
        display.show(Image.YES)
        sleep(3000)
        display.clear()
    if button_b.is_pressed():
        reading = False
        display.show(Image.NO)
        sleep(3000)
        display.clear()
        print('Stopped')
    if reading:
        print({% function %}())
    sleep(2000)