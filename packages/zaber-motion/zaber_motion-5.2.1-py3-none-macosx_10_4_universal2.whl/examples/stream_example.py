import test

from zaber_motion.ascii import Connection, StreamAxisDefinition, StreamAxisType, DigitalOutputAction
from zaber_motion import Units, Measurement, RotationDirection
from zaber_motion import Library, DeviceDbSourceType

def append_line_movement(stream):
    stream.line_absolute(
        Measurement(29.0047, Units.LENGTH_MILLIMETRES),
        Measurement(40.49, Units.LENGTH_MILLIMETRES)
    )

    stream.line_relative(
        Measurement(0),
        Measurement(50.5, Units.LENGTH_MILLIMETRES)
    )

    # or, to write less, iterate over an array of points and convert to cm once
    path_in_cm = [(0.00, 3.00), (2.25, 7.10), (5.35, 0.15), (1.45, 10.20), (9.00, 9.00)]
    for point in path_in_cm:
        stream.line_absolute(
            Measurement(point[0], Units.LENGTH_CENTIMETRES),
            Measurement(point[1], Units.LENGTH_CENTIMETRES)
        )

def append_circular_movement(stream):
    # start at (4, 4)
    stream.line_absolute(
        Measurement(4, Units.LENGTH_CENTIMETRES),
        Measurement(4, Units.LENGTH_CENTIMETRES)
    )

    # do a clockwise rotation with radius 2, starting at 0 degrees
    circle_center_abs = (
        Measurement(2, Units.LENGTH_CENTIMETRES),
        Measurement(4, Units.LENGTH_CENTIMETRES)
    )
    stream.circle_absolute(RotationDirection.CW, circle_center_abs[0], circle_center_abs[1])

    # do a counter-clockwise rotation with radius 4, starting at 0 degrees
    circle_center_rel = (
        Measurement(-2, Units.LENGTH_CENTIMETRES),
        Measurement(0, Units.LENGTH_CENTIMETRES)
    )
    stream.circle_relative(RotationDirection.CCW, circle_center_rel[0], circle_center_rel[1])


def append_arc_movement(stream):
    # start at (4, 4)
    stream.line_absolute(
        Measurement(4, Units.LENGTH_CENTIMETRES),
        Measurement(4, Units.LENGTH_CENTIMETRES)
    )

    arc_circle_center_rel = (
        Measurement(-2, Units.LENGTH_CENTIMETRES),
        Measurement(0, Units.LENGTH_CENTIMETRES)
    )
    arc_end_rel = (
        Measurement(-4, Units.LENGTH_CENTIMETRES),
        Measurement(0, Units.LENGTH_CENTIMETRES)
    )
    # move from 0 degrees to 180 degrees of circle with radius 4
    stream.arc_relative(
        RotationDirection.CCW,
        arc_circle_center_rel[0],
        arc_circle_center_rel[1],
        arc_end_rel[0],
        arc_end_rel[1]
    )

    arc_circle_center_abs = (
        Measurement(2, Units.LENGTH_CENTIMETRES),
        Measurement(4, Units.LENGTH_CENTIMETRES)
    )
    arc_end_abs = (
        Measurement(4, Units.LENGTH_CENTIMETRES),
        Measurement(4, Units.LENGTH_CENTIMETRES)
    )
    # backtrace last arc movement by moving from 180 degrees to 0 degrees
    stream.arc_absolute(
        RotationDirection.CW,
        arc_circle_center_abs[0],
        arc_circle_center_abs[1],
        arc_end_abs[0],
        arc_end_abs[1]
    )


def append_io(stream):
    stream.set_digital_output(1, DigitalOutputAction.ON)

    stream.wait_digital_input(1, True)
    stream.set_digital_output(1, DigitalOutputAction.TOGGLE)

    stream.set_analog_output(1, 0.42) # In Volts
    # condition can be on of '!=', '<=', '>=', '==', '>', '<'
    stream.wait_analog_input(1, '>=', .50)

def print_stream_information(stream):
    print("Stream string representation:")
    print(stream.__repr__())

    print("Axes stream targets:")
    print(stream.axes)

    print("Stream mode:")
    print(stream.mode)

    print("Max speed:")
    print(stream.get_max_speed(Units.VELOCITY_CENTIMETRES_PER_SECOND))

    print("Max tangential acceleration:")
    print(stream.get_max_tangential_acceleration(Units.ACCELERATION_CENTIMETRES_PER_SECOND_SQUARED))

    print("Max centripetal acceleration:")
    print(stream.get_max_centripetal_acceleration(Units.ACCELERATION_CENTIMETRES_PER_SECOND_SQUARED))

def main():
    with Connection.open_tcp("localhost", Connection.TCP_PORT_DEVICE_ONLY) as connection:
        Library.set_device_db_source(DeviceDbSourceType.WEB_SERVICE, 'https://api.zaber.io/device-db/master')
        device_list = connection.detect_devices()
        print("Found {} devices".format(len(device_list)))

        device = device_list[0]
        device.all_axes.home()

        num_streams = device.settings.get('stream.numstreams')
        print('Number of streams possible:', num_streams)

        num_stream_buffers = device.settings.get('stream.numbufs')
        print('Number of stream buffers on device:', num_stream_buffers)

        stream = device.streams.get_stream(1)

        stream_buffer = device.streams.get_buffer(1)
        stream_buffer.erase()
        # set up stream to store actions to stream buffer 1 and
        # to use the first two axes for unit conversion
        stream.setup_store(stream_buffer, 1, 2)

        # append some line movement actions to the buffer
        append_line_movement(stream)

        print("Stream buffer contents:")
        print(stream_buffer.get_content())

        # change the streams mode from Store to Live
        stream.disable()

        stream.setup_live(1, 2)

        # append previously stored path movement to queue
        stream.call(stream_buffer)

        # add some circular and arc movement to the action queue
        append_circular_movement(stream)
        append_arc_movement(stream)

        # move only the first axis in the stream
        stream.line_absolute_on([1], [Measurement(1, Units.NATIVE)])

        # alter movement settings
        stream.set_max_centripetal_acceleration(5, Units.ACCELERATION_CENTIMETRES_PER_SECOND_SQUARED)
        stream.set_max_tangential_acceleration(5, Units.ACCELERATION_CENTIMETRES_PER_SECOND_SQUARED)
        stream.set_max_speed(0.5, Units.VELOCITY_MILLIMETRES_PER_SECOND)

        # append wait
        stream.wait(2, Units.TIME_SECONDS)

        # Optionally play with some I/O,
        # This section is commented out because your device may not support I/O
        # append_io(stream)

        print("Waiting...")
        stream.wait_until_idle()

        print_stream_information(stream)

        # cork stream execution
        stream.cork()

        stream.line_relative(
            Measurement(0.1, Units.LENGTH_MILLIMETRES),
            Measurement(0.14, Units.LENGTH_MILLIMETRES)
        )

        stream.line_relative(
            Measurement(2.10, Units.LENGTH_MILLIMETRES),
            Measurement(0.49, Units.LENGTH_MILLIMETRES)
        )

        # uncork and cause actions in queue to start executing with no discontinuities
        stream.uncork()

        # print some information about this stream
        print_stream_information(stream)

        if stream.is_busy():
            print("Waiting until stream completes...")
            stream.wait_until_idle()

        stream.disable()
        print("Stream finished.")

main()
