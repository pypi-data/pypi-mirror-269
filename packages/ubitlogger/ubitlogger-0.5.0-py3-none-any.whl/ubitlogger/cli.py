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
        choices=['temperature', 'light', 'accelerometer', 'radio'],
        required=True,
        help='Specify the sensor to read'
        )
    sp_flash.add_argument(
        '-rg',
        '--radio-group',
        action='store',
        type=int,
        required=False,
        help='Specify the "group" the radio should listen on. '
            + 'A "group" is a number between 0 and 255, inclusive. '
            + 'The default is 0.'
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
        if 'WSL' in os.uname().release:
            print("WSL doesn't support flashing!")
            exit(1)

        if args.sensor:
            if args.sensor == 'temperature':
                _function = args.sensor
            if args.sensor == 'light':
                _function = 'display.read_light_level'
            if args.sensor == 'accelerometer':
                _function = 'accelerometer.get_values'
            if args.sensor == 'radio':
                radio_group = args.radio_group if args.radio_group else 0
                if radio_group not in range(0, 256):
                    print('Use a radio-group between 0 and 255, inclusive.')
                    exit(0)
                micropython_script_name = 'data_receiver'
                replace_this = '{% group %}'
                replace_with = str(radio_group)
            if args.sensor in ['temperature', 'light', 'accelerometer']:
                micropython_script_name = 'read_sensor'
                replace_this = '{% function %}'
                replace_with = _function

            package_dir = os.path.dirname(os.path.abspath(__file__))
            script_file_path = f'{package_dir}/{micropython_script_name}.py'
            script_file_copy_path = script_file_path.replace('.py', '_copy.py')
            with open(script_file_path, 'r') as fh:
                script = fh.read()
                script = script.replace(replace_this, replace_with)
                with open(script_file_copy_path, 'w') as fh_copy:
                    fh_copy.write(script)

            uflash.flash(path_to_python=script_file_copy_path)
            exit(0)

    try:
        ubitlogger = UBitLogger(**kwargs)
        ubitlogger.start()
    except NoUBitFound:
        print("No micro:bit found ! Is it plugged in ?")
