import test

from zaber_motion.ascii import Connection, StreamAxisDefinition, StreamAxisType
from zaber_motion import Units, Measurement, RotationDirection
from zaber_motion import Library, DeviceDbSourceType

def print_stream_information(stream):
    print("Stream string representation:")
    print(stream.__repr__())

    print("Axes stream targets:")
    print(stream.axes)

    print("Max speed:")
    print(stream.get_max_speed(Units.VELOCITY_CENTIMETRES_PER_SECOND))

    print("Max tangential acceleration:")
    print(stream.get_max_tangential_acceleration(Units.ACCELERATION_CENTIMETRES_PER_SECOND_SQUARED))

    print("Max centripetal acceleration:")
    print(stream.get_max_centripetal_acceleration(Units.ACCELERATION_CENTIMETRES_PER_SECOND_SQUARED))

def main():
    with Connection.open_serial_port("/dev/ttyUSB0") as connection:
        Library.set_device_db_source(DeviceDbSourceType.WEB_SERVICE, 'https://api.zaber.io/device-db/master')
        device_list = connection.detect_devices()
        print("Found {} devices".format(len(device_list)))

        device = device_list[0]

        lockstep = device.get_lockstep(1)
        if lockstep.is_enabled():
            lockstep.disable()

        device.all_axes.home()

        lockstep.enable(1, 2)

        num_streams = device.settings.get('stream.numstreams')
        print('Number of streams possible:', num_streams)

        num_stream_buffers = device.settings.get('stream.numbufs')
        print('Number of stream buffers on device:', num_stream_buffers)

        stream = device.streams.get_stream(1)
        stream.setup_live([StreamAxisDefinition(1, StreamAxisType.LOCKSTEP)])
        print_stream_information(stream)

        # alter movement settings
        stream.set_max_centripetal_acceleration(5, Units.ACCELERATION_CENTIMETRES_PER_SECOND_SQUARED)
        stream.set_max_tangential_acceleration(5, Units.ACCELERATION_CENTIMETRES_PER_SECOND_SQUARED)
        stream.set_max_speed(1, Units.VELOCITY_MILLIMETRES_PER_SECOND)

        stream.cork()

        stream.line_absolute([Measurement(10, Units.LENGTH_MILLIMETRES)])
        stream.line_relative([Measurement(-5, Units.LENGTH_MILLIMETRES)])
        stream.wait(2, Units.TIME_SECONDS)

        stream.uncork()

        if stream.is_busy():
            print("Waiting until stream completes...")
            stream.wait_until_idle()

        print_stream_information(stream)

        stream.disable()
        print("Stream finished.")

        lockstep.disable()

main()
