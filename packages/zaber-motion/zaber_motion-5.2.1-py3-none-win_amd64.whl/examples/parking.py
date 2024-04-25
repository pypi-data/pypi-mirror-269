"""
Example to see how parking devices works

Pre-requisites:
    This example file zaber_motion runs on Python 3,
    whereas the build environment for zaber_motion needs to run on Python 2.
    After doing gulp build in Python 2, switch to Python 3 environment
    cd $GOPATH/src/zaber-motion-lib/py and execute the following:
    python3 -m invoke install
"""
import time
from zaber_motion.binary import Connection
from zaber_motion import Units, Library, LogOutputMode, Tools

Library.set_log_output(LogOutputMode.STDOUT)

Library.toggle_device_db_store(True)

with Connection.open_tcp("192.168.100.179", 6790) as connection:
    device_list = connection.detect_devices()
    print("Found {} devices".format(len(device_list)))
    device = device_list[0]
    device.all_axes.park()
    device.all_axes.unpark()
    device.all_axes.park()
    device.all_axes.unpark()
