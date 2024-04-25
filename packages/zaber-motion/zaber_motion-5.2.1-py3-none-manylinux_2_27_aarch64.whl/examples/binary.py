import time
from zaber_motion.binary import Connection, Device
from zaber_motion import Units, Library, LogOutputMode

def main():
    Library.set_log_output(LogOutputMode.STDOUT)

    with Connection.open_serial_port("COM3") as conn:
        devices = conn.detect_devices()
        device = devices[0]
        print("Device %d has device ID %d." %(device.device_address, device.identity.device_id))

        pos = device.home(Units.LENGTH_CENTIMETRES)
        print("Position after home: %5.2f cm." %pos)

        pos = device.move_absolute(1.0, Units.LENGTH_CENTIMETRES)
        print("Position after move absolute: %5.2f cm." %pos)

        pos = device.move_relative(5.0, Units.LENGTH_MILLIMETRES);
        print("Position after move relative: %5.2f mm." %pos);

        velocity = device.move_velocity(1.0, Units.VELOCITY_MILLIMETRES_PER_SECOND);
        print("Starting move velocity with speed: %5.2f mm/s." %velocity);

        time.sleep(2)

        pos = device.stop(Units.LENGTH_CENTIMETRES);
        print("Position after stop: %5.2f cm." %pos);

        print("Final position in microsteps: %d." %device.get_position());


if __name__ == '__main__':
    main()
