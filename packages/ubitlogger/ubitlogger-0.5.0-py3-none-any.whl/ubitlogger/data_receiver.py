# type: ignore

"""MicroPython script template used by ubitlogger

Script lets a micro:bit act as a receiver of data sent by another micro:bit.
Only the 'group' setting of the radio can be set via the bitlogger CLI.
The default values apply for all other radio configuration settings. For
more info: [https://microbit-micropython.readthedocs.io/en/latest/radio.html
The data received is send over to ubitlogger over the serial link.
"""

from microbit import *
import radio

radio.config(group={% group %})
radio.on()

while True:
    message = radio.receive()
    if message:
        print(message)