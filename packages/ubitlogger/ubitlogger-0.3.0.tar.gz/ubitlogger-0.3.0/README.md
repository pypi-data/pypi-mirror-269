![PyPI - Version](https://img.shields.io/pypi/v/ubitlogger)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ubitlogger)
![PyPI - License](https://img.shields.io/pypi/l/ubitlogger)
[![Static Badge](https://img.shields.io/badge/microbit-v1.3x-blue?logo=microbit&link=https%3A%2F%2Ftech.microbit.org%2Fhardware%2F1-3-revision%2F)](https://tech.microbit.org/hardware/1-3-revision/)
[![Static Badge](https://img.shields.io/badge/Ubuntu-22.04_LTS_jammy-orange?logo=ubuntu)](https://ubuntu.com/download/server)
[![Static Badge](https://img.shields.io/badge/Raspberry_Pi-4B_8GB-red?logo=raspberrypi&logoColor=red)](https://www.raspberrypi.com/products/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
# ubitlogger

A micro:bit serial port logger

## Stack

- Python 3.8, 3.9, 3.10
- Ubuntu 22.04 LTS jammy on
    - WSL 2 on Windows 11
        - usbipd-win to attach micro:bit to WSL
    - Raspberry Pi 4B, 8GB
- micro:bit
    - Board revision 1.3B
    - Bootloader 02xx
    - Interface 0253
    - See [update daplink version](https://tech.microbit.org/software/daplink-interface/#:~:text=It%20is%20possible%20to%20update%20the%20version%20of%20DAPLink%20running%20on%20your%20micro%3Abit)

## Installation

### From PyPI

```bash
(venv) $ pip install ubitlogger
(venv) $
```

### or from GitHub

```bash
(venv) $ pip install git+https://github.com/p4irin/ubitlogger.git
(venv) $
```

## Usage

```bash
# Show version
(venv) $ ubitlogger -V
x.y.x

# Show help
(venv) $ ubitlogger -h
usage: ubitlogger [-h] [-V] {start,flash} ...

micro:bit serial port logger

options:
  -h, --help     show this help message and exit
  -V, --version  show version and exit.

Sub commands:
  {start,flash}
    start        start logging
    flash        Flash an example sensor reader script to the micro:bit.
                 Does NOT work on WSL! On Ubuntu jammy the micro:bit is
                 NOT auto mounted! You need to mount it like "sudo mount
                 /dev/<device> /media/MICROBIT" Figure out the <device>
                 with "sudo fdisk -l". To flash, you need sudo and the
                 path to ubitlogger! I.e., "sudo venv/bin/ubitlogger
                 flash -s light", assuming you use a virtualenv venv.

# Show help on start sub command
(venv) $ ubitlogger start -h
usage: ubitlogger start [-h] [-d] [-t TIMEOUT]

options:
  -h, --help            show this help message and exit
  -d, --debug           show debugging output
  -t TIMEOUT, --timeout TIMEOUT
                        set a timeout (float)

# Show help on the flash sub command
(venv) $ ubitlogger flash -h
usage: ubitlogger flash [-h] -s {temperature,light}

options:
  -h, --help            show this help message and exit
  -s {temperature,light}, --sensor {temperature,light}
                        Specify the sensor to read

# Log to the console with defaults
(venv) $ ubitlogger start
...
<data>
...
# Hit CTRL-C to stop logging
^C
Exited by CTRL-C
Cleaning up thread
--> Waiting for thread to finish

# Log to a file
(venv) $ ubitlogger start > data.log

# Flashing an example script to read a sensor, currently temperature and light.
# This doesn't work on WSL as we can't mount the micro:bit as a
# USB mass storage device.
# On Ubuntu jammy the micro:bit isn't auto mounted.
# First figure out the device with
(venv) $ sudo fdisk -l
# and then mount it like this
(venv) $ sudo mount /dev/<device> /media/MICROBIT

# Flash a script to the micro:bit that reads the light sensor and sends
# readings to the serial port.
(venv) $ sudo venv/bin/ubitlogger flash -s light
```

## Using ubitlogger from a linux distro on WSL 2

Connect a USB device to your linux distro on WSL 2 using [usbipd-win](https://github.com/dorssel/usbipd-win)

List USB devices

```powershell
PS C:\Users\p4irin> usbipd list --usbids

Connected:
BUSID  VID:PID  DEVICE                          STATE
1-1    046d:c534  Logitech, Inc., NanoReceiver  Not shared
1-3    0d28:0204  NXP, ARM  mbed                Not Shared
...
```

Register/bind a USB device for sharing. Device "NXP, ARM mbed" with busid _1-3_ identifies our micro:bit:

```powershell
PS C:\Users\p4irin> usbipd bind --busid 1-3
```

If you list USB devices again, the microbit wil show up as _Shared_:

```powershell
PS C:\Users\p4irin> usbipd list --usbids

Connected:
BUSID  VID:PID  DEVICE                          STATE
1-1    046d:c534  Logitech, Inc., NanoReceiver  Not shared
1-3    0d28:0204  NXP, ARM  mbed                Shared
...
PS C:\Users\p4irin>
```

Attach the USB device to WSL:

```powershell
PS C:\Users\p4irin> usbipd attach --wsl --busid 1-3 --auto-attach

usbipd: info: Using WSL distribution 'Ubuntu-22.04' to attach; the device will be available in all WSL 2 distributions.
usbipd: info: Using IP address 172.21.144.1 to reach the host.
usbipd: info: Starting endless attach loop; press Ctrl+C to quit.

PS C:\Users\p4irin>
```

Listing USB devices will show the micro:bit attached:

```powershell
PS C:\Users\p4irin> usbipd list --usbids

Connected:
BUSID  VID:PID  DEVICE                          STATE
1-1    046d:c534  Logitech, Inc., NanoReceiver  Not shared
1-3    0d28:0204  NXP, ARM  mbed                Attached
...
PS C:\Users\p4irin>
```

In your WSL distro's terminal, check if the micro:bit is listed:

```bash
$ lsusb
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 001 Device 004: ID 0d28:0204 NXP ARM mbed
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
$
```

Now run _ubitlogger_ in your Python virtualenv:

```bash
(venv) $ ubitlogger start -d -t 3

Found a micro:bit on: /dev/ttyACM0
Listening on port /dev/ttyACM0
Baudrate: 115200
Data bits: 8
Stop bits: 1
Parity: N
timeout: 3.0
18 17
18 6
^C
Exited by CTRL-C
Cleaning up thread
--> Waiting for thread to finish.

(venv) $
```

To detach the device from WSL:

```powershell
PS C:\Users\p4irin> usbipd detach --busid 1-3
```

## Reference

* [pySerial](https://pythonhosted.org/pyserial/)
* [usbipd-win](https://github.com/dorssel/usbipd-win)
* [micro:bit 1.3x](https://tech.microbit.org/hardware/1-3-revision/)