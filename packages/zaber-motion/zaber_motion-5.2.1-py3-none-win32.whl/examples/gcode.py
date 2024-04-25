from zaber_motion import DeviceDbSourceType, Library, LogOutputMode, Measurement
from zaber_motion.ascii import Connection
from zaber_motion.gcode import Translator
from zaber_motion.gcode.axis_mapping import AxisMapping
from zaber_motion.gcode.translator_config import TranslatorConfig
from zaber_motion.units import Units

Library.set_log_output(LogOutputMode.STDOUT)

def main():
    with Connection.open_tcp("localhost", 11321) as connection:
        Library.set_device_db_source(DeviceDbSourceType.WEB_SERVICE, 'https://api.zaber.io/device-db/master')
        device_list = connection.detect_devices()

        device = device_list[0]
        device.all_axes.home()

        stream = device.streams.get_stream(1)

        stream.setup_live(1, 2)

        translator = Translator.setup(stream, TranslatorConfig(
            [
                AxisMapping(axis_index=0, axis_letter="Y"),
                AxisMapping(axis_index=1, axis_letter="X")
            ]
        ))
        translator.translate('G28 Y19')
        translator.translate('G0 X10 Y20')

        y = translator.get_axis_position('Y', Units.LENGTH_MILLIMETRES)
        translator.set_axis_position('Y', y * 2, Units.LENGTH_MILLIMETRES)

        translator.set_traverse_rate(3, Units.VELOCITY_MILLIMETRES_PER_SECOND)

        translator.translate('G0 X10 Y20')

        translator.flush()
        stream.disable()

main()
