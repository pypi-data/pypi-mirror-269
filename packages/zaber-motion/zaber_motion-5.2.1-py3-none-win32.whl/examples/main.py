"""
Example to see how the Python API works.

Pre-requisites:
    This example file zaber_motion runs on Python 3,
    whereas the build environment for zaber_motion needs to run on Python 2.
    After doing gulp build in Python 2, switch to Python 3 environment
    cd $GOPATH/src/zaber-motion-lib/py and execute the following:
    python3 -m invoke install

Usage:
    main.py
    main.py list
    main.py <comm_port>
    main.py -h | --help
    main.py --version

Options:
    -h --help    Show this screen.
    --version    Show version.
"""
import time
from docopt import docopt
from zaber_motion.ascii import Connection
from zaber_motion import Units, Library, LogOutputMode, Tools


def run_example(conn: Connection):
    """
    Run actual example

    :param comm: opened communication port object
    :return: None
    """
    with conn:
        devices = conn.detect_devices()
        device = devices[0]

        device.all_axes.home()

        axis = device.get_axis(1)

        axis.move_absolute(1, Units.LENGTH_CENTIMETRES)

        axis.move_relative(-5, Units.LENGTH_MILLIMETRES)

        axis.move_velocity(1, Units.VELOCITY_MILLIMETRES_PER_SECOND)
        time.sleep(2)
        axis.stop()

        position = axis.get_position(Units.LENGTH_MILLIMETRES)
        print("Position: ", position)

    time.sleep(2)


def cmd_list():
    """
    Print a list of potential comm ports for user to choose from.

    Handy when plugging in a new USB-to-Serial converter.
    :return: None
    """
    print("List of potential comm ports:")

    ports = Tools.list_serial_ports()
    if len(ports) == 0:
        print("No ports found.")

    for port in ports:
        print("   ", port)


def cmd_example(args):
    """
    Run the examples with a known comm port.

    :param args: docopt arguments, one of which is the comm port string.
    :return: None
    """
    print("Example code communicating with Zaber device")
    conn = Connection.open_serial_port(args['<comm_port>'])
    run_example(conn)


def cmd_default():
    """
    When no comm port is specified, prompt for a comm port.

    :return: None
    """
    comm_port = input("Please enter communication port:")
    if comm_port == '':
        print("No comm port specified. Try main.py -h for help.")
        exit(1)
    conn = Connection.open_serial_port(comm_port)
    run_example(conn)


def main():
    """
    Parse command line arguments and call the correct command helper.

    :return: None
    """
    args = docopt(__doc__)
    if args['list']:
        cmd_list()
    elif args['<comm_port>']:
        cmd_example(args)
    else:
        cmd_default()


# run main function on program start
if __name__ == '__main__':
    Library.set_log_output(LogOutputMode.STDOUT)
    main()
