import argparse
import matplotlib.pyplot as plt
import time

from zaber_motion.ascii import *
from zaber_motion import Library, LogOutputMode, Units

def main():

    args = parse_command_line()
    portName = args.port
    deviceAddress = args.device
    sampleRate = args.rate
    delay = args.delay
    channelNames = args.channels

    if args.log:
        Library.set_log_output(LogOutputMode.STDOUT)

    # Sanitize timebase and delay.
    timeBase = max(0.1, 1000 / sampleRate)
    delay = max(0, delay)

    with Connection.open_serial_port(portName) as conn:
        device = conn.get_device(deviceAddress)
        device.identify()
        axis = device.get_axis(1)

        if args.home:
            print("Homing...")
            axis.home(True)

        # Configure FW scope settings.
        oscilloscope = device.oscilloscope
        oscilloscope.set_timebase(timeBase, Units.TIME_MILLISECONDS)
        oscilloscope.set_delay(delay, Units.TIME_MILLISECONDS)

        # Configure channels
        oscilloscope.clear()
        for channel in channelNames:
            oscilloscope.add_channel(1, channel)

        # Send move command if specified.
        if len(args.command) > 0:
            axis.generic_command_no_response(args.command)

        # Start scope capture.
        oscilloscope.start()

        # Wait for scope capture to finish.
        print("Waiting for data...")
        time.sleep((delay + 100) / 1000)
        data = oscilloscope.read()

        print("Plotting...")
        plot_data(data, delay, timeBase)


def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument("-port", default="COM2", help="Name of port to open.")
    parser.add_argument("-device", type=int, default=1, help="Address of device to communicate with")
    parser.add_argument("-rate", type=float, default=10000.0, help="Sample rate to use, in Hz. Must be an integer divisor of 10,000.")
    parser.add_argument("-delay", type=float, default=0.0, help="Delay before starting capture, in milliseconds.")
    parser.add_argument("-channels", nargs="*", default=["pos", "encoder.pos"], help="Channels to capture.")
    parser.add_argument("-command", default="move rel 1000000", help="Command to send to device at start of scope capture.")
    parser.add_argument("-home", action="store_true", help="Home the device first.")
    parser.add_argument("-log", action="store_true", help="Enable log output to console.")

    return parser.parse_args()


def plot_data(data, delay, timeBase):
    for i in range(len(data)):
        channel = data[i]
        samples = channel.get_data() # No unit conversion because channel may have been user specified.
        if i == 0:
            times = [channel.get_sample_time(t, Units.TIME_MILLISECONDS) for t in range(len(samples))]

        plt.plot(times, samples, label=channel.setting)

    plt.xlabel("Time (ms)")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
