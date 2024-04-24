import argparse
import os
import uflash
from . import UBitLogger, NoUBitFound, __version__


def cli() -> None:

    parser = argparse.ArgumentParser(
        prog='ubitlogger',
        description="micro:bit serial port logger",
        epilog='https://github.com/p4irin/ubitlogger'
    )

    parser.add_argument(
        '-V',
        '--version',
        action='version',
        version=f'{__version__}',
        help='show version and exit.'
    )

    sub_parsers = parser.add_subparsers(
        title='Sub commands',
        dest='command'
    )

    sp_start = sub_parsers.add_parser(
        'start',
        help="start logging",
    )

    sp_start.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help='show debugging output'
    )
    sp_start.add_argument(
        '-t',
        '--timeout',
        action='store',
        type=float,
        help='set a timeout (float)'
    )
    sp_start.add_argument(
        '-i',
        '--interval',
        action='store',
        type=int,
        help='time between readings'
    )

    sp_flash = sub_parsers.add_parser(
        'flash',
        help='Flash an example sensor reader script to the micro:bit. '
            + 'Does NOT work on WSL! On Ubuntu jammy the micro:bit is '
            + 'NOT auto mounted! You need to mount it like '
            + '"sudo mount /dev/<device> /media/MICROBIT". '
            + 'Figure out the <device> with "sudo fdisk -l". '
            + 'To flash you need sudo and the path to ubitlogger! '
            + 'I.e., "sudo venv/bin/ubitlogger flash -s light", '
            + 'assuming you use a virtualenv venv.'
    )
    sp_flash.add_argument(
        '-s',
        '--sensor',
        action='store',
        choices=['temperature', 'light', 'accelerometer'],
        required=True,
        help='Specify the sensor to read'
        )

    args = parser.parse_args()
    kwargs = {}
    if args.command == 'start':
        if args.debug:
            debug_flag = True
        else:
            debug_flag = False
        kwargs['debug'] = debug_flag
        if args.timeout:
            kwargs['timeout'] = args.timeout
        if args.interval:
            kwargs['interval'] = args.interval

    if args.command == 'flash':
        if args.sensor and 'WSL' not in os.uname().release:
            if args.sensor == 'temperature':
                _function = args.sensor
            if args.sensor == 'light':
                _function = 'display.read_light_level'
            if args.sensor == 'accelerometer':
                _function = 'accelerometer.get_values'

            package_dir = os.path.dirname(os.path.abspath(__file__))
            script_file_path = f'{package_dir}/read_sensor.py'
            script_file_copy_path = script_file_path.replace('.py', '_copy.py')
            with open(script_file_path, 'r') as fh:
                script = fh.read()
                script = script.replace('{% function %}', _function)
                with open(script_file_copy_path, 'w') as fh_copy:
                    fh_copy.write(script)
            uflash.flash(path_to_python=script_file_copy_path)
            exit(0)
        else:
            print("WSL doesn't support flashing!")
            exit(1)

    try:
        ubitlogger = UBitLogger(**kwargs)
        ubitlogger.start()
    except NoUBitFound:
        print("No micro:bit found ! Is it plugged in ?")
