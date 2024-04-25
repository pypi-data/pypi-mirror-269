from zaber_motion.ascii import Connection
from zaber_motion.microscopy import Microscope
from zaber_motion import Library, LogOutputMode

Library.set_log_output(LogOutputMode.STDOUT)

with Connection.open_network_share("cs-mvr", NETWORK_SHARE_PORT, "COM1") as connection:
    connection.detect_devices()

    scope = Microscope.find(connection)

    scope.initialize()

    print(vars(scope))

    if scope.illuminator:
        channel = scope.illuminator.get_channel(1)
        channel.set_intensity(0.5)
        print(channel.get_intensity())
        channel.on()
        channel.off()

    if scope.filter_changer:
        changer = scope.filter_changer
        print(changer.get_number_of_filters())
        changer.change(1)
        changer.change(2)
        print(changer.get_current_filter())

    if scope.objective_changer:
        changer = scope.objective_changer
        for i in range(4):
            changer.change(i + 1)
            print(changer.get_current_objective())

    if scope.focus_axis:
        axis = scope.focus_axis
        pos = axis.get_position()
        axis.move_max()
        axis.move_absolute(pos)
